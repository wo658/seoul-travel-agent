"""Planner agent state schema."""

from operator import add
from typing import Annotated, TypedDict


class PlanningState(TypedDict):
    """State schema for travel planning agent."""

    # User input
    user_request: str
    dates: tuple[str, str]  # (start_date, end_date)
    budget: int
    interests: list[str]

    # Vector search results (SEO-33 integration)
    attractions: list[dict]
    restaurants: list[dict]
    accommodations: list[dict]

    # Generated plan
    travel_plan: dict | None

    # Metadata
    attempts: int
    errors: Annotated[list[str], add]  # Reducer pattern for accumulating errors
