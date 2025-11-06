"""Venue service with vector similarity search."""

import logging
from typing import List, Optional, Tuple

from pgvector.sqlalchemy import cosine_distance
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.venue.embedding_service import EmbeddingService
from app.venue.models import Venue

logger = logging.getLogger(__name__)


class VenueService:
    """Service for venue operations including vector similarity search."""

    def __init__(self, db: Session):
        """Initialize venue service.

        Args:
            db: Database session
        """
        self.db = db
        self.embedding_service = EmbeddingService()

    async def search_venues_vector(
        self,
        query: str,
        category: Optional[str] = None,
        location: Optional[str] = None,
        limit: int = 20,
        similarity_threshold: float = 0.7,
    ) -> List[Tuple[Venue, float]]:
        """Perform vector similarity search on venues.

        Args:
            query: Natural language search query
            category: Filter by category (nature, restaurant, attraction, accommodation)
            location: Filter by location string (searches in new_address field)
            limit: Maximum number of results to return
            similarity_threshold: Minimum similarity score (0.0-1.0)

        Returns:
            List of tuples (Venue, similarity_score) sorted by similarity (descending)

        Raises:
            Exception: If embedding generation or database query fails
        """
        # Generate query embedding
        logger.info(f"Generating embedding for query: {query}")
        query_embedding = await self.embedding_service.generate_query_embedding(query)

        # Calculate cosine similarity (1 - cosine_distance)
        similarity_expr = 1 - cosine_distance(Venue.description_embedding, query_embedding)

        # Build query with filters
        stmt = (
            select(Venue, similarity_expr.label("similarity"))
            .filter(Venue.business_status == "영업중")
            .filter(similarity_expr > similarity_threshold)
        )

        # Apply category filter
        if category:
            stmt = stmt.filter(Venue.category == category)

        # Apply location filter (searches in new_address)
        if location:
            stmt = stmt.filter(Venue.new_address.contains(location))

        # Order by similarity and limit results
        stmt = stmt.order_by(desc("similarity")).limit(limit)

        # Execute query
        result = self.db.execute(stmt)
        venues_with_scores = [(row.Venue, row.similarity) for row in result]

        logger.info(
            f"Found {len(venues_with_scores)} venues with similarity > {similarity_threshold}"
        )

        return venues_with_scores

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
