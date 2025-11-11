"""AI domain router - LangGraph agent endpoints."""

import json
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.ai.ai_schemas import (
    GenerateTravelPlanRequest,
    ReviewTravelPlanRequest,
    TravelPlanResponse,
)
from app.ai.ai_service import ai_service
from app.database import get_db
from app.plan import plan_service

logger = logging.getLogger(__name__)

router = APIRouter()


# Travel plan generation endpoints
@router.post("/plans/generate", response_model=TravelPlanResponse)
async def generate_travel_plan(
    request: GenerateTravelPlanRequest,
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    save_to_db: bool = Query(True, description="Whether to save the generated plan to database"),
    db: Session = Depends(get_db),
):
    """Generate initial travel plan using Planner Agent.

    This endpoint uses LangGraph-based Planner Agent to:
    1. Parse user request and extract structured information
    2. Fetch relevant venues using vector search (SEO-33)
    3. Generate comprehensive day-by-day itinerary
    4. Validate budget and time constraints
    5. Optionally save the plan to database (default: True)

    Frontend usage:
    ```javascript
    // Generate plan and save to DB (default)
    const response = await fetch('/api/ai/plans/generate?user_id=1', {
      method: 'POST',
      body: JSON.stringify({
        user_request: "3일 서울 여행",
        start_date: "2025-07-01",
        end_date: "2025-07-03",
        budget: 500000,
        interests: ["palace", "food"]
      })
    });

    // Generate plan without saving
    const response = await fetch('/api/ai/plans/generate?user_id=1&save_to_db=false', {
      method: 'POST',
      body: JSON.stringify({ ... })
    });
    ```

    Args:
        request: Travel plan generation request
        user_id: User ID (temporary: will be replaced with authentication)
        save_to_db: Whether to save the generated plan to database (default: True)
        db: Database session

    Returns:
        TravelPlanResponse with generated plan and optional plan_id if saved
    """
    logger.info("🚀 [API] POST /plans/generate - Request received")
    logger.debug(f"📥 Request: dates={request.start_date} to {request.end_date}, budget={request.budget}, interests={request.interests}, save_to_db={save_to_db}")

    try:
        plan = await ai_service.generate_initial_plan(
            user_request=request.user_request,
            dates=(request.start_date, request.end_date),
            budget=request.budget,
            interests=request.interests,
        )

        logger.info("✅ [API] Plan generation completed successfully")

        # Optionally save to database
        plan_id = None
        if save_to_db:
            try:
                saved_plan = plan_service.create_plan(
                    db=db,
                    user_id=user_id,
                    planner_data=plan
                )
                plan_id = saved_plan.id
                logger.info(f"💾 [API] Plan saved to database with ID: {plan_id}")
            except Exception as save_error:
                logger.error(f"⚠️ [API] Failed to save plan to database: {save_error}")
                # Continue even if save fails - plan generation was successful

        return TravelPlanResponse(plan=plan, plan_id=plan_id)

    except ValueError as e:
        logger.error(f"❌ [API] Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ [API] Plan generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


@router.post("/plans/generate/stream")
async def generate_travel_plan_stream(
    request: GenerateTravelPlanRequest,
    db: Session = Depends(get_db),
):
    """Generate travel plan with SSE streaming for real-time progress updates.

    This endpoint streams the following events:
    - status: Current node execution status
    - node_start: When a node starts execution
    - node_complete: When a node completes with data
    - error: If any error occurs
    - complete: Final plan when generation is complete
    """
    logger.info("🚀 [API] POST /plans/generate/stream - SSE request received")
    logger.debug(f"📥 Request: dates={request.start_date} to {request.end_date}, budget={request.budget}")

    async def event_generator():
        """Generate SSE events for plan generation progress."""
        try:
            # Stream events from the planner agent
            async for event in ai_service.generate_plan_stream(
                user_request=request.user_request,
                dates=(request.start_date, request.end_date),
                budget=request.budget,
                interests=request.interests,
            ):
                # Format as SSE event
                event_data = json.dumps(event, ensure_ascii=False)
                yield f"data: {event_data}\n\n"

        except Exception as e:
            logger.error(f"❌ [API] Streaming error: {e}", exc_info=True)
            error_event = {
                "type": "error",
                "message": str(e),
            }
            yield f"data: {json.dumps(error_event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/plans/review", response_model=TravelPlanResponse)
async def review_travel_plan(
    request: ReviewTravelPlanRequest,
    original_plan: dict,
    db: Session = Depends(get_db),
):
    """Review and modify travel plan using Reviewer Agent.

    This endpoint uses LangGraph-based Reviewer Agent to:
    1. Parse user feedback (approve/reject/modify)
    2. Modify specific sections of the plan
    3. Validate modified plan consistency

    Request body should include the original plan in the request.
    """
    try:
        modified_plan = await ai_service.review_and_modify_plan(
            original_plan=original_plan,
            user_feedback=request.user_feedback,
            iteration=request.iteration,
        )

        return TravelPlanResponse(plan=modified_plan)

    except ValueError as e:
        # Rejection or need to regenerate
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan review failed: {str(e)}")
