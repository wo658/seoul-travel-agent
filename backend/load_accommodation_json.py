"""Load accommodation data from local JSON file."""

import asyncio
import json
import logging
from pathlib import Path

from app.config import settings
from app.database import SessionLocal
from app.venue.embedding_service import EmbeddingService
from app.venue.models import Venue
from app.venue.vector_store import VenueVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_json_to_venue(data: dict) -> Venue:
    """Convert JSON accommodation data to Venue model.

    Args:
        data: Raw JSON data from accommodation file

    Returns:
        Venue object
    """
    # Extract coordinates (convert from local coordinate system if needed)
    x_coord = None
    y_coord = None

    if data.get("x") and data.get("y"):
        try:
            # These are local coordinates, store them as-is
            x_coord = float(data["x"])
            y_coord = float(data["y"])
        except (ValueError, TypeError):
            pass

    # Extract phone number (clean up if needed)
    phone = data.get("sitetel", "")
    if phone and not phone.startswith("02-") and not phone.startswith("0"):
        phone = f"02-{phone}"  # Add Seoul area code if missing

    # Build venue data
    venue_data = {
        "external_id": f"accommodation_{data['mgtno']}",
        "name": data["bplcnm"],
        "category": "accommodation",
        "address": data.get("sitewhladdr") or "",
        "new_address": data.get("rdnwhladdr") or "",
        "postal_code": data.get("rdnpostno") or data.get("sitepostno") or "",
        "x_coord": x_coord,
        "y_coord": y_coord,
        "phone": phone if phone else None,
        "business_status": data.get("trdstatenm", ""),
        "extra_info": {
            "room_count": data.get("stroomcnt"),
            "facilities": data.get("afc"),
            "accommodation_type": data.get("trstlodgclnm"),
            "approval_date": data.get("apvpermymd"),
            "last_modified": data.get("lastmodts"),
        }
    }

    return Venue(**venue_data)


async def load_accommodations_from_json(
    json_path: str,
    db_session,
    embedding_service: EmbeddingService,
    vector_store: VenueVectorStore,
) -> dict:
    """Load accommodations from JSON file and store in DB + ChromaDB.

    Args:
        json_path: Path to JSON file
        db_session: Database session
        embedding_service: Embedding service
        vector_store: Vector store

    Returns:
        Statistics dictionary
    """
    stats = {
        "total_in_file": 0,
        "active_business": 0,
        "processed": 0,
        "errors": 0,
    }

    # Load JSON file
    logger.info(f"Loading accommodation data from {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    raw_data = json_data.get("DATA", [])
    stats["total_in_file"] = len(raw_data)
    logger.info(f"Found {stats['total_in_file']} accommodations in file")

    # Filter only active businesses
    active_data = [
        item for item in raw_data
        if item.get("trdstatenm") == "영업/정상"
    ]
    stats["active_business"] = len(active_data)
    logger.info(f"Filtered to {stats['active_business']} active businesses")

    # Convert to Venue objects
    venues = []
    for item in active_data:
        try:
            venue = convert_json_to_venue(item)
            venues.append(venue)
        except Exception as e:
            logger.error(f"Error converting accommodation: {e}")
            logger.error(f"Data: {item.get('bplcnm', 'unknown')}")
            stats["errors"] += 1

    if not venues:
        logger.warning("No venues to process!")
        return stats

    logger.info(f"Successfully converted {len(venues)} venues")

    # Generate embeddings in batches
    logger.info("Generating embeddings in batches...")
    batch_size = 500
    all_embeddings = []

    for i in range(0, len(venues), batch_size):
        batch_venues = venues[i:i + batch_size]
        descriptions = [
            embedding_service.format_venue_description(venue)
            for venue in batch_venues
        ]

        logger.info(f"Processing batch {i//batch_size + 1}/{(len(venues) + batch_size - 1)//batch_size} ({len(batch_venues)} venues)...")
        batch_embeddings = await embedding_service.batch_generate_embeddings(
            descriptions
        )
        all_embeddings.extend(batch_embeddings)

    embeddings = all_embeddings
    logger.info(f"Generated {len(embeddings)} embeddings total")

    # Save to database
    logger.info("Saving accommodations to database...")
    venue_ids = []
    external_ids = []
    metadatas = []

    for venue, embedding in zip(venues, embeddings):
        try:
            # Check if venue already exists
            existing = (
                db_session.query(Venue)
                .filter(Venue.external_id == venue.external_id)
                .first()
            )

            if existing:
                # Update existing venue
                for key, value in venue.__dict__.items():
                    if key != "_sa_instance_state" and key != "id":
                        setattr(existing, key, value)
                db_session.flush()
                venue_id = existing.id
                logger.info(f"Updated existing accommodation: {venue.name}")
            else:
                # Add new venue
                db_session.add(venue)
                db_session.flush()
                venue_id = venue.id
                logger.info(f"Added new accommodation: {venue.name}")

            # Collect data for ChromaDB
            venue_ids.append(venue_id)
            external_ids.append(venue.external_id)
            metadatas.append({
                "name": venue.name,
                "category": venue.category,
                "address": venue.new_address or venue.address or "",
            })

            stats["processed"] += 1

        except Exception as e:
            logger.error(f"Error saving venue {venue.name}: {e}")
            stats["errors"] += 1

    db_session.commit()
    logger.info(f"Saved {len(venue_ids)} accommodations to database")

    # Store embeddings in ChromaDB (handle existing venues)
    logger.info("Storing embeddings in ChromaDB...")

    # Check which venues already exist in ChromaDB
    existing_ids = set()
    try:
        all_results = vector_store.collection.get(include=[])
        existing_ids = set(int(id_str) for id_str in all_results["ids"])
        logger.info(f"Found {len(existing_ids)} existing venue IDs in ChromaDB")
    except Exception as e:
        logger.warning(f"Could not check existing IDs: {e}")

    # Filter new venues only
    new_venue_data = []
    update_count = 0

    for venue_id, external_id, embedding, metadata in zip(venue_ids, external_ids, embeddings, metadatas):
        if venue_id in existing_ids:
            # Delete existing then re-add (update)
            try:
                vector_store.delete_venue_embedding(venue_id)
                new_venue_data.append((venue_id, external_id, embedding, metadata))
                update_count += 1
            except Exception as e:
                logger.warning(f"Could not update venue {venue_id}: {e}")
        else:
            new_venue_data.append((venue_id, external_id, embedding, metadata))

    logger.info(f"Will add {len(new_venue_data)} venues ({update_count} updates, {len(new_venue_data) - update_count} new)")

    # Add in batches
    if new_venue_data:
        # Check for duplicates in the data to be added
        new_ids = [d[0] for d in new_venue_data]
        unique_check = set()
        duplicates = []
        for vid in new_ids:
            if vid in unique_check:
                duplicates.append(vid)
            unique_check.add(vid)

        if duplicates:
            logger.warning(f"Found {len(duplicates)} duplicate venue IDs in batch: {duplicates[:10]}")
            # Deduplicate by keeping last occurrence of each ID
            seen = {}
            for data in reversed(new_venue_data):
                if data[0] not in seen:
                    seen[data[0]] = data
            new_venue_data = list(reversed(list(seen.values())))
            logger.info(f"Deduplicated to {len(new_venue_data)} unique venues")

        chroma_batch_size = 5000
        new_ids = [d[0] for d in new_venue_data]
        new_external_ids = [d[1] for d in new_venue_data]
        new_embeddings = [d[2] for d in new_venue_data]
        new_metadatas = [d[3] for d in new_venue_data]

        for i in range(0, len(new_ids), chroma_batch_size):
            batch_end = min(i + chroma_batch_size, len(new_ids))
            logger.info(f"Storing ChromaDB batch {i//chroma_batch_size + 1}/{(len(new_ids) + chroma_batch_size - 1)//chroma_batch_size} ({batch_end - i} venues)...")

            vector_store.add_venue_embeddings_batch(
                venue_ids=new_ids[i:batch_end],
                external_ids=new_external_ids[i:batch_end],
                embeddings=new_embeddings[i:batch_end],
                metadatas=new_metadatas[i:batch_end],
            )

    logger.info("Accommodation loading completed!")
    return stats


async def main():
    """Main function to load accommodation data."""
    # Check if API key is configured
    if not settings.OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is not configured. Please set it in .env file.")
        return

    # Find JSON file
    json_path = Path("/Users/jhkim/seoul-travel-agent/서울시 관광숙박업 인허가 정보.json")

    if not json_path.exists():
        logger.error(f"JSON file not found: {json_path}")
        return

    # Create database session
    db = SessionLocal()

    try:
        # Initialize services
        embedding_service = EmbeddingService()
        vector_store = VenueVectorStore(persist_directory="./chroma_db")

        # Load accommodations
        stats = await load_accommodations_from_json(
            str(json_path),
            db,
            embedding_service,
            vector_store,
        )

        logger.info("=" * 60)
        logger.info("Accommodation Loading Statistics")
        logger.info("=" * 60)
        logger.info(f"Total in file: {stats['total_in_file']}")
        logger.info(f"Active businesses: {stats['active_business']}")
        logger.info(f"Successfully processed: {stats['processed']}")
        logger.info(f"Errors: {stats['errors']}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Loading failed: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
