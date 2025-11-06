"""Venue service with ChromaDB vector similarity search."""

import logging
from typing import List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.venue.embedding_service import EmbeddingService
from app.venue.models import Venue
from app.venue.vector_store import VenueVectorStore

logger = logging.getLogger(__name__)


class VenueService:
    """Service for venue operations including ChromaDB vector similarity search."""

    def __init__(self, db: Session, chroma_persist_dir: str = "./chroma_db"):
        """Initialize venue service.

        Args:
            db: Database session
            chroma_persist_dir: Directory for ChromaDB persistence
        """
        self.db = db
        self.embedding_service = EmbeddingService()
        self.vector_store = VenueVectorStore(persist_directory=chroma_persist_dir)

    async def search_venues_vector(
        self,
        query: str,
        category: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 20,
        similarity_threshold: float = 0.7,
    ) -> List[Tuple[Venue, float]]:
        """Perform vector similarity search on venues using ChromaDB.

        Args:
            query: Natural language search query
            category: Filter by category (nature, restaurant, attraction, accommodation)
            location: Filter by location string (searches in new_address field)
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0.0-1.0)

        Returns:
            List of tuples (Venue, similarity_score) sorted by similarity (descending)

        Raises:
            Exception: If embedding generation or search fails
        """
        # Generate query embedding
        logger.info(f"Generating embedding for query: {query}")
        query_embedding = await self.embedding_service.generate_query_embedding(query)

        # Build ChromaDB where filter
        where_filter = {}
        if category:
            where_filter["category"] = category

        # Search in ChromaDB
        venue_ids, similarities, metadatas = self.vector_store.search_similar_venues(
            query_embedding=query_embedding,
            n_results=limit * 2,  # Get more results to filter by similarity threshold
            where=where_filter if where_filter else None,
        )

        # Filter by similarity threshold and location
        filtered_results = []
        for venue_id, similarity in zip(venue_ids, similarities):
            if similarity < similarity_threshold:
                continue

            # Get full venue from database
            venue = self.db.query(Venue).filter(Venue.id == venue_id).first()

            if not venue:
                continue

            # Filter by location if specified
            if location and venue.new_address and location not in venue.new_address:
                continue

            # Filter by business status
            if venue.business_status != "영업중":
                continue

            filtered_results.append((venue, similarity))

            if len(filtered_results) >= limit:
                break

        logger.info(
            f"Found {len(filtered_results)} venues with similarity > {similarity_threshold}"
        )

        return filtered_results

    def format_venues_for_llm(
        self, venues_with_scores: List[Tuple[Venue, float]]
    ) -> str:
        """Format venue list into concise text for LLM context.

        Args:
            venues_with_scores: List of (Venue, similarity_score) tuples

        Returns:
            Formatted string suitable for LLM context injection
        """
        if not venues_with_scores:
            return "검색 결과가 없습니다."

        formatted = []

        for venue, similarity in venues_with_scores:
            info_parts = [f"- {venue.name} (관련도: {similarity:.2f})"]

            # Add category-specific information
            if venue.category == "restaurant":
                if venue.extra_info and "representative_menu" in venue.extra_info:
                    menu = venue.extra_info["representative_menu"]
                    info_parts.append(f"대표메뉴: {menu}")
                else:
                    info_parts.append("음식점")

            elif venue.category == "accommodation":
                if venue.extra_info:
                    room_count = venue.extra_info.get("room_count")
                    acc_type = venue.extra_info.get("accommodation_type")
                    facilities = venue.extra_info.get("facilities")

                    acc_info = []
                    if acc_type:
                        acc_info.append(acc_type)
                    if room_count:
                        acc_info.append(f"객실 {room_count}개")
                    if facilities:
                        acc_info.append(f"시설: {facilities}")

                    if acc_info:
                        info_parts.append(", ".join(acc_info))
                    else:
                        info_parts.append("숙박시설")
                else:
                    info_parts.append("숙박시설")

            elif venue.category == "attraction":
                if venue.extra_info and "tags" in venue.extra_info:
                    tags = venue.extra_info["tags"]
                    info_parts.append(f"특징: {tags}")
                else:
                    info_parts.append("관광명소")

            elif venue.category == "nature":
                if venue.extra_info and "tags" in venue.extra_info:
                    tags = venue.extra_info["tags"]
                    info_parts.append(f"특징: {tags}")
                else:
                    info_parts.append("자연명소")

            # Add location and transportation info
            if venue.subway_info:
                info_parts.append(f"교통: {venue.subway_info}")

            if venue.operating_hours:
                info_parts.append(f"운영: {venue.operating_hours}")

            if venue.phone:
                info_parts.append(f"전화: {venue.phone}")

            formatted.append(" | ".join(info_parts))

        return "\n".join(formatted)

    def get_venue_by_id(self, venue_id: int) -> Optional[Venue]:
        """Get venue by ID.

        Args:
            venue_id: Venue ID

        Returns:
            Venue object or None if not found
        """
        return self.db.query(Venue).filter(Venue.id == venue_id).first()

    def get_venue_by_external_id(self, external_id: str) -> Optional[Venue]:
        """Get venue by external API ID.

        Args:
            external_id: External API ID

        Returns:
            Venue object or None if not found
        """
        return (
            self.db.query(Venue).filter(Venue.external_id == external_id).first()
        )

    def get_venues_by_category(
        self, category: str, limit: int = 100
    ) -> List[Venue]:
        """Get venues by category.

        Args:
            category: Venue category
            limit: Maximum number of results

        Returns:
            List of Venue objects
        """
        return (
            self.db.query(Venue)
            .filter(Venue.category == category)
            .filter(Venue.business_status == "영업중")
            .limit(limit)
            .all()
        )

    def count_venues(self) -> int:
        """Count total number of venues in database.

        Returns:
            Total venue count
        """
        return self.db.query(func.count(Venue.id)).scalar()

    def count_venues_by_category(self) -> dict:
        """Count venues grouped by category.

        Returns:
            Dictionary with category counts
        """
        results = (
            self.db.query(Venue.category, func.count(Venue.id))
            .group_by(Venue.category)
            .all()
        )

        return {category: count for category, count in results}
