#!/usr/bin/env python3
"""Check tourist attractions data in database."""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.database import SessionLocal
from app.tourist_attraction.models import TouristAttraction

def check_database():
    """Check database for tourist attractions."""
    print("=" * 70)
    print("Database Tourist Attractions Check")
    print("=" * 70)

    db = SessionLocal()

    try:
        # Get all attractions
        attractions = db.query(TouristAttraction).all()
        print(f"\n✅ Found {len(attractions)} attractions in database\n")

        # Group by category
        categories = {}
        for attr in attractions:
            category = attr.category or "Unknown"
            if category not in categories:
                categories[category] = []
            categories[category].append(attr.name)

        print("Categories breakdown:")
        for category, names in sorted(categories.items()):
            print(f"\n  [{category}] ({len(names)} items):")
            for name in names[:5]:  # Show first 5
                print(f"    - {name}")
            if len(names) > 5:
                print(f"    ... and {len(names) - 5} more")

        # Check for restaurants specifically
        print("\n" + "=" * 70)
        print("Searching for restaurants/food venues...")
        print("=" * 70)

        restaurant_keywords = ["식당", "음식", "맛집", "카페", "레스토랑", "restaurant", "cafe"]
        found_restaurants = []

        for attr in attractions:
            attr_text = f"{attr.name} {attr.category or ''} {attr.introduction or ''}".lower()
            if any(keyword in attr_text for keyword in restaurant_keywords):
                found_restaurants.append(attr)

        if found_restaurants:
            print(f"\n✅ Found {len(found_restaurants)} potential restaurants:")
            for r in found_restaurants[:10]:
                print(f"  - {r.name} ({r.category})")
        else:
            print("\n⚠️  No restaurants found in database!")
            print("   The dataset appears to contain only tourist attractions, not restaurants.")

        # Check for accommodations
        print("\n" + "=" * 70)
        print("Searching for accommodations...")
        print("=" * 70)

        accommodation_keywords = ["숙박", "호텔", "게스트", "펜션", "hotel", "accommodation"]
        found_accommodations = []

        for attr in attractions:
            attr_text = f"{attr.name} {attr.category or ''} {attr.introduction or ''}".lower()
            if any(keyword in attr_text for keyword in accommodation_keywords):
                found_accommodations.append(attr)

        if found_accommodations:
            print(f"\n✅ Found {len(found_accommodations)} potential accommodations:")
            for a in found_accommodations[:10]:
                print(f"  - {a.name} ({a.category})")
        else:
            print("\n⚠️  No accommodations found in database!")
            print("   The dataset appears to contain only tourist attractions.")

    finally:
        db.close()

if __name__ == "__main__":
    check_database()
