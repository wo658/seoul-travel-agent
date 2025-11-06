"""Reviewer agent state schema."""

from typing import TypedDict


class ReviewState(TypedDict):
    """State schema for plan review and modification agent."""

    # Input
    original_plan: dict  # Original plan from Planner
    user_feedback: str  # User feedback

    # Parsed results
    feedback_type: str | None  # "modify" | "approve" | "reject"
    target_section: str | None  # "day_1", "budget", "accommodation", etc.

    # Output
    modified_plan: dict | None

    # Metadata
    iteration: int
    max_iterations: int  # Maximum 3 iterations
