"""Plan domain schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


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
