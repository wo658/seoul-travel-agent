"""Pydantic models for planner agent structured outputs."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class TravelInfoExtraction(BaseModel):
    """Structured output for travel information extraction from user request.

    Example:
        dates: ('2025-01-10', '2025-01-15')
        budget: 500000
        interests: ['역사', '맛집', '쇼핑']
    """

    dates: Optional[tuple[str, str]] = Field(
        None,
        description="Start and end dates in YYYY-MM-DD format"
    )
    budget: Optional[int] = Field(
        None,
        description="Total budget in Korean Won (KRW)"
    )
    interests: Optional[list[str]] = Field(
        None,
        description="List of user interests or preferred activities"
    )


class Activity(BaseModel):
    """Single activity in the itinerary.

    Example:
        time: '09:00'
        venue_name: '경복궁'
        venue_type: 'attraction'
        duration_minutes: 120
        estimated_cost: 3000
        notes: '한복 대여 추천'
    """

    time: str = Field(description="Start time in HH:MM format")
    venue_name: str = Field(description="Name of the venue")
    venue_type: Literal["attraction", "restaurant", "accommodation"] = Field(
        description="Type of venue"
    )
    duration_minutes: int = Field(description="Duration in minutes", gt=0)
    estimated_cost: int = Field(description="Estimated cost in KRW", ge=0)
    notes: str = Field(default="", description="Brief notes or tips")


class DayItinerary(BaseModel):
    """Itinerary for a single day.

    Example:
        day: 1
        date: '2025-01-15'
        theme: '역사 탐방'
        activities: [Activity(...), Activity(...)]
        daily_cost: 50000
    """

    day: int = Field(description="Day number (1-indexed)", gt=0)
    date: str = Field(description="Actual date in YYYY-MM-DD format")
    theme: str = Field(description="Theme for the day")
    activities: list[Activity] = Field(description="List of activities for the day")
    daily_cost: int = Field(description="Total cost for the day in KRW", ge=0)


class AccommodationInfo(BaseModel):
    """Accommodation information.

    Example:
        name: '서울 호텔'
        cost_per_night: 80000
        total_nights: 2
    """

    name: str = Field(description="Hotel or accommodation name")
    cost_per_night: int = Field(description="Cost per night in KRW", ge=0)
    total_nights: int = Field(description="Total number of nights", ge=0)


class TravelPlan(BaseModel):
    """Complete travel plan structure.

    Example:
        title: '서울 역사 탐방 3일 여행'
        total_days: 3
        total_cost: 500000
        itinerary: [DayItinerary(...), DayItinerary(...), DayItinerary(...)]
        accommodation: AccommodationInfo(...)
        summary: '경복궁, 북촌 한옥마을 등을 포함한 서울의 역사와 문화를 체험하는 여행'
    """

    title: str = Field(description="Title of the travel plan")
    total_days: int = Field(description="Total number of days", gt=0)
    total_cost: int = Field(description="Total estimated cost in KRW", ge=0)
    itinerary: list[DayItinerary] = Field(description="Day-by-day itinerary")
    accommodation: AccommodationInfo = Field(description="Accommodation details")
    summary: str = Field(description="Brief summary of the plan")


class ValidationResult(BaseModel):
    """Result of travel plan validation.

    Example (valid):
        is_valid: True
        errors: []

    Example (invalid):
        is_valid: False
        errors: ['Budget exceeded by 30%', 'Day 2 has time conflicts']
    """

    is_valid: bool = Field(description="Whether the plan is valid")
    errors: list[str] = Field(
        default_factory=list,
        description="List of critical error messages if plan is invalid"
    )
