"""AI domain router."""

from fastapi import APIRouter

from app.ai.ai_schemas import (
    ChatRequest,
    ChatResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.ai.ai_service import ai_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with AI travel assistant."""
    return await ai_service.chat(request)


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get AI-powered travel recommendations."""
    return await ai_service.get_recommendations(request)
