"""Test Plan domain models."""

import pytest
from datetime import datetime


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

    def test_travel_plan_json_fields(self, test_db_session, mock_user):
        """Test storing JSON data in itinerary and recommendations."""
        from app.plan.models import TravelPlan

        itinerary_data = {
            "total_days": 3,
            "days": [
                {
                    "day": 1,
                    "date": "2025-01-15",
                    "theme": "역사",
                    "activities": [
                        {
                            "time": "10:00",
                            "venue_name": "경복궁",
                            "duration_minutes": 120
                        }
                    ],
                    "daily_cost": 50000
                }
            ]
        }

        recommendations_data = {
            "accommodation": {
                "name": "호텔",
                "cost_per_night": 80000
            },
            "tips": ["팁1", "팁2"]
        }

        plan = TravelPlan(
            user_id=mock_user.id,
            title="JSON 테스트",
            itinerary=itinerary_data,
            recommendations=recommendations_data
        )
        test_db_session.add(plan)
        test_db_session.commit()
        test_db_session.refresh(plan)

        assert plan.itinerary["total_days"] == 3
        assert len(plan.itinerary["days"]) == 1
        assert plan.recommendations["accommodation"]["name"] == "호텔"
        assert len(plan.recommendations["tips"]) == 2
