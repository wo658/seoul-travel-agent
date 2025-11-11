"""Plan domain service layer."""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.plan.models import TravelPlan
from app.plan.plan_schemas import PlannerPlanCreate


# ============================================================================
# Helper Functions
# ============================================================================


def _extract_dates_from_itinerary(itinerary_data: List[Dict]) -> tuple[datetime, datetime]:
    """Extract start and end dates from itinerary days.

    Args:
        itinerary_data: List of day itinerary dictionaries

    Returns:
        Tuple of (start_date, end_date)
    """
    if not itinerary_data:
        raise ValueError("Itinerary data is empty")

    # Parse first and last day dates
    first_date_str = itinerary_data[0]["date"]
    last_date_str = itinerary_data[-1]["date"]

    start_date = datetime.strptime(first_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(last_date_str, "%Y-%m-%d")

    return start_date, end_date


def _convert_planner_to_travel_plan_data(planner_plan: PlannerPlanCreate) -> Dict:
    """Convert PlannerPlan schema to TravelPlan model data.

    Args:
        planner_plan: Validated PlannerPlanCreate schema

    Returns:
        Dictionary with TravelPlan model fields
    """
    # Convert itinerary list to backend JSON structure
    itinerary_json = {
        "total_days": planner_plan.total_days,
        "days": [day.model_dump() for day in planner_plan.itinerary]
    }

    # Convert recommendations (accommodation)
    recommendations_json = {}
    if planner_plan.accommodation:
        recommendations_json["accommodation"] = planner_plan.accommodation.model_dump()

    return {
        "title": planner_plan.title,
        "description": planner_plan.summary or "",
        "itinerary": itinerary_json,
        "recommendations": recommendations_json,
    }


# ============================================================================
# Database Query Helpers
# ============================================================================


def _get_plan_by_id(db: Session, plan_id: int) -> Optional[TravelPlan]:
    """Get plan by ID from database.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        TravelPlan instance or None if not found
    """
    return db.query(TravelPlan).filter(TravelPlan.id == plan_id).first()


def _get_plans_by_user(db: Session, user_id: int) -> List[TravelPlan]:
    """Get all plans for a user from database.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        List of TravelPlan instances
    """
    return db.query(TravelPlan).filter(TravelPlan.user_id == user_id).all()


# ============================================================================
# CRUD Operations
# ============================================================================


def create_plan(
    db: Session,
    user_id: int,
    planner_data: Dict
) -> TravelPlan:
    """Create a new travel plan from Planner Agent response.

    Args:
        db: Database session
        user_id: User ID who owns the plan
        planner_data: Dictionary with PlannerPlan structure

    Returns:
        Created TravelPlan instance

    Raises:
        ValueError: If itinerary data is invalid or empty
    """
    # Validate with Pydantic schema
    planner_plan = PlannerPlanCreate(**planner_data)

    # Convert to TravelPlan data
    plan_data = _convert_planner_to_travel_plan_data(planner_plan)

    # Extract dates from itinerary
    itinerary_list = [day.model_dump() for day in planner_plan.itinerary]
    start_date, end_date = _extract_dates_from_itinerary(itinerary_list)

    # Create TravelPlan instance
    travel_plan = TravelPlan(
        user_id=user_id,
        title=plan_data["title"],
        description=plan_data["description"],
        itinerary=plan_data["itinerary"],
        recommendations=plan_data["recommendations"],
        start_date=start_date,
        end_date=end_date,
    )

    db.add(travel_plan)
    db.commit()
    db.refresh(travel_plan)

    return travel_plan


def get_plan(
    db: Session,
    plan_id: int
) -> Optional[TravelPlan]:
    """Get a travel plan by ID.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        TravelPlan instance or None if not found
    """
    return _get_plan_by_id(db, plan_id)


def list_plans(
    db: Session,
    user_id: int
) -> List[TravelPlan]:
    """List all travel plans for a user.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        List of TravelPlan instances
    """
    return _get_plans_by_user(db, user_id)


def update_plan(
    db: Session,
    plan_id: int,
    update_data: Dict
) -> Optional[TravelPlan]:
    """Update a travel plan.

    Args:
        db: Database session
        plan_id: Plan ID
        update_data: Dictionary with fields to update

    Returns:
        Updated TravelPlan instance or None if not found
    """
    plan = _get_plan_by_id(db, plan_id)

    if not plan:
        return None

    # Update only provided fields
    for field, value in update_data.items():
        if value is not None and hasattr(plan, field):
            setattr(plan, field, value)

    # Update timestamp
    plan.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(plan)

    return plan


def delete_plan(
    db: Session,
    plan_id: int
) -> bool:
    """Delete a travel plan.

    Args:
        db: Database session
        plan_id: Plan ID

    Returns:
        True if deleted, False if not found
    """
    plan = _get_plan_by_id(db, plan_id)

    if not plan:
        return False

    db.delete(plan)
    db.commit()

    return True
