"""AI service - LLM integration logic."""

from app.ai.ai_schemas import (
    ChatRequest,
    ChatResponse,
    RecommendationRequest,
    RecommendationResponse,
)


class AIService:
    """AI service for travel recommendations and chat."""

    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process chat request with LLM."""
        # TODO: Integrate with OpenAI/Anthropic
        return ChatResponse(
            message="Hello! I'm your Seoul travel assistant. How can I help you plan your trip?",
            suggestions=[
                "Show me popular attractions",
                "Recommend local restaurants",
                "Plan a 3-day itinerary",
            ],
        )

    async def get_recommendations(
        self, request: RecommendationRequest
    ) -> RecommendationResponse:
        """Get AI-powered travel recommendations."""
        # TODO: Implement LLM-based recommendation logic
        return RecommendationResponse(
            places=[
                {
                    "name": "Gyeongbokgung Palace",
                    "description": "Historic royal palace",
                    "category": "Historical",
                }
            ],
            restaurants=[
                {
                    "name": "Gwangjang Market",
                    "description": "Traditional Korean street food",
                    "cuisine": "Korean",
                }
            ],
            activities=[
                {
                    "name": "Han River Cruise",
                    "description": "Scenic river tour",
                    "duration": "2 hours",
                }
            ],
        )


ai_service = AIService()
