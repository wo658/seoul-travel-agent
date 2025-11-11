"""Plan domain router."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.plan import plan_service
from app.plan.plan_schemas import (
    PlannerPlanCreate,
    TravelPlanResponse,
    TravelPlanUpdate,
)

router = APIRouter()
logger = logging.getLogger(__name__)


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


@router.post("/", response_model=TravelPlanResponse, status_code=status.HTTP_201_CREATED)
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
        HTTPException: 400 if validation fails, 500 if database error
    """
    try:
        created_plan = plan_service.create_plan(
            db=db,
            user_id=user_id,
            planner_data=plan.model_dump()
        )
        logger.info(f"Created plan {created_plan.id} for user {user_id}")
        return created_plan
    except ValidationError as e:
        logger.warning(f"Validation error creating plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except ValueError as e:
        logger.warning(f"Value error creating plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error creating plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create plan due to database error"
        )
    except Exception as e:
        logger.error(f"Unexpected error creating plan: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


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
    try:
        plan = plan_service.get_plan(db=db, plan_id=plan_id)

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan with ID {plan_id} not found"
            )

        # TODO: Add ownership check when authentication is implemented
        # if plan.user_id != current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

        return plan
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving plan {plan_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve plan due to database error"
        )


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
        HTTPException: 404 if plan not found, 400 if validation fails
    """
    try:
        # Prepare update data (exclude None values)
        update_data = plan.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        updated_plan = plan_service.update_plan(
            db=db,
            plan_id=plan_id,
            update_data=update_data
        )

        if not updated_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan with ID {plan_id} not found"
            )

        # TODO: Add ownership check when authentication is implemented
        # if updated_plan.user_id != current_user.id:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

        logger.info(f"Updated plan {plan_id}")
        return updated_plan
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error updating plan {plan_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update plan due to database error"
        )


@router.delete("/{plan_id}", status_code=status.HTTP_200_OK)
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
    try:
        # TODO: Add ownership check when authentication is implemented
        deleted = plan_service.delete_plan(db=db, plan_id=plan_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan with ID {plan_id} not found"
            )

        logger.info(f"Deleted plan {plan_id}")
        return {"message": "Plan deleted successfully"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting plan {plan_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete plan due to database error"
        )
