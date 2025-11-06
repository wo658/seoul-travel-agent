"""Embedding generation service for venue semantic search."""

from typing import List

from openai import AsyncOpenAI

from app.config import settings
from app.venue.models import Venue


class EmbeddingService:
    """Service for generating OpenAI embeddings for venues.

    Uses text-embedding-3-small model for cost-effective embedding generation.
    Dimension: 1536
    Cost: $0.02 / 1M tokens
    """

    def __init__(self):
        """Initialize embedding service with OpenAI client."""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for embedding generation")

        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.dimension = 1536

    def format_venue_description(self, venue: Venue) -> str:
        """Format venue information into a comprehensive description for embedding.

        Delegates to Venue.get_embedding_description() to avoid duplication.

        Args:
            venue: Venue object to format

        Returns:
            Formatted description string
        """
        return venue.get_embedding_description()

    async def generate_venue_embedding(self, venue: Venue) -> List[float]:
        """Generate embedding for a single venue.

        Args:
            venue: Venue object to generate embedding for

        Returns:
            List of floats representing the embedding vector (dimension=1536)

        Raises:
            Exception: If OpenAI API call fails
        """
        description = self.format_venue_description(venue)

        response = await self.client.embeddings.create(
            model=self.model, input=description, encoding_format="float"
        )

        return response.data[0].embedding

    async def batch_generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts in batch.

        More efficient than calling generate_venue_embedding multiple times
        as it reduces API calls.

        Args:
            texts: List of text strings to generate embeddings for

        Returns:
            List of embedding vectors

        Raises:
            Exception: If OpenAI API call fails
        """
        if not texts:
            return []

        response = await self.client.embeddings.create(
            model=self.model, input=texts, encoding_format="float"
        )

        return [item.embedding for item in response.data]

    async def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a search query.

        Args:
            query: Search query string

        Returns:
            List of floats representing the embedding vector

        Raises:
            Exception: If OpenAI API call fails
        """
        response = await self.client.embeddings.create(
            model=self.model, input=query, encoding_format="float"
        )

        return response.data[0].embedding
