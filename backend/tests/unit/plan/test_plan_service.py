"""Unit tests for Plan Service layer."""

from datetime import datetime


class TestPlanServiceCreate:
    """Test plan creation from Planner Agent response."""

    def test_create_plan_from_planner_response(self, test_db_session, mock_user):
        """Test creating plan from PlannerPlan structure."""
        from app.plan import plan_service

        # Planner Agent 응답 구조 (frontend PlannerPlan 타입 기반)
        planner_data = {
            "title": "3일 서울 여행",
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
            "summary": "서울의 역사와 문화를 체험하는 3일 일정"
        }

        plan = plan_service.create_plan(
            db=test_db_session,
            user_id=mock_user.id,
            planner_data=planner_data
        )

        assert plan.id is not None
        assert plan.user_id == mock_user.id
        assert plan.title == "3일 서울 여행"
        assert plan.description == "서울의 역사와 문화를 체험하는 3일 일정"
        assert plan.itinerary is not None
        assert isinstance(plan.itinerary, dict)
        assert plan.created_at is not None

    def test_create_plan_extracts_dates_from_itinerary(self, test_db_session, mock_user):
        """Test automatic date extraction from itinerary."""
        from app.plan import plan_service

        planner_data = {
            "title": "주말 서울 여행",
            "total_days": 2,
            "total_cost": 200000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-02-01",
                    "theme": "첫날",
                    "activities": [],
                    "daily_cost": 100000
                },
                {
                    "day": 2,
                    "date": "2025-02-02",
                    "theme": "둘째날",
                    "activities": [],
                    "daily_cost": 100000
                }
            ]
        }

        plan = plan_service.create_plan(
            db=test_db_session,
            user_id=mock_user.id,
            planner_data=planner_data
        )

        # start_date는 첫날, end_date는 마지막날
        assert plan.start_date is not None
        assert plan.end_date is not None
        assert plan.start_date.date() == datetime(2025, 2, 1).date()
        assert plan.end_date.date() == datetime(2025, 2, 2).date()

    def test_create_plan_stores_json_fields_correctly(self, test_db_session, mock_user):
        """Test JSON field storage (itinerary, recommendations)."""
        from app.plan import plan_service

        planner_data = {
            "title": "테스트 플랜",
            "total_days": 1,
            "total_cost": 50000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-03-01",
                    "theme": "테스트",
                    "activities": [
                        {
                            "time": "14:00",
                            "venue_name": "남산타워",
                            "venue_type": "attraction",
                            "duration_minutes": 90,
                            "estimated_cost": 15000,
                            "notes": "서울 전망"
                        }
                    ],
                    "daily_cost": 50000
                }
            ],
            "accommodation": {
                "name": "게스트하우스",
                "cost_per_night": 40000,
                "total_nights": 1
            }
        }

        plan = plan_service.create_plan(
            db=test_db_session,
            user_id=mock_user.id,
            planner_data=planner_data
        )

        # itinerary JSON 구조 검증
        assert "total_days" in plan.itinerary
        assert "days" in plan.itinerary
        assert len(plan.itinerary["days"]) == 1
        assert plan.itinerary["days"][0]["day"] == 1
        assert plan.itinerary["days"][0]["activities"][0]["venue_name"] == "남산타워"

        # recommendations JSON 구조 검증
        assert "accommodation" in plan.recommendations
        assert plan.recommendations["accommodation"]["name"] == "게스트하우스"

    def test_create_plan_without_optional_fields(self, test_db_session, mock_user):
        """Test creating plan without optional fields (accommodation, summary)."""
        from app.plan import plan_service

        planner_data = {
            "title": "간단한 플랜",
            "total_days": 1,
            "total_cost": 30000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-04-01",
                    "theme": "당일치기",
                    "activities": [],
                    "daily_cost": 30000
                }
            ]
        }

        plan = plan_service.create_plan(
            db=test_db_session,
            user_id=mock_user.id,
            planner_data=planner_data
        )

        assert plan.id is not None
        assert plan.title == "간단한 플랜"
        assert plan.description is None or plan.description == ""


class TestPlanServiceRead:
    """Test plan retrieval operations."""

    def test_get_plan_by_id(self, test_db_session, mock_travel_plan):
        """Test retrieving a plan by ID."""
        from app.plan import plan_service

        plan = plan_service.get_plan(
            db=test_db_session,
            plan_id=mock_travel_plan.id
        )

        assert plan is not None
        assert plan.id == mock_travel_plan.id
        assert plan.title == mock_travel_plan.title

    def test_get_plan_not_found(self, test_db_session):
        """Test retrieving non-existent plan returns None."""
        from app.plan import plan_service

        plan = plan_service.get_plan(
            db=test_db_session,
            plan_id=99999
        )

        assert plan is None

    def test_list_plans_by_user(self, test_db_session, mock_user, mock_travel_plan):
        """Test listing plans for a specific user."""
        from app.plan import plan_service
        from app.plan.models import TravelPlan

        # 추가 플랜 생성
        plan2 = TravelPlan(
            user_id=mock_user.id,
            title="두 번째 플랜",
            description="또 다른 여행"
        )
        test_db_session.add(plan2)
        test_db_session.commit()

        plans = plan_service.list_plans(
            db=test_db_session,
            user_id=mock_user.id
        )

        assert len(plans) == 2
        assert all(p.user_id == mock_user.id for p in plans)

    def test_list_plans_empty_for_new_user(self, test_db_session):
        """Test listing plans returns empty list for user with no plans."""
        from app.auth.models import User
        from app.plan import plan_service

        # 플랜이 없는 새 사용자
        new_user = User(
            email="newuser@example.com",
            username="newuser",
            hashed_password="hash"
        )
        test_db_session.add(new_user)
        test_db_session.commit()
        test_db_session.refresh(new_user)

        plans = plan_service.list_plans(
            db=test_db_session,
            user_id=new_user.id
        )

        assert len(plans) == 0
        assert isinstance(plans, list)

    def test_list_plans_filters_by_user(self, test_db_session, mock_user):
        """Test that list_plans only returns plans for specified user."""
        from app.auth.models import User
        from app.plan import plan_service
        from app.plan.models import TravelPlan

        # 다른 사용자와 플랜 생성
        other_user = User(
            email="other@example.com",
            username="otheruser",
            hashed_password="hash"
        )
        test_db_session.add(other_user)
        test_db_session.commit()
        test_db_session.refresh(other_user)

        other_plan = TravelPlan(
            user_id=other_user.id,
            title="다른 사람 플랜"
        )
        test_db_session.add(other_plan)
        test_db_session.commit()

        # mock_user의 플랜만 조회되어야 함
        plans = plan_service.list_plans(
            db=test_db_session,
            user_id=mock_user.id
        )

        assert all(p.user_id == mock_user.id for p in plans)
        assert not any(p.user_id == other_user.id for p in plans)


class TestPlanServiceUpdate:
    """Test plan update operations."""

    def test_update_plan_title_and_description(self, test_db_session, mock_travel_plan):
        """Test updating basic fields."""
        from app.plan import plan_service

        update_data = {
            "title": "수정된 제목",
            "description": "수정된 설명"
        }

        updated_plan = plan_service.update_plan(
            db=test_db_session,
            plan_id=mock_travel_plan.id,
            update_data=update_data
        )

        assert updated_plan.id == mock_travel_plan.id
        assert updated_plan.title == "수정된 제목"
        assert updated_plan.description == "수정된 설명"
        assert updated_plan.updated_at > updated_plan.created_at

    def test_update_plan_itinerary(self, test_db_session, mock_travel_plan):
        """Test updating itinerary JSON field."""
        from app.plan import plan_service

        new_itinerary = {
            "days": [
                {
                    "day": 1,
                    "date": "2025-05-01",
                    "activities": [
                        {
                            "time": "11:00",
                            "activity": "New Activity",
                            "duration": 60
                        }
                    ]
                }
            ]
        }

        update_data = {"itinerary": new_itinerary}

        updated_plan = plan_service.update_plan(
            db=test_db_session,
            plan_id=mock_travel_plan.id,
            update_data=update_data
        )

        assert updated_plan.itinerary["days"][0]["activities"][0]["activity"] == "New Activity"

    def test_update_plan_partial_fields(self, test_db_session, mock_travel_plan):
        """Test updating only some fields (others should remain unchanged)."""
        from app.plan import plan_service

        original_title = mock_travel_plan.title
        original_itinerary = mock_travel_plan.itinerary

        update_data = {"description": "새로운 설명만 변경"}

        updated_plan = plan_service.update_plan(
            db=test_db_session,
            plan_id=mock_travel_plan.id,
            update_data=update_data
        )

        # 변경된 필드
        assert updated_plan.description == "새로운 설명만 변경"
        # 변경 안 된 필드
        assert updated_plan.title == original_title
        assert updated_plan.itinerary == original_itinerary

    def test_update_plan_not_found(self, test_db_session):
        """Test updating non-existent plan returns None."""
        from app.plan import plan_service

        update_data = {"title": "존재하지 않는 플랜"}

        updated_plan = plan_service.update_plan(
            db=test_db_session,
            plan_id=99999,
            update_data=update_data
        )

        assert updated_plan is None


class TestPlanServiceDelete:
    """Test plan deletion operations."""

    def test_delete_plan(self, test_db_session, mock_travel_plan):
        """Test deleting a plan."""
        from app.plan import plan_service

        plan_id = mock_travel_plan.id

        result = plan_service.delete_plan(
            db=test_db_session,
            plan_id=plan_id
        )

        assert result is True

        # 삭제 확인
        deleted_plan = plan_service.get_plan(
            db=test_db_session,
            plan_id=plan_id
        )
        assert deleted_plan is None

    def test_delete_nonexistent_plan(self, test_db_session):
        """Test deleting non-existent plan returns False."""
        from app.plan import plan_service

        result = plan_service.delete_plan(
            db=test_db_session,
            plan_id=99999
        )

        assert result is False
