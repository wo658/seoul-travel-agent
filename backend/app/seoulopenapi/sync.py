"""Data synchronization script for Seoul Open API to database with ChromaDB."""

import asyncio
import logging
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.seoulopenapi.client import SeoulOpenAPIClient
from app.venue.embedding_service import EmbeddingService
from app.venue.models import Venue
from app.venue.vector_store import VenueVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VenueSyncService:
    """Service for synchronizing venue data from Seoul Open API with ChromaDB."""

    # Category mapping configuration
    CATEGORY_MAPPINGS = {
        "nature": {
            "id_field": "POST_SN",
            "name_field": "POST_SJ",
            "common_fields": {
                "address": "ADDRESS",
                "new_address": "NEW_ADDRESS",
                "phone": "CMMN_TELNO",
                "website": "CMMN_HMPG_URL",
                "operating_hours": "CMMN_USE_TIME",
                "subway_info": "SUBWAY_INFO",
                "x_coord": "X_COORD",
                "y_coord": "Y_COORD",
            },
            "extra_fields": {
                "introduction": "CMMN_INTRCN_CN",
            },
            "business_status": "영업중",
        },
        "restaurant": {
            "id_field": "POST_SN",
            "name_field": "POST_SJ",
            "common_fields": {
                "address": "ADDRESS",
                "new_address": "NEW_ADDRESS",
                "phone": "CMMN_TELNO",
                "website": "CMMN_HMPG_URL",
                "operating_hours": "CMMN_USE_TIME",
                "subway_info": "SUBWAY_INFO",
                "x_coord": "X_COORD",
                "y_coord": "Y_COORD",
            },
            "extra_fields": {
                "representative_menu": "FD_REPRSNT_MENU",
            },
            "business_status": "영업중",
        },
        "attraction": {
            "id_field": "POST_SN",
            "name_field": "POST_SJ",
            "common_fields": {
                "address": "ADDRESS",
                "new_address": "NEW_ADDRESS",
                "phone": "CMMN_TELNO",
                "website": "CMMN_HMPG_URL",
                "operating_hours": "CMMN_USE_TIME",
                "subway_info": "SUBWAY_INFO",
                "x_coord": "X_COORD",
                "y_coord": "Y_COORD",
            },
            "extra_fields": {
                "introduction": "CMMN_INTRCN_CN",
                "tags": "TAG",
                "accessibility": "BF_DESC",
            },
            "business_status": "영업중",
        },
        "accommodation": {
            "id_field": "MGTNO",
            "name_field": "BPLCNM",
            "common_fields": {
                "address": "SITEWHLADDR",
                "new_address": "RDNWHLADDR",
                "phone": "SITETEL",
                "x_coord": "X",
                "y_coord": "Y",
            },
            "extra_fields": {
                "room_count": "STROOMCNT",
                "facilities": "AFC",
                "accommodation_type": "TRSTLODGCLNM",
            },
            "business_status_field": "TRDSTATENM",
        },
    }

    def __init__(self, db: Session, api_key: str, chroma_persist_dir: str = "./chroma_db"):
        """Initialize sync service.

        Args:
            db: Database session
            api_key: Seoul Open API key
            chroma_persist_dir: ChromaDB persistence directory
        """
        self.db = db
        self.api_client = SeoulOpenAPIClient(api_key)
        self.embedding_service = EmbeddingService()
        self.vector_store = VenueVectorStore(persist_directory=chroma_persist_dir)

    def _convert_to_venue(self, category: str, data: Dict[str, Any]) -> Venue:
        """Convert API data to Venue model using category mapping.

        Args:
            category: Venue category (nature, restaurant, attraction, accommodation)
            data: Raw API data

        Returns:
            Venue object
        """
        mapping = self.CATEGORY_MAPPINGS[category]

        # Build common fields
        venue_data = {
            "external_id": f"{category}_{data[mapping['id_field']]}",
            "name": data[mapping["name_field"]],
            "category": category,
        }

        # Map common fields
        for venue_field, api_field in mapping["common_fields"].items():
            venue_data[venue_field] = data.get(api_field)

        # Handle business status
        if "business_status_field" in mapping:
            venue_data["business_status"] = data.get(mapping["business_status_field"], "")
        else:
            venue_data["business_status"] = mapping["business_status"]

        # Build extra_info
        extra_info = {}
        for extra_field, api_field in mapping["extra_fields"].items():
            value = data.get(api_field)
            if value is not None:
                extra_info[extra_field] = value

        venue_data["extra_info"] = extra_info

        return Venue(**venue_data)

    async def sync_venues_with_embeddings(
        self, max_records_per_category: int = 100
    ) -> Dict[str, int]:
        """Sync all venues from Seoul Open API with ChromaDB embeddings.

        Args:
            max_records_per_category: Maximum records to fetch per category

        Returns:
            Dictionary with counts per category
        """
        stats = {
            "nature": 0,
            "restaurant": 0,
            "attraction": 0,
            "accommodation": 0,
            "total": 0,
            "errors": 0,
        }

        try:
            # Fetch all categories
            logger.info("Fetching nature sites...")
            nature_data = await self.api_client.fetch_nature_sites(
                max_records=max_records_per_category
            )

            logger.info("Fetching restaurants...")
            restaurant_data = await self.api_client.fetch_restaurants(
                max_records=max_records_per_category
            )

            logger.info("Fetching attractions...")
            attraction_data = await self.api_client.fetch_attractions(
                max_records=max_records_per_category
            )

            logger.info("Fetching accommodations...")
            accommodation_data = await self.api_client.fetch_accommodations(
                max_records=max_records_per_category
            )

            # Convert to Venue objects using unified converter
            venues: List[Venue] = []

            # Process each category
            categories_data = [
                ("nature", nature_data),
                ("restaurant", restaurant_data),
                ("attraction", attraction_data),
                ("accommodation", accommodation_data),
            ]

            for category, data_list in categories_data:
                for data in data_list:
                    try:
                        venue = self._convert_to_venue(category, data)

                        # Filter accommodations by business status
                        if category == "accommodation" and venue.business_status != "영업중":
                            continue

                        venues.append(venue)
                        stats[category] += 1
                    except Exception as e:
                        logger.error(f"Error converting {category} data: {e}")
                        stats["errors"] += 1

            logger.info(f"Total venues to process: {len(venues)}")

            # Generate embeddings in smaller batches to avoid API limits
            logger.info("Generating embeddings in batches...")
            batch_size = 500  # Process 500 venues at a time
            all_embeddings = []

            for i in range(0, len(venues), batch_size):
                batch_venues = venues[i:i + batch_size]
                descriptions = [
                    self.embedding_service.format_venue_description(venue)
                    for venue in batch_venues
                ]

                logger.info(f"Processing batch {i//batch_size + 1}/{(len(venues) + batch_size - 1)//batch_size} ({len(batch_venues)} venues)...")
                batch_embeddings = await self.embedding_service.batch_generate_embeddings(
                    descriptions
                )
                all_embeddings.extend(batch_embeddings)

            embeddings = all_embeddings
            logger.info(f"Generated {len(embeddings)} embeddings total")

            # Save to database first to get IDs
            logger.info("Saving venues to database...")
            venue_ids = []
            external_ids = []
            metadatas = []

            for venue, embedding in zip(venues, embeddings):
                # Check if venue already exists
                existing = (
                    self.db.query(Venue)
                    .filter(Venue.external_id == venue.external_id)
                    .first()
                )

                if existing:
                    # Update existing venue
                    for key, value in venue.__dict__.items():
                        if key != "_sa_instance_state" and key != "id":
                            setattr(existing, key, value)
                    self.db.flush()
                    venue_id = existing.id
                else:
                    # Add new venue
                    self.db.add(venue)
                    self.db.flush()
                    venue_id = venue.id

                # Collect data for ChromaDB
                venue_ids.append(venue_id)
                external_ids.append(venue.external_id)
                metadatas.append({
                    "name": venue.name,
                    "category": venue.category,
                    "address": venue.new_address or venue.address or "",
                })

            self.db.commit()

            # Store embeddings in ChromaDB in batches
            logger.info("Storing embeddings in ChromaDB...")
            chroma_batch_size = 5000  # ChromaDB max batch size limit
            for i in range(0, len(venue_ids), chroma_batch_size):
                batch_end = min(i + chroma_batch_size, len(venue_ids))
                logger.info(f"Storing ChromaDB batch {i//chroma_batch_size + 1}/{(len(venue_ids) + chroma_batch_size - 1)//chroma_batch_size} ({batch_end - i} venues)...")

                self.vector_store.add_venue_embeddings_batch(
                    venue_ids=venue_ids[i:batch_end],
                    external_ids=external_ids[i:batch_end],
                    embeddings=embeddings[i:batch_end],
                    metadatas=metadatas[i:batch_end],
                )

            stats["total"] = len(venues)

            logger.info(f"Sync completed! Stats: {stats}")

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            self.db.rollback()
            raise

        finally:
            await self.api_client.close()

        return stats


async def main():
    """Main function to run venue synchronization."""
    # Check if API key is configured
    if not settings.SEOUL_OPENAPI_KEY:
        logger.error(
            "SEOUL_OPENAPI_KEY is not configured. Please set it in .env file."
        )
        return

    if not settings.OPENAI_API_KEY:
        logger.error(
            "OPENAI_API_KEY is not configured. Please set it in .env file."
        )
        return

    # Create database session
    db = SessionLocal()

    try:
        # Initialize sync service
        sync_service = VenueSyncService(db, settings.SEOUL_OPENAPI_KEY)

        # Run synchronization (fetch all records)
        logger.info("Starting venue synchronization (all records)...")
        stats = await sync_service.sync_venues_with_embeddings(
            max_records_per_category=10000  # High limit to fetch all available data
        )

        logger.info("Synchronization completed successfully!")
        logger.info(f"Final stats: {stats}")

    except Exception as e:
        logger.error(f"Synchronization failed: {e}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
