"""Build ChromaDB vector store for tourist attractions."""

import logging
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal
from app.tourist_attraction.models import TouristAttraction
from app.tourist_attraction.vector_store import TouristAttractionVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_vector_store():
    """Build vector store from tourist attractions in database."""
    logger.info("=" * 70)
    logger.info("Building Tourist Attraction Vector Store")
    logger.info("=" * 70)

    db = SessionLocal()

    try:
        # Step 1: Load attractions from database
        logger.info("\n[Step 1] Loading tourist attractions from database...")
        attractions = db.query(TouristAttraction).all()
        logger.info(f"Found {len(attractions)} attractions")

        if not attractions:
            logger.error("No attractions found in database!")
            return False

        # Step 2: Convert to dict format
        logger.info("\n[Step 2] Preparing attraction data...")
        attraction_dicts = []
        for attr in attractions:
            attraction_dicts.append({
                "id": attr.id,
                "name": attr.name,
                "category": attr.category,
                "description": attr.introduction or "",
                "address": attr.road_address or attr.jibun_address or "",
                "latitude": attr.latitude,
                "longitude": attr.longitude,
                "public_facilities": attr.public_facilities,
                "cultural_facilities": attr.cultural_facilities,
            })

        # Step 3: Initialize vector store
        logger.info("\n[Step 3] Initializing ChromaDB vector store...")
        vector_store = TouristAttractionVectorStore(persist_directory="chroma_db")

        # Reset existing data
        logger.info("Resetting existing vector store...")
        vector_store.reset()

        # Step 4: Add attractions to vector store
        logger.info("\n[Step 4] Generating embeddings and storing vectors...")
        logger.info("(This may take a minute...)")
        vector_store.add_attractions(attraction_dicts)

        # Step 5: Verify
        logger.info("\n[Step 5] Verifying vector store...")
        count = vector_store.count()
        logger.info(f"Vector store contains {count} attractions")

        if count != len(attractions):
            logger.warning(f"⚠️  Count mismatch: expected {len(attractions)}, got {count}")
            return False

        # Step 6: Test search
        logger.info("\n[Step 6] Testing semantic search...")
        test_queries = [
            "역사적인 궁궐과 왕실 유적",
            "자연과 산책을 즐길 수 있는 곳",
            "종교와 순교 역사",
        ]

        for query in test_queries:
            logger.info(f"\n  Query: '{query}'")
            results = vector_store.search_attractions(query, n_results=3)
            for idx, (metadata, score) in enumerate(results, 1):
                logger.info(f"    {idx}. {metadata['name']} (similarity: {score:.3f})")

        logger.info("\n" + "=" * 70)
        logger.info("✅ Vector store built successfully!")
        logger.info("=" * 70)
        return True

    except Exception as e:
        logger.error(f"❌ Failed to build vector store: {e}", exc_info=True)
        return False

    finally:
        db.close()


if __name__ == "__main__":
    success = build_vector_store()
    sys.exit(0 if success else 1)
