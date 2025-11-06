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

        # Filter by similarity threshold
        filtered_ids = [
            (vid, sim)
            for vid, sim in zip(venue_ids, similarities)
            if sim >= similarity_threshold
        ]

        if not filtered_ids:
            logger.info("No venues found above similarity threshold")
            return []

        # Extract venue IDs and create similarity map
        venue_ids_to_fetch = [vid for vid, _ in filtered_ids]
        similarity_map = {vid: sim for vid, sim in filtered_ids}

        # Build optimized DB query with filters
        query = self.db.query(Venue).filter(
            Venue.id.in_(venue_ids_to_fetch),
            Venue.business_status == "영업중",
        )

        # Add location filter if specified
        if location:
            query = query.filter(Venue.new_address.contains(location))

        # Fetch venues in single query
        venues = query.all()

        # Combine venues with similarity scores and sort by similarity
        results = [
            (venue, similarity_map[venue.id])
            for venue in venues
            if venue.id in similarity_map
        ]
        results.sort(key=lambda x: x[1], reverse=True)

        # Limit final results
        filtered_results = results[:limit]

        logger.info(
            f"Found {len(filtered_results)} venues with similarity > {similarity_threshold}"
        )

        return filtered_results

    def format_venues_for_llm(
        self, venues_with_scores: List[Tuple[Venue, float]]
    ) -> str:
        """Format venue list into concise text for LLM context.

        Delegates to Venue.get_llm_summary() to avoid duplication.

        Args:
            venues_with_scores: List of (Venue, similarity_score) tuples

        Returns:
            Formatted string suitable for LLM context injection
        """
        if not venues_with_scores:
            return "검색 결과가 없습니다."

        return "\n".join(
            venue.get_llm_summary(similarity) for venue, similarity in venues_with_scores
        )

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
