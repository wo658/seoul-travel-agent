"""Plan domain router."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.plan import plan_service
from app.plan.plan_schemas import (
    PlannerPlanCreate,
    TravelPlanResponse,
    TravelPlanUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[TravelPlanResponse])
async def list_plans(
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    db: Session = Depends(get_db),
):
    """List all travel plans for current user.

    Args:
        user_id: User ID (temporary: will be replaced with authentication)
        db: Database session

    Returns:
        List of travel plans
    """
    plans = plan_service.list_plans(db=db, user_id=user_id)
    return plans


@router.post("/", response_model=TravelPlanResponse, status_code=201)
async def create_plan(
    plan: PlannerPlanCreate,
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    db: Session = Depends(get_db),
):
    """Create a new travel plan from Planner Agent response.

    Args:
        plan: PlannerPlan data from frontend
        user_id: User ID (temporary: will be replaced with authentication)
        db: Database session

    Returns:
        Created travel plan

    Raises:
        HTTPException: If creation fails
    """
    try:
        created_plan = plan_service.create_plan(
            db=db,
            user_id=user_id,
            planner_data=plan.model_dump()
        )
        return created_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{plan_id}", response_model=TravelPlanResponse)
async def get_plan(
    plan_id: int,
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    db: Session = Depends(get_db),
):
    """Get a specific travel plan.

    Args:
        plan_id: Plan ID
        user_id: User ID (temporary: will be replaced with authentication)
        db: Database session

    Returns:
        Travel plan details

    Raises:
        HTTPException: 404 if plan not found
    """
    plan = plan_service.get_plan(db=db, plan_id=plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # TODO: Add ownership check when authentication is implemented
    # if plan.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    return plan


@router.patch("/{plan_id}", response_model=TravelPlanResponse)
async def update_plan(
    plan_id: int,
    plan: TravelPlanUpdate,
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    db: Session = Depends(get_db),
):
    """Update a travel plan.

    Args:
        plan_id: Plan ID
        plan: Update data
        user_id: User ID (temporary: will be replaced with authentication)
        db: Database session

    Returns:
        Updated travel plan

    Raises:
        HTTPException: 404 if plan not found
    """
    # Prepare update data (exclude None values)
    update_data = plan.model_dump(exclude_unset=True)

    updated_plan = plan_service.update_plan(
        db=db,
        plan_id=plan_id,
        update_data=update_data
    )

    if not updated_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # TODO: Add ownership check when authentication is implemented
    # if updated_plan.user_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized")

    return updated_plan


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    user_id: int = Query(..., description="User ID (임시: 나중에 인증으로 대체)"),
    db: Session = Depends(get_db),
):
    """Delete a travel plan.

    Args:
        plan_id: Plan ID
        user_id: User ID (temporary: will be replaced with authentication)
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: 404 if plan not found
    """
    deleted = plan_service.delete_plan(db=db, plan_id=plan_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Plan not found")

    # TODO: Add ownership check when authentication is implemented

    return {"message": "Plan deleted successfully"}
