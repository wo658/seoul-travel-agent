"""Verify venue data in SQLite and ChromaDB."""

import asyncio

from app.database import SessionLocal
from app.venue.models import Venue
from app.venue.vector_store import VenueVectorStore


async def main():
    """Verify venue data."""
    # Check SQLite
    print("=" * 60)
    print("SQLite Database Verification")
    print("=" * 60)

    db = SessionLocal()
    try:
        # Count venues by category
        total = db.query(Venue).count()
        print(f"\nTotal venues: {total}")

        for category in ["nature", "restaurant", "attraction", "accommodation"]:
            count = db.query(Venue).filter(Venue.category == category).count()
            print(f"  - {category}: {count}")

        # Sample venues
        print("\n" + "=" * 60)
        print("Sample Venues (first 3)")
        print("=" * 60)

        venues = db.query(Venue).limit(3).all()
        for venue in venues:
            print(f"\nID: {venue.id}")
            print(f"Name: {venue.name}")
            print(f"Category: {venue.category}")
            print(f"Address: {venue.new_address or venue.address}")
            print(f"Phone: {venue.phone}")
            if venue.extra_info:
                print(f"Extra Info: {venue.extra_info}")

    finally:
        db.close()

    # Check ChromaDB
    print("\n" + "=" * 60)
    print("ChromaDB Verification")
    print("=" * 60)

    vector_store = VenueVectorStore(persist_directory="./chroma_db")
    collection_size = vector_store.collection.count()
    print(f"\nChromaDB collection size: {collection_size}")

    if collection_size > 0:
        # Sample search
        print("\n" + "=" * 60)
        print("Sample Vector Search Test")
        print("=" * 60)

        from app.venue.embedding_service import EmbeddingService

        embedding_service = EmbeddingService()

        test_queries = [
            "공원",
            "한식당",
            "관광명소"
        ]

        for query in test_queries:
            print(f"\nQuery: '{query}'")

            # Generate query embedding
            query_embedding = await embedding_service.generate_query_embedding(query)

            # Search
            venue_ids, similarities, metadatas = vector_store.search_similar_venues(
                query_embedding=query_embedding,
                n_results=3
            )

            print(f"Top 3 results:")
            for i, (venue_id, similarity, metadata) in enumerate(zip(venue_ids, similarities, metadatas), 1):
                print(f"  {i}. {metadata.get('name')} "
                      f"({metadata.get('category')}) - "
                      f"similarity: {similarity:.3f}")

    print("\n" + "=" * 60)
    print("Verification Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
