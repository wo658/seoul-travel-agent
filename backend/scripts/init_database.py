#!/usr/bin/env python3
"""Initialize all databases (SQLite + ChromaDB) for Seoul Travel Agent.

This script:
1. Removes existing databases
2. Creates fresh SQLite database with tourist attraction data
3. Builds ChromaDB vector store from the data

Usage:
    python scripts/init_database.py
"""

import logging
import shutil
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print formatted header."""
    logger.info("=" * 80)
    logger.info(f"  {title}")
    logger.info("=" * 80)


def clean_databases():
    """Remove existing database files."""
    logger.info("\n[Step 1] Cleaning existing databases...")

    files_to_remove = [
        backend_dir / "seoul_travel.db",
        backend_dir / "data" / "seoul_travel.db",
        backend_dir / "app.db",
    ]

    dirs_to_remove = [
        backend_dir / "chroma_db",
    ]

    removed_count = 0

    # Remove database files
    for file_path in files_to_remove:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"  ✓ Removed: {file_path.relative_to(backend_dir)}")
            removed_count += 1

    # Remove directories
    for dir_path in dirs_to_remove:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            logger.info(f"  ✓ Removed: {dir_path.relative_to(backend_dir)}/")
            removed_count += 1

    if removed_count == 0:
        logger.info("  ✓ No existing databases found (clean slate)")
    else:
        logger.info(f"  ✓ Cleaned {removed_count} items")


def import_attractions():
    """Import tourist attractions to SQLite database."""
    logger.info("\n[Step 2] Importing tourist attractions to SQLite...")

    # Import here to avoid early database connection
    from scripts.import_tourist_attractions import import_attractions

    try:
        import_attractions()
        return True
    except Exception as e:
        logger.error(f"  ✗ Failed to import attractions: {e}")
        return False


def build_vector_store():
    """Build ChromaDB vector store."""
    logger.info("\n[Step 3] Building ChromaDB vector store...")

    # Import here to avoid early database connection
    from scripts.build_vector_store import build_vector_store

    try:
        return build_vector_store()
    except Exception as e:
        logger.error(f"  ✗ Failed to build vector store: {e}")
        return False


def main():
    """Main initialization process."""
    print_header("Seoul Travel Agent - Database Initialization")

    # Step 1: Clean existing databases
    clean_databases()

    # Step 2: Import tourist attractions
    if not import_attractions():
        logger.error("\n❌ Database initialization failed at Step 2")
        return False

    # Step 3: Build vector store
    if not build_vector_store():
        logger.error("\n❌ Database initialization failed at Step 3")
        return False

    # Success
    print_header("✅ Database Initialization Complete!")
    logger.info("\nYou can now start the backend server:")
    logger.info("  uvicorn app.main:app --reload --port 8000")
    logger.info("\nOr use the Makefile:")
    logger.info("  make webapp")
    logger.info("")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
