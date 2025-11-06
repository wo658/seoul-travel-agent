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


class TestVenueModel:
    """Test Venue model."""

    def test_create_venue(self, test_db_session):
        """Test creating a venue."""
        from app.venue.models import Venue

        venue = Venue(
            external_id="12345",
            category="attraction",
            name="Gyeongbokgung Palace",
            address="서울특별시 종로구",
            new_address="서울특별시 종로구 새주소",
            x_coord=127.0,
            y_coord=37.5,
            phone="02-123-4567",
            website="https://example.com",
            operating_hours="09:00-18:00",
            business_status="active",
        )
        test_db_session.add(venue)
        test_db_session.commit()
        test_db_session.refresh(venue)

        assert venue.id is not None
        assert venue.external_id == "12345"
        assert venue.category == "attraction"
        assert venue.name == "Gyeongbokgung Palace"
        assert venue.created_at is not None

    def test_venue_with_extra_info(self, test_db_session):
        """Test venue with extra info JSON."""
        from app.venue.models import Venue

        venue = Venue(
            external_id="67890",
            category="restaurant",
            name="Korean BBQ Restaurant",
            extra_info={"representative_menu": "갈비", "price_range": "30000-50000"},
        )
        test_db_session.add(venue)
        test_db_session.commit()
        test_db_session.refresh(venue)

        assert venue.extra_info["representative_menu"] == "갈비"
        assert venue.extra_info["price_range"] == "30000-50000"
