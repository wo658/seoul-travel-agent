"""AI domain router."""

import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.ai.ai_schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.ai.ai_service import ai_service
from app.ai.models import Conversation, Message
from app.database import get_db

router = APIRouter()


# Conversation endpoints
@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
):
    """Create a new conversation with initial message."""
    # TODO: Get user_id from auth token
    user_id = 1  # Mock user for now

    try:
        return await ai_service.create_conversation(
            user_id=user_id,
            initial_message=request.initial_message,
            title=request.title,
            db=db,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=list[ConversationListResponse])
async def list_conversations(db: Session = Depends(get_db)):
    """List all conversations for current user."""
    # TODO: Get user_id from auth token
    user_id = 1  # Mock user for now

    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return [
        ConversationListResponse(
            id=conv.id,
            title=conv.title,
            status=conv.status,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages),
        )
        for conv in conversations
    ]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Get conversation with full message history."""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return ConversationResponse.model_validate(conversation)


@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(
    conversation_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """Send a message to conversation and get AI response."""
    try:
        return await ai_service.chat(
            conversation_id=conversation_id,
            user_message=request.content,
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversations/{conversation_id}/messages/stream")
async def stream_message(
    conversation_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """Stream AI response with Server-Sent Events."""

    async def event_generator():
        """Generate SSE events."""
        try:
            async for chunk in ai_service.stream_chat(
                conversation_id=conversation_id,
                user_message=request.content,
                db=db,
            ):
                # Send each chunk as SSE event
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            # Send completion event
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """Delete a conversation."""
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    db.delete(conversation)
    db.commit()

    return {"message": "Conversation deleted successfully"}


# Legacy endpoints
@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get AI-powered travel recommendations."""
    return await ai_service.get_recommendations(request)
