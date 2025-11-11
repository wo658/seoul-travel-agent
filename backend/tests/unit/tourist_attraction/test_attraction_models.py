"""Test TouristAttraction domain models."""



class TestTouristAttractionModel:
    """Test TouristAttraction model."""

    def test_create_tourist_attraction(self, test_db_session):
        """Test creating a tourist attraction."""
        from app.tourist_attraction.models import TouristAttraction

        attraction = TouristAttraction(
            name="경복궁",
            category="관광지",
            road_address="서울특별시 종로구 사직로 161",
            latitude=37.578840,
            longitude=126.977000,
            phone="02-3700-3900",
            introduction="조선시대 궁궐",
        )
        test_db_session.add(attraction)
        test_db_session.commit()
        test_db_session.refresh(attraction)

        assert attraction.id is not None
        assert attraction.name == "경복궁"
        assert attraction.category == "관광지"
        assert attraction.latitude == 37.578840
        assert attraction.longitude == 126.977000
        assert attraction.created_at is not None

    def test_tourist_attraction_with_facilities(self, test_db_session):
        """Test tourist attraction with facility information."""
        from app.tourist_attraction.models import TouristAttraction

        attraction = TouristAttraction(
            name="남산공원",
            category="관광지",
            latitude=37.551168,
            longitude=126.988227,
            public_facilities="화장실, 주차장",
            cultural_facilities="전망대",
        )
        test_db_session.add(attraction)
        test_db_session.commit()
        test_db_session.refresh(attraction)

        assert attraction.public_facilities == "화장실, 주차장"
        assert attraction.cultural_facilities == "전망대"
