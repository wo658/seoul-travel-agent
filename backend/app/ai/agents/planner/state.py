"""Planner agent state schema."""

from operator import add
from typing import Annotated, TypedDict


class PlanningState(TypedDict, total=False):
    """State schema for travel planning agent.

    Note: total=False means all fields are optional by default.
    This matches the runtime behavior where fields can be None or missing.
    """

    # User input
    user_request: str | None
    dates: tuple[str, str] | None  # (start_date, end_date)
    budget: int | None
    interests: list[str] | None

    # Vector search results (SEO-33 integration)
    attractions: list[dict] | None
    restaurants: list[dict] | None
    accommodations: list[dict] | None

    # Generated plan
    travel_plan: dict | None

    # Metadata
    attempts: int
    errors: Annotated[list[str], add]  # Reducer pattern for accumulating errors
