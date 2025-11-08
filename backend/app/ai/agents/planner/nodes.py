"""Planner agent node functions."""

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.agents.planner.prompts import (
    COLLECT_INFO_PROMPT,
    GENERATE_PLAN_PROMPT,
    VALIDATE_PLAN_PROMPT,
)
from app.ai.agents.planner.state import PlanningState
from app.ai.agents.utils import get_llm

logger = logging.getLogger(__name__)


async def collect_info(state: PlanningState) -> dict[str, Any]:
    """Parse user request and extract structured information."""
    logger.info("🔵 [collect_info] Node started")
    logger.debug(f"📥 Input state: user_request={state.get('user_request', '')[:100]}...")

    llm = get_llm(temperature=0)

    prompt = COLLECT_INFO_PROMPT.format(user_request=state["user_request"])

    messages = [
        SystemMessage(content="You are a travel planning assistant."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)
    logger.debug(f"🤖 LLM response length: {len(response.content)} chars")

    try:
        parsed_data = json.loads(response.content)
        logger.info(f"✅ [collect_info] Successfully parsed: dates={parsed_data.get('dates')}, budget={parsed_data.get('budget')}, interests={parsed_data.get('interests')}")

        # Only override state values if LLM extracted valid data
        # Otherwise, keep existing state values
        result = {}

        if parsed_data.get("dates") is not None:
            result["dates"] = tuple(parsed_data["dates"])
        elif state.get("dates") is not None:
            result["dates"] = state["dates"]

        if parsed_data.get("budget") is not None:
            result["budget"] = parsed_data["budget"]
        elif state.get("budget") is not None:
            result["budget"] = state["budget"]

        if parsed_data.get("interests") is not None:
            result["interests"] = parsed_data["interests"]
        elif state.get("interests") is not None:
            result["interests"] = state["interests"]

        return result
    except json.JSONDecodeError as e:
        logger.error(f"❌ [collect_info] JSON decode failed: {e}")
        logger.debug(f"Raw response: {response.content[:500]}")
        return {
            "errors": ["Failed to parse user request. Please provide clearer information."]
        }


async def fetch_venues(state: PlanningState) -> dict[str, Any]:
    """Fetch tourist attractions from database."""
    logger.info("🔵 [fetch_venues] Node started")
    logger.debug(f"📥 Input state: interests={state.get('interests')}, budget={state.get('budget')}")

    from app.database import SessionLocal
    from app.tourist_attraction.models import TouristAttraction

    # Create database session
    db = SessionLocal()

    try:
        # Get all tourist attractions
        attractions_query = db.query(TouristAttraction).all()

        # Convert to dict format for LLM consumption
        def attraction_to_dict(attraction):
            """Convert TouristAttraction to dict."""
            return {
                "id": attraction.id,
                "name": attraction.name,
                "category": attraction.category,
                "description": attraction.introduction or "정보 없음",
                "address": attraction.road_address or attraction.jibun_address or "",
                "phone": attraction.phone or "",
                "latitude": attraction.latitude,
                "longitude": attraction.longitude,
                "facilities": {
                    "public": attraction.public_facilities,
                    "cultural": attraction.cultural_facilities,
                    "sports": attraction.sports_facilities,
                },
            }

        attractions = [attraction_to_dict(a) for a in attractions_query]

        logger.info(f"✅ [fetch_venues] Found {len(attractions)} tourist attractions")

        # TODO: Implement Naver Local API integration for restaurants and accommodations
        return {
            "attractions": attractions,
            "restaurants": [],  # Will be populated via Naver Local API
            "accommodations": [],  # Will be populated via Naver Local API
        }

    except Exception as e:
        logger.error(f"❌ [fetch_venues] Error during venue search: {e}", exc_info=True)
        # Return empty lists on error to allow planning to continue
        return {
            "attractions": [],
            "restaurants": [],
            "accommodations": [],
        }
    finally:
        db.close()


async def generate_plan(state: PlanningState) -> dict[str, Any]:
    """Generate travel plan using LLM."""
    attempt = state.get("attempts", 0) + 1
    logger.info(f"🔵 [generate_plan] Node started (attempt {attempt})")
    logger.debug(f"📥 Input state: dates={state.get('dates')}, budget={state.get('budget')}, interests={state.get('interests')}")
    logger.debug(f"📥 Venue counts: attractions={len(state.get('attractions', []))}, restaurants={len(state.get('restaurants', []))}, accommodations={len(state.get('accommodations', []))}")

    llm = get_llm(temperature=0.5)

    # Safely get state values with defaults to prevent format errors
    dates = state.get("dates", ("", ""))
    budget = state.get("budget", 0)
    interests = state.get("interests", [])
    attractions = state.get("attractions", [])
    restaurants = state.get("restaurants", [])
    accommodations = state.get("accommodations", [])

    prompt = GENERATE_PLAN_PROMPT.format(
        user_request=state["user_request"],
        dates=dates,
        budget=budget,
        interests=", ".join(interests) if interests else "general sightseeing",
        attractions=json.dumps(attractions, ensure_ascii=False),
        restaurants=json.dumps(restaurants, ensure_ascii=False),
        accommodations=json.dumps(accommodations, ensure_ascii=False),
    )

    messages = [
        SystemMessage(content="You are an expert Seoul travel planner."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)
    logger.debug(f"🤖 LLM response length: {len(response.content)} chars")

    try:
        travel_plan = json.loads(response.content)
        logger.info(f"✅ [generate_plan] Successfully generated plan with {len(travel_plan.get('itinerary', []))} days")

        return {
            "travel_plan": travel_plan,
            "attempts": attempt,
        }
    except json.JSONDecodeError as e:
        logger.error(f"❌ [generate_plan] JSON decode failed: {e}")
        logger.debug(f"Raw response: {response.content[:500]}")
        return {
            "errors": ["Failed to generate valid plan structure."],
            "attempts": attempt,
        }


async def validate_plan(state: PlanningState) -> dict[str, Any]:
    """Validate generated plan for logical consistency."""
    logger.info("🔵 [validate_plan] Node started")

    if not state.get("travel_plan"):
        logger.error("❌ [validate_plan] No plan to validate")
        return {"errors": ["No plan to validate"]}

    logger.debug(f"📥 Validating plan with {len(state['travel_plan'].get('itinerary', []))} days")

    llm = get_llm(temperature=0)

    # Safely get budget with default to prevent format errors
    budget = state.get("budget", 0)

    prompt = VALIDATE_PLAN_PROMPT.format(
        plan=json.dumps(state["travel_plan"], ensure_ascii=False),
        budget=budget,
    )

    messages = [
        SystemMessage(content="You are a travel plan validator."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)
    logger.debug(f"🤖 LLM response length: {len(response.content)} chars")

    try:
        validation_result = json.loads(response.content)

        if not validation_result.get("is_valid", False):
            errors = validation_result.get("errors", [])
            logger.warning(f"⚠️ [validate_plan] Plan validation failed: {errors}")
            return {
                "errors": errors,
                "travel_plan": None,  # Clear invalid plan
            }

        logger.info("✅ [validate_plan] Plan is valid")
        return {}  # Valid plan, no changes needed

    except json.JSONDecodeError as e:
        logger.error(f"❌ [validate_plan] JSON decode failed: {e}")
        logger.debug(f"Raw response: {response.content[:500]}")
        return {"errors": ["Validation check failed"]}


def should_retry(state: PlanningState) -> str:
    """Routing function: decide whether to retry plan generation."""
    max_attempts = 3
    attempts = state.get("attempts", 0)
    errors = state.get("errors", [])

    logger.info(f"🔵 [should_retry] Routing decision started")
    logger.debug(f"📥 State: attempts={attempts}/{max_attempts}, errors={len(errors)}")

    # If there are errors and haven't exceeded max attempts
    if errors and attempts < max_attempts:
        logger.info(f"🔄 [should_retry] Retrying (attempt {attempts + 1}/{max_attempts})")
        logger.debug(f"Retry reason: {errors}")
        return "retry"

    # If validation passed or max attempts reached
    if attempts >= max_attempts:
        logger.warning(f"⚠️ [should_retry] Max attempts reached ({max_attempts})")
    else:
        logger.info("✅ [should_retry] Plan is valid, ending graph")

    return "end"
