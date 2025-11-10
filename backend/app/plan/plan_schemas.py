"""Plan domain schemas."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel


# ============================================================================
# Planner Agent Response Schemas (Frontend compatibility)
# ============================================================================


class PlannerActivity(BaseModel):
    """Activity in a day's itinerary."""

    time: str  # HH:MM format
    venue_name: str
    venue_type: Literal["attraction", "restaurant", "accommodation", "cafe", "shopping"]
    duration_minutes: int
    estimated_cost: int
    notes: Optional[str] = None


class PlannerDayItinerary(BaseModel):
    """Single day itinerary."""

    day: int
    date: str  # YYYY-MM-DD
    theme: str
    activities: List[PlannerActivity]
    daily_cost: int


class PlannerAccommodation(BaseModel):
    """Accommodation information."""

    name: str
    cost_per_night: int
    total_nights: int


class PlannerPlanCreate(BaseModel):
    """Schema for creating a plan from Planner Agent response."""

    title: str
    total_days: int
    total_cost: int
    itinerary: List[PlannerDayItinerary]
    accommodation: Optional[PlannerAccommodation] = None
    summary: Optional[str] = None


# ============================================================================
# TravelPlan CRUD Schemas
# ============================================================================


class TravelPlanCreate(BaseModel):
    """Travel plan creation schema."""

    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TravelPlanUpdate(BaseModel):
    """Travel plan update schema."""

    title: Optional[str] = None
    description: Optional[str] = None
    itinerary: Optional[dict] = None
    recommendations: Optional[dict] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TravelPlanResponse(BaseModel):
    """Travel plan response schema."""

    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    itinerary: Optional[dict] = None
    recommendations: Optional[dict] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
