"""ChromaDB vector store for tourist attractions."""

import logging

import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings

from app.config import settings as app_settings

logger = logging.getLogger(__name__)


class TouristAttractionVectorStore:
    """Vector store for semantic search of tourist attractions."""

    def __init__(self, persist_directory: str = "chroma_db"):
        """Initialize ChromaDB vector store.

        Args:
            persist_directory: Directory to persist ChromaDB data
        """
        self.persist_directory = persist_directory
        self.collection_name = "tourist_attractions"

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=app_settings.OPENAI_API_KEY,
        )

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"Created new collection: {self.collection_name}")

    def add_attractions(self, attractions: list[dict]) -> None:
        """Add tourist attractions to vector store.

        Args:
            attractions: List of attraction dictionaries from TouristAttraction model
        """
        if not attractions:
            logger.warning("No attractions to add")
            return

        documents = []
        metadatas = []
        ids = []

        for attraction in attractions:
            # Create rich text description for embedding
            doc = self._create_document(attraction)
            documents.append(doc)

            # Store metadata
            metadatas.append({
                "id": str(attraction["id"]),
                "name": attraction["name"],
                "category": attraction["category"],
                "address": attraction.get("address", ""),
                "latitude": str(attraction["latitude"]),
                "longitude": str(attraction["longitude"]),
            })

            ids.append(f"attraction_{attraction['id']}")

        # Generate embeddings and add to collection
        try:
            embeddings_list = self.embeddings.embed_documents(documents)

            self.collection.add(
                documents=documents,
                embeddings=embeddings_list,
                metadatas=metadatas,
                ids=ids,
            )

            logger.info(f"Added {len(attractions)} attractions to vector store")

        except Exception as e:
            logger.error(f"Failed to add attractions to vector store: {e}")
            raise

    def search_attractions(
        self,
        query: str,
        n_results: int = 5,
        filter_dict: dict = None,
    ) -> list[tuple[dict, float]]:
        """Search for attractions using semantic similarity.

        Args:
            query: Search query (e.g., "역사적인 궁궐", "자연과 산책")
            n_results: Number of results to return
            filter_dict: Optional metadata filters

        Returns:
            List of (attraction_metadata, similarity_score) tuples
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query)

            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_dict,
            )

            # Format results
            attractions = []
            if results["metadatas"] and results["distances"]:
                for metadata, distance in zip(
                    results["metadatas"][0], results["distances"][0]
                ):
                    # Convert cosine distance to similarity score (0-1)
                    similarity = 1 - distance
                    attractions.append((metadata, similarity))

            logger.info(
                f"Found {len(attractions)} attractions for query: '{query[:50]}...'"
            )
            return attractions

        except Exception as e:
            logger.error(f"Failed to search attractions: {e}")
            return []

    def _create_document(self, attraction: dict) -> str:
        """Create rich text document for embedding.

        Args:
            attraction: Attraction dictionary

        Returns:
            Rich text description
        """
        parts = []

        # Name and category
        parts.append(f"이름: {attraction['name']}")
        parts.append(f"구분: {attraction['category']}")

        # Description
        if attraction.get("description"):
            parts.append(f"설명: {attraction['description']}")

        # Address
        if attraction.get("address"):
            parts.append(f"위치: {attraction['address']}")

        # Facilities (if available)
        facilities = []
        if attraction.get("public_facilities"):
            facilities.append(attraction["public_facilities"])
        if attraction.get("cultural_facilities"):
            facilities.append(attraction["cultural_facilities"])
        if facilities:
            parts.append(f"시설: {', '.join(facilities)}")

        return " | ".join(parts)

    def count(self) -> int:
        """Get count of attractions in vector store."""
        return self.collection.count()

    def reset(self) -> None:
        """Reset the collection (delete all data)."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(f"Reset collection: {self.collection_name}")
