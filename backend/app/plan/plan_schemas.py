"""Plan domain schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# ============================================================================
# Planner Agent Response Schemas (Frontend compatibility)
# ============================================================================


class PlannerActivity(BaseModel):
    """Activity in a day's itinerary."""

    time: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$", description="Time in HH:MM format")
    venue_name: str = Field(..., min_length=1, max_length=200, description="Name of the venue")
    venue_type: Literal["attraction", "restaurant", "accommodation", "cafe", "shopping"]
    duration_minutes: int = Field(..., gt=0, le=1440, description="Duration in minutes (max 24 hours)")
    estimated_cost: int = Field(..., ge=0, description="Estimated cost in KRW")
    notes: str | None = Field(None, max_length=1000, description="Additional notes")


class PlannerDayItinerary(BaseModel):
    """Single day itinerary."""

    day: int = Field(..., gt=0, description="Day number (starts from 1)")
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date in YYYY-MM-DD format")
    theme: str = Field(..., min_length=1, max_length=200, description="Theme for the day")
    activities: list[PlannerActivity] = Field(default_factory=list, description="List of activities")
    daily_cost: int = Field(..., ge=0, description="Total cost for the day in KRW")


class PlannerAccommodation(BaseModel):
    """Accommodation information."""

    name: str = Field(..., min_length=1, max_length=200, description="Accommodation name")
    cost_per_night: int = Field(..., gt=0, description="Cost per night in KRW")
    total_nights: int = Field(..., gt=0, description="Total number of nights")


class PlannerPlanCreate(BaseModel):
    """Schema for creating a plan from Planner Agent response."""

    title: str = Field(..., min_length=1, max_length=200, description="Plan title")
    total_days: int = Field(..., gt=0, le=30, description="Total number of days (max 30)")
    total_cost: int = Field(..., ge=0, description="Total estimated cost in KRW")
    itinerary: list[PlannerDayItinerary] = Field(..., min_length=1, description="Daily itinerary (at least 1 day)")
    accommodation: PlannerAccommodation | None = Field(None, description="Accommodation information")
    summary: str | None = Field(None, max_length=1000, description="Plan summary")

    @field_validator("itinerary")
    @classmethod
    def validate_itinerary_days(cls, v: list[PlannerDayItinerary]) -> list[PlannerDayItinerary]:
        """Validate that itinerary days are sequential."""
        if not v:
            raise ValueError("Itinerary must have at least one day")

        # Check if days are sequential starting from 1
        expected_day = 1
        for day_itinerary in v:
            if day_itinerary.day != expected_day:
                raise ValueError(f"Expected day {expected_day}, but got day {day_itinerary.day}")
            expected_day += 1

        return v


# ============================================================================
# TravelPlan CRUD Schemas
# ============================================================================


class TravelPlanCreate(BaseModel):
    """Travel plan creation schema."""

    title: str = Field(..., min_length=1, max_length=200, description="Plan title")
    description: str | None = Field(None, max_length=2000, description="Plan description")
    start_date: datetime | None = Field(None, description="Start date of the trip")
    end_date: datetime | None = Field(None, description="End date of the trip")


class TravelPlanUpdate(BaseModel):
    """Travel plan update schema."""

    title: str | None = Field(None, min_length=1, max_length=200, description="Plan title")
    description: str | None = Field(None, max_length=2000, description="Plan description")
    itinerary: dict | None = Field(None, description="Updated itinerary")
    recommendations: dict | None = Field(None, description="Updated recommendations")
    start_date: datetime | None = Field(None, description="Start date of the trip")
    end_date: datetime | None = Field(None, description="End date of the trip")


class TravelPlanResponse(BaseModel):
    """Travel plan response schema."""

    id: int
    user_id: int
    title: str
    description: str | None = None
    itinerary: dict | None = None
    recommendations: dict | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
