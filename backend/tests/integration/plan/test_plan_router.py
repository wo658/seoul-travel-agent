"""Integration tests for Plan Router endpoints."""

import pytest
from datetime import datetime


class TestPlanRouterCreate:
    """Test POST /plans endpoint."""

    def test_create_plan_endpoint(self, client, test_db_session, mock_user):
        """Test creating a plan via API."""
        plan_data = {
            "title": "API 테스트 플랜",
            "total_days": 2,
            "total_cost": 150000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-07-01",
                    "theme": "첫날",
                    "activities": [
                        {
                            "time": "10:00",
                            "venue_name": "경복궁",
                            "venue_type": "attraction",
                            "duration_minutes": 120,
                            "estimated_cost": 3000
                        }
                    ],
                    "daily_cost": 75000
                },
                {
                    "day": 2,
                    "date": "2025-07-02",
                    "theme": "둘째날",
                    "activities": [],
                    "daily_cost": 75000
                }
            ],
            "summary": "2일 서울 여행"
        }

        response = client.post(
            "/api/plans",
            json=plan_data,
            params={"user_id": mock_user.id}  # 임시: 나중에 인증으로 대체
        )

        if response.status_code != 201:
            print(f"Error response: {response.json()}")
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "API 테스트 플랜"
        assert data["user_id"] == mock_user.id
        assert data["id"] is not None
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_plan_with_minimal_data(self, client, test_db_session, mock_user):
        """Test creating plan with only required fields."""
        plan_data = {
            "title": "최소 데이터 플랜",
            "total_days": 1,
            "total_cost": 50000,
            "itinerary": [
                {
                    "day": 1,
                    "date": "2025-08-01",
                    "theme": "당일치기",
                    "activities": [],
                    "daily_cost": 50000
                }
            ]
        }

        response = client.post(
            "/api/plans",
            json=plan_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "최소 데이터 플랜"

    def test_create_plan_invalid_data(self, client, mock_user):
        """Test creating plan with invalid data returns 422."""
        invalid_data = {
            "title": "",  # Empty title
            "itinerary": []  # Empty itinerary
        }

        response = client.post(
            "/api/plans",
            json=invalid_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 422


class TestPlanRouterList:
    """Test GET /plans endpoint."""

    def test_list_plans_endpoint(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test listing all plans for a user."""
        response = client.get(
            "/api/plans",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(plan["user_id"] == mock_user.id for plan in data)

    def test_list_plans_empty(self, client, test_db_session):
        """Test listing plans for user with no plans."""
        from app.auth.models import User

        new_user = User(
            email="empty@example.com",
            username="emptyuser",
            hashed_password="hash"
        )
        test_db_session.add(new_user)
        test_db_session.commit()
        test_db_session.refresh(new_user)

        response = client.get(
            "/api/plans",
            params={"user_id": new_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_plans_filters_by_user(self, client, test_db_session, mock_user):
        """Test that list only returns plans for specified user."""
        from app.auth.models import User
        from app.plan.models import TravelPlan

        # Create another user with a plan
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
            title="다른 사용자 플랜"
        )
        test_db_session.add(other_plan)
        test_db_session.commit()

        response = client.get(
            "/api/plans",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert all(plan["user_id"] == mock_user.id for plan in data)


class TestPlanRouterGet:
    """Test GET /plans/{plan_id} endpoint."""

    def test_get_plan_endpoint(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test retrieving a specific plan."""
        response = client.get(
            f"/api/plans/{mock_travel_plan.id}",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_travel_plan.id
        assert data["title"] == mock_travel_plan.title
        assert data["user_id"] == mock_user.id

    def test_get_plan_not_found(self, client, mock_user):
        """Test retrieving non-existent plan returns 404."""
        response = client.get(
            "/api/plans/99999",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_get_plan_with_full_data(self, client, test_db_session, mock_user):
        """Test retrieving plan with itinerary and recommendations."""
        from app.plan.models import TravelPlan

        full_plan = TravelPlan(
            user_id=mock_user.id,
            title="전체 데이터 플랜",
            description="설명",
            itinerary={
                "total_days": 2,
                "days": [
                    {
                        "day": 1,
                        "date": "2025-09-01",
                        "activities": []
                    }
                ]
            },
            recommendations={
                "accommodation": {
                    "name": "호텔",
                    "cost_per_night": 80000
                }
            }
        )
        test_db_session.add(full_plan)
        test_db_session.commit()
        test_db_session.refresh(full_plan)

        response = client.get(
            f"/api/plans/{full_plan.id}",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["itinerary"] is not None
        assert data["recommendations"] is not None
        assert "accommodation" in data["recommendations"]


class TestPlanRouterUpdate:
    """Test PATCH /plans/{plan_id} endpoint."""

    def test_update_plan_endpoint(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test updating a plan."""
        update_data = {
            "title": "수정된 제목",
            "description": "수정된 설명"
        }

        response = client.patch(
            f"/api/plans/{mock_travel_plan.id}",
            json=update_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_travel_plan.id
        assert data["title"] == "수정된 제목"
        assert data["description"] == "수정된 설명"

    def test_update_plan_partial(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test updating only some fields."""
        original_title = mock_travel_plan.title

        update_data = {
            "description": "설명만 변경"
        }

        response = client.patch(
            f"/api/plans/{mock_travel_plan.id}",
            json=update_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "설명만 변경"
        # Title should remain unchanged
        assert data["title"] == original_title

    def test_update_plan_not_found(self, client, mock_user):
        """Test updating non-existent plan returns 404."""
        update_data = {"title": "존재하지 않는 플랜"}

        response = client.patch(
            "/api/plans/99999",
            json=update_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 404

    def test_update_plan_itinerary(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test updating itinerary field."""
        new_itinerary = {
            "total_days": 1,
            "days": [
                {
                    "day": 1,
                    "date": "2025-10-01",
                    "activities": [
                        {
                            "time": "14:00",
                            "venue_name": "새로운 장소"
                        }
                    ]
                }
            ]
        }

        update_data = {"itinerary": new_itinerary}

        response = client.patch(
            f"/api/plans/{mock_travel_plan.id}",
            json=update_data,
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["itinerary"]["days"][0]["activities"][0]["venue_name"] == "새로운 장소"


class TestPlanRouterDelete:
    """Test DELETE /plans/{plan_id} endpoint."""

    def test_delete_plan_endpoint(self, client, test_db_session, mock_user, mock_travel_plan):
        """Test deleting a plan."""
        plan_id = mock_travel_plan.id

        response = client.delete(
            f"/api/plans/{plan_id}",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

        # Verify plan is deleted
        get_response = client.get(
            f"/api/plans/{plan_id}",
            params={"user_id": mock_user.id}
        )
        assert get_response.status_code == 404

    def test_delete_plan_not_found(self, client, mock_user):
        """Test deleting non-existent plan returns 404."""
        response = client.delete(
            "/api/plans/99999",
            params={"user_id": mock_user.id}
        )

        assert response.status_code == 404

    def test_delete_plan_and_list(self, client, test_db_session, mock_user):
        """Test that deleted plan doesn't appear in list."""
        from app.plan.models import TravelPlan

        plan1 = TravelPlan(user_id=mock_user.id, title="플랜 1")
        plan2 = TravelPlan(user_id=mock_user.id, title="플랜 2")
        test_db_session.add_all([plan1, plan2])
        test_db_session.commit()
        test_db_session.refresh(plan1)
        test_db_session.refresh(plan2)

        # Delete plan1
        client.delete(f"/api/plans/{plan1.id}", params={"user_id": mock_user.id})

        # List should only have plan2
        response = client.get("/api/plans", params={"user_id": mock_user.id})
        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == plan2.id
