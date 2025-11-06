"""ChromaDB-based vector store for venue embeddings."""

import logging
from typing import List, Optional, Tuple

import chromadb
from chromadb.config import Settings

from app.venue.models import Venue

logger = logging.getLogger(__name__)


class VenueVectorStore:
    """ChromaDB-based vector store for venue semantic search.

    Stores venue embeddings in a persistent ChromaDB collection
    for fast similarity search.
    """

    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_directory,
                anonymized_telemetry=False,
            )
        )

        # Get or create collection for venues
        self.collection = self.client.get_or_create_collection(
            name="venues",
            metadata={"description": "Seoul tourism venue embeddings"},
        )

        logger.info(
            f"ChromaDB initialized. Collection size: {self.collection.count()}"
        )

    def add_venue_embedding(
        self,
        venue_id: int,
        external_id: str,
        embedding: List[float],
        metadata: dict,
    ):
        """Add a single venue embedding to the store.

        Args:
            venue_id: Database venue ID
            external_id: External API ID
            embedding: Embedding vector
            metadata: Additional metadata (name, category, etc.)
        """
        self.collection.add(
            ids=[str(venue_id)],
            embeddings=[embedding],
            metadatas=[{**metadata, "external_id": external_id}],
        )

    def add_venue_embeddings_batch(
        self,
        venue_ids: List[int],
        external_ids: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict],
    ):
        """Add multiple venue embeddings in batch.

        Args:
            venue_ids: List of database venue IDs
            external_ids: List of external API IDs
            embeddings: List of embedding vectors
            metadatas: List of metadata dicts
        """
        # Add external_id to each metadata
        enhanced_metadatas = [
            {**metadata, "external_id": ext_id}
            for metadata, ext_id in zip(metadatas, external_ids)
        ]

        self.collection.add(
            ids=[str(vid) for vid in venue_ids],
            embeddings=embeddings,
            metadatas=enhanced_metadatas,
        )

        logger.info(f"Added {len(venue_ids)} venue embeddings to ChromaDB")

    def search_similar_venues(
        self,
        query_embedding: List[float],
        n_results: int = 20,
        where: Optional[dict] = None,
    ) -> Tuple[List[int], List[float], List[dict]]:
        """Search for similar venues using vector similarity.

        Args:
            query_embedding: Query embedding vector
            n_results: Number of results to return
            where: Metadata filter conditions (e.g., {"category": "restaurant"})

        Returns:
            Tuple of (venue_ids, similarities, metadatas)
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["metadatas", "distances"],
        )

        # Convert string IDs back to integers
        venue_ids = [int(id_str) for id_str in results["ids"][0]]

        # Convert distances to similarity scores (1 - distance)
        # ChromaDB returns squared L2 distance, convert to cosine similarity
        similarities = [1 - (dist / 2) for dist in results["distances"][0]]

        metadatas = results["metadatas"][0]

        return venue_ids, similarities, metadatas

    def delete_venue_embedding(self, venue_id: int):
        """Delete a venue embedding from the store.

        Args:
            venue_id: Database venue ID
        """
        try:
            self.collection.delete(ids=[str(venue_id)])
            logger.info(f"Deleted venue embedding: {venue_id}")
        except Exception as e:
            logger.warning(f"Failed to delete venue {venue_id}: {e}")

    def clear_all(self):
        """Clear all embeddings from the collection."""
        self.client.delete_collection(name="venues")
        self.collection = self.client.get_or_create_collection(
            name="venues",
            metadata={"description": "Seoul tourism venue embeddings"},
        )
        logger.info("Cleared all venue embeddings")

    def get_collection_stats(self) -> dict:
        """Get statistics about the vector store.

        Returns:
            Dictionary with collection statistics
        """
        return {
            "total_count": self.collection.count(),
            "collection_name": self.collection.name,
        }
