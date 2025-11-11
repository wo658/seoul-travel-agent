"""AI domain schemas."""

from datetime import datetime

from pydantic import BaseModel


# Message schemas
class MessageBase(BaseModel):
    """Base message schema."""

    role: str
    content: str


class MessageCreate(MessageBase):
    """Message creation schema."""

    conversation_id: int


class MessageResponse(MessageBase):
    """Message response schema."""

    id: int
    conversation_id: int
    model: str | None = None
    tokens_used: int | None = None
    created_at: datetime

    class Config:
        from_attributes = True


# Conversation schemas
class ConversationCreate(BaseModel):
    """Conversation creation schema."""

    initial_message: str
    title: str | None = None


class ConversationResponse(BaseModel):
    """Conversation response schema."""

    id: int
    user_id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Conversation list item schema."""

    id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True


# Chat schemas
class ChatRequest(BaseModel):
    """Chat request schema."""

    content: str


class ChatResponse(BaseModel):
    """Chat response schema."""

    message: str
    conversation_id: int
    message_id: int


# Travel plan generation
class GeneratePlanRequest(BaseModel):
    """Generate travel plan from conversation."""

    conversation_id: int


class GeneratePlanResponse(BaseModel):
    """Generated travel plan response."""

    plan_id: int
    title: str
    itinerary: dict


# Legacy schemas (for backward compatibility)
class ChatMessage(BaseModel):
    """Chat message."""

    role: str
    content: str


class ChatRequestLegacy(BaseModel):
    """Legacy chat request."""

    messages: list[ChatMessage]
    context: dict | None = None


class ChatResponseLegacy(BaseModel):
    """Legacy chat response."""

    message: str
    suggestions: list[str] | None = None


class RecommendationRequest(BaseModel):
    """Travel recommendation request."""

    interests: list[str]
    duration_days: int
    budget_level: str = "medium"  # low, medium, high


class RecommendationResponse(BaseModel):
    """Travel recommendation response."""

    places: list[dict]
    restaurants: list[dict]
    activities: list[dict]


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
