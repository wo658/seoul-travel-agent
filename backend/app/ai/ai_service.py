"""AI service - LangGraph agent orchestration for travel planning."""

import logging

logger = logging.getLogger(__name__)


class AIService:
    """AI service for LangGraph-based travel planning agents.

    This service orchestrates two specialized agents:
    - Planner Agent: Generates initial travel plans
    - Reviewer Agent: Reviews and modifies plans based on user feedback
    """

    def _create_initial_planning_state(
        self,
        user_request: str,
        dates: tuple[str, str],
        budget: int,
        interests: list[str],
    ) -> dict:
        """Create initial planning state."""
        return {
            "user_request": user_request,
            "dates": dates,
            "budget": budget,
            "interests": interests,
            "attractions": [],
            "restaurants": [],
            "accommodations": [],
            "travel_plan": None,
            "attempts": 0,
            "errors": [],
        }

    async def generate_initial_plan(
        self,
        user_request: str,
        dates: tuple[str, str],
        budget: int,
        interests: list[str],
    ) -> dict:
        """Generate initial travel plan using Planner Agent.

        Args:
            user_request: User's travel request description
            dates: Tuple of (start_date, end_date) in YYYY-MM-DD format
            budget: Budget amount in KRW
            interests: List of user interests

        Returns:
            Generated travel plan as dict

        Raises:
            ValueError: If plan generation fails after max attempts
        """
        logger.info("Starting plan generation")

        from app.ai.agents.planner import planner_graph

        initial_state = self._create_initial_planning_state(
            user_request, dates, budget, interests
        )

        final_state = await planner_graph.ainvoke(initial_state)

        if final_state.get("errors"):
            error_msg = f"Plan generation failed: {'; '.join(final_state['errors'])}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        if not final_state.get("travel_plan"):
            logger.error("No plan generated")
            raise ValueError("No plan generated")

        logger.info("Plan generation successful")
        return final_state["travel_plan"]

    async def review_and_modify_plan(
        self,
        original_plan: dict,
        user_feedback: str,
        iteration: int = 0,
    ) -> dict:
        """Review and modify travel plan using Reviewer Agent.

        Args:
            original_plan: Original travel plan from Planner
            user_feedback: User's feedback on the plan
            iteration: Current iteration number (default: 0)

        Returns:
            Modified plan or original plan based on feedback type

        Raises:
            ValueError: If rejection requires new plan generation
        """
        from app.ai.agents.reviewer import ReviewState, reviewer_graph

        review_state: ReviewState = {
            "original_plan": original_plan,
            "user_feedback": user_feedback,
            "feedback_type": None,
            "target_section": None,
            "modified_plan": None,
            "iteration": iteration,
            "max_iterations": 3,
        }

        final_state = await reviewer_graph.ainvoke(review_state)

        feedback_type = final_state.get("feedback_type")

        if feedback_type == "reject":
            raise ValueError(
                "User rejected the plan. Please generate a new plan with updated requirements."
            )
        elif feedback_type == "approve":
            return original_plan
        else:  # modify
            return final_state.get("modified_plan", original_plan)


ai_service = AIService()
