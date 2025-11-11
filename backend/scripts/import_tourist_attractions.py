"""Import Seoul tourist attractions from JSON data."""

import json
import logging
from pathlib import Path

# Import Base to create tables
from app.database import Base, SessionLocal, engine
from app.tourist_attraction.models import TouristAttraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def import_attractions():
    """Import tourist attractions from JSON file."""
    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Load JSON data
    data_path = Path(__file__).parent.parent / "data" / "서울관광지정보.json"
    logger.info(f"Loading data from {data_path}")

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    records = data["records"]
    logger.info(f"Found {len(records)} tourist attractions")

    # Create database session
    db = SessionLocal()

    try:
        imported_count = 0
        skipped_count = 0

        for record in records:
            try:
                # Parse coordinates
                latitude = float(record["위도"]) if record.get("위도") else None
                longitude = float(record["경도"]) if record.get("경도") else None

                # Skip if no coordinates
                if not latitude or not longitude:
                    logger.warning(f"Skipping {record['관광지명']}: No coordinates")
                    skipped_count += 1
                    continue

                # Parse capacity and parking
                try:
                    capacity = int(record["수용인원수"]) if record.get("수용인원수") else None
                except (ValueError, TypeError):
                    capacity = None

                try:
                    parking = int(record["주차가능수"]) if record.get("주차가능수") else None
                except (ValueError, TypeError):
                    parking = None

                # Create attraction instance
                attraction = TouristAttraction(
                    name=record["관광지명"],
                    category=record.get("관광지구분", "관광지"),
                    road_address=record.get("소재지도로명주소"),
                    jibun_address=record.get("소재지지번주소"),
                    latitude=latitude,
                    longitude=longitude,
                    area=record.get("면적"),
                    public_facilities=record.get("공공편익시설정보"),
                    accommodation_facilities=record.get("숙박시설정보"),
                    sports_facilities=record.get("운동및오락시설정보"),
                    cultural_facilities=record.get("휴양및문화시설정보"),
                    hospitality_facilities=record.get("접객시설정보"),
                    support_facilities=record.get("지원시설정보"),
                    capacity=capacity,
                    parking_spaces=parking,
                    introduction=record.get("관광지소개"),
                    phone=record.get("관리기관전화번호"),
                    manager_name=record.get("관리기관명"),
                    designated_date=record.get("지정일자"),
                    reference_date=record.get("데이터기준일자"),
                    provider_code=record.get("제공기관코드"),
                    provider_name=record.get("제공기관명"),
                )

                db.add(attraction)
                imported_count += 1

                if imported_count % 10 == 0:
                    logger.info(f"Imported {imported_count} attractions...")

            except Exception as e:
                logger.error(f"Error importing {record.get('관광지명', 'Unknown')}: {e}")
                skipped_count += 1
                continue

        # Commit all changes
        db.commit()
        logger.info("✅ Import completed!")
        logger.info(f"   Imported: {imported_count}")
        logger.info(f"   Skipped: {skipped_count}")

    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_attractions()
