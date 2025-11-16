#!/usr/bin/env python3
"""Check ChromaDB vector store status."""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.tourist_attraction.vector_store import TouristAttractionVectorStore

def check_vector_store():
    """Check vector store status and perform test search."""
    print("=" * 70)
    print("ChromaDB Vector Store Status Check")
    print("=" * 70)

    try:
        # Initialize vector store
        print("\n[1] Initializing vector store...")
        vector_store = TouristAttractionVectorStore(
            persist_directory=str(backend_dir / "chroma_db")
        )

        # Check count
        print("\n[2] Checking data count...")
        count = vector_store.count()
        print(f"✅ Vector store contains {count} attractions")

        if count == 0:
            print("⚠️  WARNING: Vector store is empty!")
            return False

        # Test search
        print("\n[3] Testing search functionality...")
        test_queries = [
            "역사적인 궁궐",
            "자연과 산책",
            "음식점 맛집",
        ]

        for query in test_queries:
            print(f"\n  Query: '{query}'")
            results = vector_store.search_attractions(query, n_results=3)

            if not results:
                print(f"    ⚠️  No results found!")
            else:
                for idx, (metadata, score) in enumerate(results, 1):
                    print(f"    {idx}. {metadata['name']} (similarity: {score:.3f})")

        print("\n" + "=" * 70)
        print("✅ Vector store is working correctly!")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_vector_store()
    sys.exit(0 if success else 1)
