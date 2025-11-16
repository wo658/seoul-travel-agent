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
    modification_type: str | None  # "restaurant", "attraction", "accommodation", "budget", "time", "general"

    # Context data (fetched based on modification needs)
    attractions: list[dict]  # New attraction options from vector search
    restaurants: list[dict]  # New restaurant options from Naver API
    accommodations: list[dict]  # New accommodation options from Naver API

    # Output
    modified_plan: dict | None

    # Metadata
    iteration: int
    max_iterations: int  # Maximum 3 iterations
