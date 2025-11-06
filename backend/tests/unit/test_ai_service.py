"""Test AI service."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestAIService:
    """Test AIService class."""

    @pytest.fixture
    def ai_service(self):
        """Get AI service instance."""
        from app.ai.ai_service import AIService

        return AIService()

    def test_ai_service_instantiation(self, ai_service):
        """Test that AI service can be instantiated."""
        assert ai_service is not None

    @pytest.mark.asyncio
    async def test_generate_initial_plan_structure(self, ai_service):
        """Test generate_initial_plan method signature."""
        # Test that the method exists and has the correct signature
        assert hasattr(ai_service, "generate_initial_plan")
        assert callable(ai_service.generate_initial_plan)

    @pytest.mark.asyncio
    async def test_review_and_modify_plan_structure(self, ai_service):
        """Test review_and_modify_plan method signature."""
        # Test that the method exists and has the correct signature
        assert hasattr(ai_service, "review_and_modify_plan")
        assert callable(ai_service.review_and_modify_plan)

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.planner_graph")
    async def test_generate_initial_plan_success(self, mock_planner_graph, ai_service):
        """Test successful plan generation."""
        # Mock successful plan generation
        mock_plan = {
            "title": "Seoul Adventure",
            "days": [
                {
                    "day": 1,
                    "date": "2025-01-01",
                    "activities": [],
                }
            ],
        }

        mock_planner_graph.ainvoke = AsyncMock(
            return_value={
                "travel_plan": mock_plan,
                "errors": [],
            }
        )

        result = await ai_service.generate_initial_plan(
            user_request="Plan a 3-day trip to Seoul",
            dates=("2025-01-01", "2025-01-03"),
            budget=1000000,
            interests=["culture", "food"],
        )

        assert result == mock_plan
        mock_planner_graph.ainvoke.assert_called_once()

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.planner_graph")
    async def test_generate_initial_plan_with_errors(self, mock_planner_graph, ai_service):
        """Test plan generation with errors."""
        # Mock plan generation with errors
        mock_planner_graph.ainvoke = AsyncMock(
            return_value={
                "travel_plan": None,
                "errors": ["Failed to generate plan"],
            }
        )

        with pytest.raises(ValueError, match="Plan generation failed"):
            await ai_service.generate_initial_plan(
                user_request="Plan a trip",
                dates=("2025-01-01", "2025-01-03"),
                budget=1000000,
                interests=["culture"],
            )

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.planner_graph")
    async def test_generate_initial_plan_no_plan(self, mock_planner_graph, ai_service):
        """Test plan generation when no plan is returned."""
        # Mock plan generation returning no plan
        mock_planner_graph.ainvoke = AsyncMock(
            return_value={
                "travel_plan": None,
                "errors": [],
            }
        )

        with pytest.raises(ValueError, match="No plan generated"):
            await ai_service.generate_initial_plan(
                user_request="Plan a trip",
                dates=("2025-01-01", "2025-01-03"),
                budget=1000000,
                interests=["culture"],
            )

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.reviewer_graph")
    async def test_review_and_modify_plan_approve(self, mock_reviewer_graph, ai_service):
        """Test plan review with approval."""
        original_plan = {"title": "Original Plan", "days": []}

        mock_reviewer_graph.ainvoke = AsyncMock(
            return_value={
                "feedback_type": "approve",
                "modified_plan": None,
            }
        )

        result = await ai_service.review_and_modify_plan(
            original_plan=original_plan,
            user_feedback="Looks great!",
        )

        assert result == original_plan

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.reviewer_graph")
    async def test_review_and_modify_plan_reject(self, mock_reviewer_graph, ai_service):
        """Test plan review with rejection."""
        original_plan = {"title": "Original Plan", "days": []}

        mock_reviewer_graph.ainvoke = AsyncMock(
            return_value={
                "feedback_type": "reject",
                "modified_plan": None,
            }
        )

        with pytest.raises(ValueError, match="User rejected the plan"):
            await ai_service.review_and_modify_plan(
                original_plan=original_plan,
                user_feedback="Not what I wanted",
            )

    @pytest.mark.asyncio
    @patch("app.ai.ai_service.reviewer_graph")
    async def test_review_and_modify_plan_modify(self, mock_reviewer_graph, ai_service):
        """Test plan review with modification."""
        original_plan = {"title": "Original Plan", "days": []}
        modified_plan = {"title": "Modified Plan", "days": [{"day": 1}]}

        mock_reviewer_graph.ainvoke = AsyncMock(
            return_value={
                "feedback_type": "modify",
                "modified_plan": modified_plan,
            }
        )

        result = await ai_service.review_and_modify_plan(
            original_plan=original_plan,
            user_feedback="Add more activities",
        )

        assert result == modified_plan
