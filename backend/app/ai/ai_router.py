"""AI domain router - LangGraph agent endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.ai_schemas import (
    GenerateTravelPlanRequest,
    ReviewTravelPlanRequest,
    TravelPlanResponse,
)
from app.ai.ai_service import ai_service
from app.database import get_db

router = APIRouter()


# Travel plan generation endpoints
@router.post("/plans/generate", response_model=TravelPlanResponse)
async def generate_travel_plan(
    request: GenerateTravelPlanRequest,
    db: Session = Depends(get_db),
):
    """Generate initial travel plan using Planner Agent.

    This endpoint uses LangGraph-based Planner Agent to:
    1. Parse user request and extract structured information
    2. Fetch relevant venues using vector search (SEO-33)
    3. Generate comprehensive day-by-day itinerary
    4. Validate budget and time constraints
    """
    try:
        plan = await ai_service.generate_initial_plan(
            user_request=request.user_request,
            dates=(request.start_date, request.end_date),
            budget=request.budget,
            interests=request.interests,
        )

        return TravelPlanResponse(plan=plan)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


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
