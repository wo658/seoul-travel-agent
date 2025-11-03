"""Plan domain router."""

from typing import List
from fastapi import APIRouter
from .schemas import TravelPlanCreate, TravelPlanUpdate, TravelPlanResponse

router = APIRouter()


@router.get("/", response_model=List[TravelPlanResponse])
async def list_plans():
    """List all travel plans for current user."""
    # TODO: Implement plan listing
    return []


@router.post("/", response_model=TravelPlanResponse)
async def create_plan(plan: TravelPlanCreate):
    """Create a new travel plan."""
    # TODO: Implement plan creation
    from datetime import datetime

    return TravelPlanResponse(
        id=1,
        user_id=1,
        title=plan.title,
        description=plan.description,
        start_date=plan.start_date,
        end_date=plan.end_date,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@router.get("/{plan_id}", response_model=TravelPlanResponse)
async def get_plan(plan_id: int):
    """Get a specific travel plan."""
    # TODO: Implement plan retrieval
    from datetime import datetime

    return TravelPlanResponse(
        id=plan_id,
        user_id=1,
        title="My Seoul Trip",
        description="3-day Seoul adventure",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@router.patch("/{plan_id}", response_model=TravelPlanResponse)
async def update_plan(plan_id: int, plan: TravelPlanUpdate):
    """Update a travel plan."""
    # TODO: Implement plan update
    from datetime import datetime

    return TravelPlanResponse(
        id=plan_id,
        user_id=1,
        title=plan.title or "Updated Plan",
        description=plan.description,
        itinerary=plan.itinerary,
        recommendations=plan.recommendations,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


@router.delete("/{plan_id}")
async def delete_plan(plan_id: int):
    """Delete a travel plan."""
    # TODO: Implement plan deletion
    return {"message": "Plan deleted successfully"}
