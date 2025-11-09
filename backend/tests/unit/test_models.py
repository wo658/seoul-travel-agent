"""Test database models."""

import pytest
from datetime import datetime


class TestUserModel:
    """Test User model."""

    def test_create_user(self, test_db_session):
        """Test creating a user."""
        from app.auth.models import User

        user = User(
            email="unique_test@example.com",  # Use unique email
            username="uniquetestuser",
            hashed_password="hashed_password_here",
        )
        test_db_session.add(user)
        test_db_session.commit()
        test_db_session.refresh(user)

        assert user.id is not None
        assert user.email == "unique_test@example.com"
        assert user.username == "uniquetestuser"
        # SQLite stores boolean as integer (1 for True)
        assert user.is_active == 1
        assert user.created_at is not None

    def test_user_relationships(self, test_db_session, mock_user, mock_travel_plan):
        """Test user relationships with travel plans."""
        assert len(mock_user.plans) == 1
        assert mock_user.plans[0].id == mock_travel_plan.id


class TestTravelPlanModel:
    """Test TravelPlan model."""

    def test_create_travel_plan(self, test_db_session, mock_user):
        """Test creating a travel plan."""
        from app.plan.models import TravelPlan

        plan = TravelPlan(
            user_id=mock_user.id,
            title="Seoul Adventure",
            description="3-day Seoul trip",
            itinerary={"days": []},
            recommendations={"restaurants": [], "attractions": []},
        )
        test_db_session.add(plan)
        test_db_session.commit()
        test_db_session.refresh(plan)

        assert plan.id is not None
        assert plan.user_id == mock_user.id
        assert plan.title == "Seoul Adventure"
        assert plan.description == "3-day Seoul trip"
        assert plan.created_at is not None
        assert plan.updated_at is not None

    def test_travel_plan_with_dates(self, test_db_session, mock_user):
        """Test travel plan with start and end dates."""
        from app.plan.models import TravelPlan

        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 1, 3)

        plan = TravelPlan(
            user_id=mock_user.id,
            title="New Year Trip",
            start_date=start_date,
            end_date=end_date,
        )
        test_db_session.add(plan)
        test_db_session.commit()
        test_db_session.refresh(plan)

        assert plan.start_date == start_date
        assert plan.end_date == end_date

    def test_travel_plan_user_relationship(self, test_db_session, mock_travel_plan, mock_user):
        """Test travel plan relationship with user."""
        assert mock_travel_plan.user.id == mock_user.id
        assert mock_travel_plan.user.email == mock_user.email


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
