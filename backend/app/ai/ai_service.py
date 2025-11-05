"""AI service - LLM integration logic."""

import json
from typing import AsyncGenerator, Optional

from anthropic import Anthropic
from openai import OpenAI
from sqlalchemy.orm import Session

from app.ai.ai_schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.ai.models import Conversation, Message
from app.ai.prompts import SEOUL_EXPERT_SYSTEM_PROMPT
from app.config import settings


class AIService:
    """AI service for travel recommendations and chat."""

    def __init__(self):
        """Initialize AI service with LLM clients."""
        self.openai_client = None
        self.anthropic_client = None

        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def _get_available_client(self):
        """Get first available LLM client."""
        if self.openai_client:
            return "openai", self.openai_client
        elif self.anthropic_client:
            return "anthropic", self.anthropic_client
        else:
            raise ValueError("No LLM API key configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")

    async def create_conversation(
        self,
        user_id: int,
        initial_message: str,
        db: Session,
        title: Optional[str] = None,
    ) -> ConversationResponse:
        """Create a new conversation with initial message."""
        # Generate title from initial message if not provided
        if not title:
            title = self._generate_title(initial_message)

        # Create conversation
        conversation = Conversation(
            user_id=user_id,
            title=title,
            status="active",
        )
        db.add(conversation)
        db.flush()

        # Add user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=initial_message,
        )
        db.add(user_message)

        # Generate AI response
        ai_response = await self._generate_response([{"role": "user", "content": initial_message}])

        # Add AI message
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response["content"],
            model=ai_response.get("model"),
            tokens_used=ai_response.get("tokens_used"),
        )
        db.add(ai_message)
        db.commit()
        db.refresh(conversation)

        return ConversationResponse.model_validate(conversation)

    async def chat(
        self,
        conversation_id: int,
        user_message: str,
        db: Session,
    ) -> ChatResponse:
        """Add message to conversation and get AI response."""
        # Get conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Add user message
        message = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )
        db.add(message)
        db.flush()

        # Get conversation history
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
        history = [{"role": msg.role, "content": msg.content} for msg in messages]

        # Generate AI response
        ai_response = await self._generate_response(history)

        # Add AI message
        ai_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response["content"],
            model=ai_response.get("model"),
            tokens_used=ai_response.get("tokens_used"),
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)

        return ChatResponse(
            message=ai_response["content"],
            conversation_id=conversation_id,
            message_id=ai_message.id,
        )

    async def stream_chat(
        self,
        conversation_id: int,
        user_message: str,
        db: Session,
    ) -> AsyncGenerator[str, None]:
        """Stream chat response with SSE."""
        # Get conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")

        # Add user message
        message = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )
        db.add(message)
        db.flush()

        # Get conversation history
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
        history = [{"role": msg.role, "content": msg.content} for msg in messages]

        # Stream AI response
        full_content = ""
        async for chunk in self._stream_response(history):
            full_content += chunk
            yield chunk

        # Save AI message after streaming completes
        ai_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_content,
            model="gpt-4" if self.openai_client else "claude-3-opus",
        )
        db.add(ai_message)
        db.commit()

    async def _generate_response(self, messages: list[dict]) -> dict:
        """Generate AI response from message history."""
        provider, client = self._get_available_client()

        if provider == "openai":
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SEOUL_EXPERT_SYSTEM_PROMPT},
                    *messages,
                ],
                temperature=0.7,
                max_tokens=1000,
            )
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "tokens_used": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason,
            }
        elif provider == "anthropic":
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system=SEOUL_EXPERT_SYSTEM_PROMPT,
                messages=messages,
            )
            return {
                "content": response.content[0].text,
                "model": response.model,
                "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
                "finish_reason": response.stop_reason,
            }

    async def _stream_response(self, messages: list[dict]) -> AsyncGenerator[str, None]:
        """Stream AI response from message history."""
        provider, client = self._get_available_client()

        if provider == "openai":
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": SEOUL_EXPERT_SYSTEM_PROMPT},
                    *messages,
                ],
                temperature=0.7,
                max_tokens=1000,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        elif provider == "anthropic":
            with client.messages.stream(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system=SEOUL_EXPERT_SYSTEM_PROMPT,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text

    def _generate_title(self, initial_message: str) -> str:
        """Generate conversation title from initial message."""
        # Simple title generation (first 50 chars)
        title = initial_message[:50]
        if len(initial_message) > 50:
            title += "..."
        return title

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
