"""AI domain schemas."""

from typing import List, Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request."""

    messages: List[ChatMessage]
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """Chat response."""

    message: str
    suggestions: Optional[List[str]] = None


class RecommendationRequest(BaseModel):
    """Travel recommendation request."""

    interests: List[str]
    duration_days: int
    budget_level: str = "medium"  # low, medium, high


class RecommendationResponse(BaseModel):
    """Travel recommendation response."""

    places: List[dict]
    restaurants: List[dict]
    activities: List[dict]
