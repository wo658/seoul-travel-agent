"""AI domain schemas."""

from pydantic import BaseModel


# Travel plan generation schemas
class GenerateTravelPlanRequest(BaseModel):
    """Request schema for generating travel plan."""

    user_request: str
    start_date: str  # YYYY-MM-DD
    end_date: str  # YYYY-MM-DD
    budget: int | None = None  # Amount in KRW (optional)
    interests: list[str] = []  # Optional, defaults to empty list


class TravelPlanResponse(BaseModel):
    """Response schema for travel plan."""

    plan_id: int | None = None  # Optional, for DB-backed plans
    plan: dict  # The actual travel plan JSON


class ReviewTravelPlanRequest(BaseModel):
    """Request schema for reviewing/modifying travel plan."""

    user_feedback: str
    iteration: int = 0
