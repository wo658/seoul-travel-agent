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

        return {
            "dates": tuple(parsed_data.get("dates", state.get("dates", ("", "")))),
            "budget": parsed_data.get("budget", state.get("budget", 0)),
            "interests": parsed_data.get("interests", state.get("interests", [])),
        }
    except json.JSONDecodeError as e:
        logger.error(f"❌ [collect_info] JSON decode failed: {e}")
        logger.debug(f"Raw response: {response.content[:500]}")
        return {
            "errors": ["Failed to parse user request. Please provide clearer information."]
        }


async def fetch_venues(state: PlanningState) -> dict[str, Any]:
    """Fetch relevant venues using vector search (SEO-33 integration)."""
    logger.info("🔵 [fetch_venues] Node started")
    logger.debug(f"📥 Input state: interests={state.get('interests')}, budget={state.get('budget')}")

    # TODO: Integrate with SEO-33 vector search when available
    # For now, return placeholder data structure

    # Example integration:
    # from app.venue.service import search_venues_vector
    #
    # attractions = await search_venues_vector(
    #     db=db,
    #     query=f"{' '.join(state['interests'])} 관광지",
    #     category='attraction',
    #     limit=20,
    #     similarity_threshold=0.7,
    # )

    logger.info("✅ [fetch_venues] Returning placeholder data (SEO-33 not integrated yet)")
    return {
        "attractions": [],
        "restaurants": [],
        "accommodations": [],
    }


async def generate_plan(state: PlanningState) -> dict[str, Any]:
    """Generate travel plan using LLM."""
    attempt = state.get("attempts", 0) + 1
    logger.info(f"🔵 [generate_plan] Node started (attempt {attempt})")
    logger.debug(f"📥 Input state: dates={state.get('dates')}, budget={state.get('budget')}, interests={state.get('interests')}")
    logger.debug(f"📥 Venue counts: attractions={len(state.get('attractions', []))}, restaurants={len(state.get('restaurants', []))}, accommodations={len(state.get('accommodations', []))}")

    llm = get_llm(temperature=0.5)

    prompt = GENERATE_PLAN_PROMPT.format(
        user_request=state["user_request"],
        dates=state["dates"],
        budget=state["budget"],
        interests=", ".join(state["interests"]),
        attractions=json.dumps(state["attractions"], ensure_ascii=False),
        restaurants=json.dumps(state["restaurants"], ensure_ascii=False),
        accommodations=json.dumps(state["accommodations"], ensure_ascii=False),
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

    prompt = VALIDATE_PLAN_PROMPT.format(
        plan=json.dumps(state["travel_plan"], ensure_ascii=False),
        budget=state["budget"],
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
