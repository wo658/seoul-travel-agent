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

    def _convert_nature_to_venue(self, data: Dict[str, Any]) -> Venue:
        """Convert nature API data to Venue model."""
        return Venue(
            external_id=f"nature_{data['POST_SN']}",
            name=data["POST_SJ"],
            category="nature",
            address=data.get("ADDRESS"),
            new_address=data.get("NEW_ADDRESS"),
            phone=data.get("CMMN_TELNO"),
            website=data.get("CMMN_HMPG_URL"),
            operating_hours=data.get("CMMN_USE_TIME"),
            subway_info=data.get("SUBWAY_INFO"),
            x_coord=data.get("X_COORD"),
            y_coord=data.get("Y_COORD"),
            business_status="영업중",  # Assume active if in API
            extra_info={
                "introduction": data.get("CMMN_INTRCN_CN"),
            },
        )

    def _convert_restaurant_to_venue(self, data: Dict[str, Any]) -> Venue:
        """Convert restaurant API data to Venue model."""
        return Venue(
            external_id=f"restaurant_{data['POST_SN']}",
            name=data["POST_SJ"],
            category="restaurant",
            address=data.get("ADDRESS"),
            new_address=data.get("NEW_ADDRESS"),
            phone=data.get("CMMN_TELNO"),
            website=data.get("CMMN_HMPG_URL"),
            operating_hours=data.get("CMMN_USE_TIME"),
            subway_info=data.get("SUBWAY_INFO"),
            x_coord=data.get("X_COORD"),
            y_coord=data.get("Y_COORD"),
            business_status="영업중",
            extra_info={
                "representative_menu": data.get("FD_REPRSNT_MENU"),
            },
        )

    def _convert_attraction_to_venue(self, data: Dict[str, Any]) -> Venue:
        """Convert attraction API data to Venue model."""
        return Venue(
            external_id=f"attraction_{data['POST_SN']}",
            name=data["POST_SJ"],
            category="attraction",
            address=data.get("ADDRESS"),
            new_address=data.get("NEW_ADDRESS"),
            phone=data.get("CMMN_TELNO"),
            website=data.get("CMMN_HMPG_URL"),
            operating_hours=data.get("CMMN_USE_TIME"),
            subway_info=data.get("SUBWAY_INFO"),
            x_coord=data.get("X_COORD"),
            y_coord=data.get("Y_COORD"),
            business_status="영업중",
            extra_info={
                "introduction": data.get("CMMN_INTRCN_CN"),
                "tags": data.get("TAG"),
                "accessibility": data.get("BF_DESC"),
            },
        )

    def _convert_accommodation_to_venue(self, data: Dict[str, Any]) -> Venue:
        """Convert accommodation API data to Venue model."""
        # Filter by business status
        business_status = data.get("TRDSTATENM", "")

        return Venue(
            external_id=f"accommodation_{data['MGTNO']}",
            name=data["BPLCNM"],
            category="accommodation",
            address=data.get("SITEWHLADDR"),
            new_address=data.get("RDNWHLADDR"),
            phone=data.get("SITETEL"),
            x_coord=data.get("X"),
            y_coord=data.get("Y"),
            business_status=business_status,
            extra_info={
                "room_count": data.get("STROOMCNT"),
                "facilities": data.get("AFC"),
                "accommodation_type": data.get("TRSTLODGCLNM"),
            },
        )

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

            # Convert to Venue objects
            venues: List[Venue] = []

            for data in nature_data:
                try:
                    venue = self._convert_nature_to_venue(data)
                    venues.append(venue)
                    stats["nature"] += 1
                except Exception as e:
                    logger.error(f"Error converting nature data: {e}")
                    stats["errors"] += 1

            for data in restaurant_data:
                try:
                    venue = self._convert_restaurant_to_venue(data)
                    venues.append(venue)
                    stats["restaurant"] += 1
                except Exception as e:
                    logger.error(f"Error converting restaurant data: {e}")
                    stats["errors"] += 1

            for data in attraction_data:
                try:
                    venue = self._convert_attraction_to_venue(data)
                    venues.append(venue)
                    stats["attraction"] += 1
                except Exception as e:
                    logger.error(f"Error converting attraction data: {e}")
                    stats["errors"] += 1

            for data in accommodation_data:
                try:
                    venue = self._convert_accommodation_to_venue(data)
                    # Only include active accommodations
                    if venue.business_status == "영업중":
                        venues.append(venue)
                        stats["accommodation"] += 1
                except Exception as e:
                    logger.error(f"Error converting accommodation data: {e}")
                    stats["errors"] += 1

            logger.info(f"Total venues to process: {len(venues)}")

            # Generate embeddings in batch
            logger.info("Generating embeddings...")
            descriptions = [
                self.embedding_service.format_venue_description(venue)
                for venue in venues
            ]

            embeddings = await self.embedding_service.batch_generate_embeddings(
                descriptions
            )

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

            # Store embeddings in ChromaDB
            logger.info("Storing embeddings in ChromaDB...")
            self.vector_store.add_venue_embeddings_batch(
                venue_ids=venue_ids,
                external_ids=external_ids,
                embeddings=embeddings,
                metadatas=metadatas,
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

        # Run synchronization (limit to 100 records per category for testing)
        logger.info("Starting venue synchronization...")
        stats = await sync_service.sync_venues_with_embeddings(
            max_records_per_category=100
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
