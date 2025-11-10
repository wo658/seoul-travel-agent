"""Unit tests for Plan Schemas."""

import pytest
from datetime import datetime
from pydantic import ValidationError


class TestPlannerPlanSchema:
    """Test PlannerPlan schema validation."""

    def test_planner_plan_schema_validation(self):
        """Test that PlannerPlan schema validates correctly."""
        from app.plan.plan_schemas import PlannerPlanCreate

        planner_data = {
            "title": "서울 3일 여행",
            "total_days": 3,
            "total_cost": 500000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-01-15",
                    "theme": "역사 탐방",
                    "activities": [
                        {
                            "time": "10:00",
                            "venue_name": "경복궁",
                            "venue_type": "attraction",
                            "duration_minutes": 120,
                            "estimated_cost": 3000,
                            "notes": "조선시대 궁궐"
                        }
                    ],
                    "daily_cost": 50000
                }
            ],
            "accommodation": {
                "name": "서울 호텔",
                "cost_per_night": 80000,
                "total_nights": 3
            },
            "summary": "서울의 역사와 문화 체험"
        }

        plan = PlannerPlanCreate(**planner_data)

        assert plan.title == "서울 3일 여행"
        assert plan.total_days == 3
        assert plan.total_cost == 500000
        assert len(plan.itinerary) == 1
        assert plan.itinerary[0].day == 1
        assert plan.summary == "서울의 역사와 문화 체험"

    def test_planner_plan_without_optional_fields(self):
        """Test PlannerPlan schema with only required fields."""
        from app.plan.plan_schemas import PlannerPlanCreate

        minimal_data = {
            "title": "간단한 플랜",
            "total_days": 1,
            "total_cost": 50000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-02-01",
                    "theme": "당일치기",
                    "activities": [],
                    "daily_cost": 50000
                }
            ]
        }

        plan = PlannerPlanCreate(**minimal_data)

        assert plan.title == "간단한 플랜"
        assert plan.accommodation is None
        assert plan.summary is None

    def test_planner_activity_schema_validation(self):
        """Test Activity structure validation."""
        from app.plan.plan_schemas import PlannerActivity

        activity_data = {
            "time": "14:30",
            "venue_name": "남산타워",
            "venue_type": "attraction",
            "duration_minutes": 90,
            "estimated_cost": 15000,
            "notes": "서울 전망대"
        }

        activity = PlannerActivity(**activity_data)

        assert activity.time == "14:30"
        assert activity.venue_name == "남산타워"
        assert activity.venue_type == "attraction"
        assert activity.duration_minutes == 90
        assert activity.estimated_cost == 15000

    def test_planner_activity_valid_venue_types(self):
        """Test that only valid venue_types are accepted."""
        from app.plan.plan_schemas import PlannerActivity

        valid_types = ["attraction", "restaurant", "accommodation", "cafe", "shopping"]

        for venue_type in valid_types:
            activity_data = {
                "time": "10:00",
                "venue_name": "테스트 장소",
                "venue_type": venue_type,
                "duration_minutes": 60,
                "estimated_cost": 10000
            }
            activity = PlannerActivity(**activity_data)
            assert activity.venue_type == venue_type

    def test_planner_day_itinerary_schema(self):
        """Test DayItinerary structure validation."""
        from app.plan.plan_schemas import PlannerDayItinerary

        day_data = {
            "day": 1,
            "date": "2025-03-01",
            "theme": "문화 체험",
            "activities": [
                {
                    "time": "09:00",
                    "venue_name": "박물관",
                    "venue_type": "attraction",
                    "duration_minutes": 120,
                    "estimated_cost": 5000
                }
            ],
            "daily_cost": 50000
        }

        day = PlannerDayItinerary(**day_data)

        assert day.day == 1
        assert day.date == "2025-03-01"
        assert day.theme == "문화 체험"
        assert len(day.activities) == 1
        assert day.daily_cost == 50000


class TestPlannerToTravelPlanConversion:
    """Test conversion from PlannerPlan to TravelPlan."""

    def test_planner_to_travel_plan_conversion(self):
        """Test converting PlannerPlan schema to TravelPlan model data."""
        from app.plan.plan_schemas import PlannerPlanCreate
        from app.plan import plan_service

        planner_data = {
            "title": "변환 테스트",
            "total_days": 2,
            "total_cost": 200000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-04-01",
                    "theme": "첫날",
                    "activities": [],
                    "daily_cost": 100000
                },
                {
                    "day": 2,
                    "date": "2025-04-02",
                    "theme": "둘째날",
                    "activities": [],
                    "daily_cost": 100000
                }
            ],
            "summary": "2일 여행 계획"
        }

        planner_plan = PlannerPlanCreate(**planner_data)

        # 변환 함수 테스트 (plan_service 내부 유틸리티 함수 가정)
        converted = plan_service._convert_planner_to_travel_plan_data(planner_plan)

        assert converted["title"] == "변환 테스트"
        assert converted["description"] == "2일 여행 계획"
        assert "itinerary" in converted
        assert converted["itinerary"]["total_days"] == 2
        assert len(converted["itinerary"]["days"]) == 2

    def test_activity_structure_mapping(self):
        """Test that Activity fields are correctly mapped."""
        from app.plan.plan_schemas import PlannerActivity

        frontend_activity = {
            "time": "15:00",
            "venue_name": "카페",
            "venue_type": "cafe",
            "duration_minutes": 45,
            "estimated_cost": 8000,
            "notes": "휴식 시간"
        }

        activity = PlannerActivity(**frontend_activity)

        # Backend JSON 구조로 변환 확인
        activity_dict = activity.model_dump()

        assert "time" in activity_dict
        assert "venue_name" in activity_dict
        assert "venue_type" in activity_dict
        assert "duration_minutes" in activity_dict
        assert "estimated_cost" in activity_dict
        assert activity_dict["estimated_cost"] == 8000  # Backend uses estimated_cost

    def test_accommodation_mapping(self):
        """Test accommodation data mapping."""
        from app.plan.plan_schemas import PlannerAccommodation

        accommodation_data = {
            "name": "호텔 서울",
            "cost_per_night": 100000,
            "total_nights": 3
        }

        accommodation = PlannerAccommodation(**accommodation_data)

        assert accommodation.name == "호텔 서울"
        assert accommodation.cost_per_night == 100000
        assert accommodation.total_nights == 3

    def test_date_extraction_logic(self):
        """Test logic for extracting start_date and end_date from itinerary."""
        from app.plan import plan_service

        itinerary_data = [
            {"day": 1, "date": "2025-05-10", "theme": "첫날", "activities": [], "daily_cost": 50000},
            {"day": 2, "date": "2025-05-11", "theme": "둘째날", "activities": [], "daily_cost": 60000},
            {"day": 3, "date": "2025-05-12", "theme": "셋째날", "activities": [], "daily_cost": 70000}
        ]

        start_date, end_date = plan_service._extract_dates_from_itinerary(itinerary_data)

        assert start_date.date() == datetime(2025, 5, 10).date()
        assert end_date.date() == datetime(2025, 5, 12).date()


class TestTravelPlanCreateSchema:
    """Test TravelPlanCreate schema."""

    def test_travel_plan_create_basic_fields(self):
        """Test basic field validation."""
        from app.plan.plan_schemas import TravelPlanCreate

        plan_data = {
            "title": "새로운 여행",
            "description": "여행 설명"
        }

        plan = TravelPlanCreate(**plan_data)

        assert plan.title == "새로운 여행"
        assert plan.description == "여행 설명"

    def test_travel_plan_create_with_dates(self):
        """Test with start and end dates."""
        from app.plan.plan_schemas import TravelPlanCreate

        plan_data = {
            "title": "날짜 있는 여행",
            "start_date": datetime(2025, 6, 1),
            "end_date": datetime(2025, 6, 5)
        }

        plan = TravelPlanCreate(**plan_data)

        assert plan.start_date == datetime(2025, 6, 1)
        assert plan.end_date == datetime(2025, 6, 5)


class TestTravelPlanUpdateSchema:
    """Test TravelPlanUpdate schema."""

    def test_travel_plan_update_partial(self):
        """Test that all fields are optional."""
        from app.plan.plan_schemas import TravelPlanUpdate

        # 일부 필드만 제공
        update_data = {"title": "수정된 제목"}

        plan = TravelPlanUpdate(**update_data)

        assert plan.title == "수정된 제목"
        assert plan.description is None
        assert plan.itinerary is None

    def test_travel_plan_update_json_fields(self):
        """Test updating JSON fields."""
        from app.plan.plan_schemas import TravelPlanUpdate

        update_data = {
            "itinerary": {"days": []},
            "recommendations": {"tips": ["팁1", "팁2"]}
        }

        plan = TravelPlanUpdate(**update_data)

        assert plan.itinerary == {"days": []}
        assert plan.recommendations == {"tips": ["팁1", "팁2"]}


class TestTravelPlanResponseSchema:
    """Test TravelPlanResponse schema."""

    def test_travel_plan_response_from_orm(self, test_db_session, mock_travel_plan):
        """Test creating response from ORM model."""
        from app.plan.plan_schemas import TravelPlanResponse

        response = TravelPlanResponse.model_validate(mock_travel_plan)

        assert response.id == mock_travel_plan.id
        assert response.user_id == mock_travel_plan.user_id
        assert response.title == mock_travel_plan.title
        assert response.created_at is not None
        assert response.updated_at is not None
