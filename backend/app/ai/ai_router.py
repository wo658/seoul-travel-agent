"""AI domain router - LangGraph agent endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query
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
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Plan generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


@router.post("/plans/review", response_model=TravelPlanResponse)
async def review_travel_plan(
    request: ReviewTravelPlanRequest,
    original_plan: dict,
    plan_id: int | None = Query(None, description="Plan ID to update in database (optional)"),
    user_id: int | None = Query(None, description="User ID (optional, required if plan_id provided)"),
    db: Session = Depends(get_db),
):
    """Review and modify travel plan using Reviewer Agent.

    This endpoint uses LangGraph-based Reviewer Agent to:
    1. Parse user feedback (approve/reject/modify)
    2. Modify specific sections of the plan
    3. Validate modified plan consistency
    4. Optionally save modifications to database if plan_id provided

    Request body should include the original plan in the request.

    Args:
        request: Review request with user feedback and iteration
        original_plan: Original plan to be modified
        plan_id: Optional plan ID to update in database
        user_id: Optional user ID (required if plan_id provided)
        db: Database session

    Returns:
        TravelPlanResponse with modified plan and optional plan_id if saved
    """
    logger.info("🔄 [API] POST /plans/review - Request received")
    logger.debug(f"📥 Feedback: {request.user_feedback}, iteration={request.iteration}, plan_id={plan_id}")

    try:
        modified_plan = await ai_service.review_and_modify_plan(
            original_plan=original_plan,
            user_feedback=request.user_feedback,
            iteration=request.iteration,
        )

        logger.info("✅ [API] Plan review completed successfully")

        # Optionally save to database if plan_id provided
        if plan_id is not None:
            if user_id is None:
                raise HTTPException(
                    status_code=400,
                    detail="user_id is required when plan_id is provided"
                )

            try:
                # Verify plan exists and belongs to user
                existing_plan = plan_service.get_plan(db=db, plan_id=plan_id)
                if not existing_plan:
                    raise HTTPException(status_code=404, detail="Plan not found")
                if existing_plan.user_id != user_id:
                    raise HTTPException(status_code=403, detail="Not authorized to update this plan")

                # Convert modified_plan (full plan structure) to DB format
                # modified_plan has: {title, total_days, total_cost, days, accommodation, ...}
                # DB expects: {title, itinerary: {total_days, days}, recommendations: {accommodation}, ...}
                update_data = {
                    "itinerary": {
                        "total_days": modified_plan.get("total_days"),
                        "days": modified_plan.get("days", [])
                    }
                }

                # Update title if present
                if "title" in modified_plan:
                    update_data["title"] = modified_plan.get("title")

                # Update recommendations (accommodation) if present
                if "accommodation" in modified_plan and modified_plan.get("accommodation"):
                    update_data["recommendations"] = {
                        "accommodation": modified_plan.get("accommodation")
                    }

                # Update plan in database
                updated_plan = plan_service.update_plan(
                    db=db,
                    plan_id=plan_id,
                    update_data=update_data
                )
                logger.info(f"💾 [API] Plan {plan_id} updated in database")

                return TravelPlanResponse(plan=modified_plan, plan_id=plan_id)

            except Exception as save_error:
                logger.error(f"⚠️ [API] Failed to save plan to database: {save_error}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to save plan to database: {str(save_error)}"
                )

        return TravelPlanResponse(plan=modified_plan)

    except ValueError as e:
        # Rejection or need to regenerate
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Plan review failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Plan review failed: {str(e)}")
