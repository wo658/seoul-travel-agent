"""Reviewer agent node functions."""

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.agents.reviewer.prompts import MODIFY_PLAN_PROMPT, PARSE_FEEDBACK_PROMPT
from app.ai.agents.reviewer.state import ReviewState
from app.ai.agents.utils import get_llm

logger = logging.getLogger(__name__)


async def parse_feedback(state: ReviewState) -> dict[str, Any]:
    """Parse user feedback to determine action type and modification needs."""
    llm = get_llm(temperature=0)

    prompt = PARSE_FEEDBACK_PROMPT.format(
        original_plan=json.dumps(state["original_plan"], ensure_ascii=False),
        user_feedback=state["user_feedback"],
    )

    messages = [
        SystemMessage(content="You are a feedback analysis assistant."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)

    try:
        parsed = json.loads(response.content)

        return {
            "feedback_type": parsed.get("feedback_type"),
            "target_section": parsed.get("target_section"),
            "modification_type": parsed.get("modification_type", "general"),
            "iteration": state.get("iteration", 0) + 1,
            "attractions": [],
            "restaurants": [],
            "accommodations": [],
        }
    except json.JSONDecodeError:
        return {
            "feedback_type": "reject",  # Default to reject on parse error
            "target_section": None,
            "modification_type": None,
            "iteration": state.get("iteration", 0) + 1,
        }


async def modify_plan(state: ReviewState) -> dict[str, Any]:
    """Modify specific section of the plan based on feedback and fetched context."""
    logger.info("Modifying plan with fetched context")

    llm = get_llm(temperature=0.3)

    # Prepare context data for LLM
    context_data = {
        "attractions": state.get("attractions", []),
        "restaurants": state.get("restaurants", []),
        "accommodations": state.get("accommodations", []),
    }

    # Count available options
    total_options = sum(len(v) for v in context_data.values())
    logger.info(f"Available context: {len(context_data['attractions'])} attractions, "
                f"{len(context_data['restaurants'])} restaurants, "
                f"{len(context_data['accommodations'])} accommodations")

    prompt = MODIFY_PLAN_PROMPT.format(
        original_plan=json.dumps(state["original_plan"], ensure_ascii=False, indent=2),
        user_feedback=state["user_feedback"],
        modification_type=state.get("modification_type", "general"),
        target_section=state.get("target_section", ""),
        context_data=json.dumps(context_data, ensure_ascii=False, indent=2),
    )

    messages = [
        SystemMessage(content="You are a travel plan modification expert. "
                              "Use the provided context data (attractions, restaurants, accommodations) "
                              "to make informed modifications to the plan."),
        HumanMessage(content=prompt),
    ]

    try:
        response = await llm.ainvoke(messages)
        modified_plan = json.loads(response.content)

        logger.info("Plan modification successful")
        return {
            "modified_plan": modified_plan,
        }
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse modified plan: {e}")
        return {
            "modified_plan": state["original_plan"],  # Return original on error
        }
    except Exception as e:
        logger.error(f"Error modifying plan: {e}", exc_info=True)
        return {
            "modified_plan": state["original_plan"],
        }


async def validate_modification(state: ReviewState) -> dict[str, Any]:
    """Validate modified plan maintains consistency."""
    # Simple validation: ensure modified plan has required structure
    modified = state.get("modified_plan")

    if not modified:
        return {}

    required_keys = ["title", "total_days", "days", "total_cost"]
    missing_keys = [key for key in required_keys if key not in modified]

    if missing_keys:
        return {
            "modified_plan": state["original_plan"],  # Revert to original
        }

    return {}  # Validation passed


async def fetch_context(state: ReviewState) -> dict[str, Any]:
    """Fetch additional context data based on modification type.

    Fetches data from:
    - Vector store: For attraction searches
    - Naver API: For restaurant and accommodation searches
    """
    logger.info(f"Fetching context for modification_type: {state.get('modification_type')}")

    modification_type = state.get("modification_type")
    original_plan = state.get("original_plan", {})

    result = {
        "attractions": [],
        "restaurants": [],
        "accommodations": [],
    }

    # Skip context fetching if not needed
    if modification_type in ["budget", "time", "general", None]:
        logger.info("Modification doesn't require external data - skipping context fetch")
        return result

    try:
        from app.database import SessionLocal
        from app.naver.client import NaverLocalClient
        from app.tourist_attraction.vector_store import TouristAttractionVectorStore

        # Extract location info from original plan
        plan_interests = original_plan.get("interests", [])
        first_day = original_plan.get("days", [{}])[0] if original_plan.get("days") else {}
        activities = first_day.get("activities", [])

        # Get base location from first activity (fallback to Gangnam)
        base_lat, base_lon = 37.4979, 127.0276  # Default: Gangnam
        if activities and len(activities) > 0:
            first_activity = activities[0]
            if "location" in first_activity:
                base_lat = first_activity["location"].get("latitude", base_lat)
                base_lon = first_activity["location"].get("longitude", base_lon)

        # Fetch attractions if needed
        if modification_type in ["attraction", "activity"]:
            logger.info("Fetching attractions from vector store")
            vector_store = TouristAttractionVectorStore()

            query = state.get("user_feedback", "")
            search_results = await vector_store.search_attractions(query=query, top_k=5)

            result["attractions"] = [
                {
                    "name": doc.get("name"),
                    "category": doc.get("category"),
                    "introduction": doc.get("introduction"),
                    "latitude": doc.get("latitude"),
                    "longitude": doc.get("longitude"),
                    "facilities": doc.get("public_facilities"),
                }
                for doc in search_results
            ]
            logger.info(f"Found {len(result['attractions'])} attractions")

        # Fetch restaurants if needed
        if modification_type in ["restaurant", "food", "meal"]:
            logger.info("Fetching restaurants from Naver API")
            naver_client = NaverLocalClient()

            # Extract keywords from user feedback
            query = state.get("user_feedback", "맛집")
            restaurants = await naver_client.search_nearby_restaurants(
                latitude=base_lat,
                longitude=base_lon,
                radius=2000,
                query=query[:20]  # Limit query length
            )

            result["restaurants"] = restaurants[:10]
            logger.info(f"Found {len(result['restaurants'])} restaurants")

        # Fetch accommodations if needed
        if modification_type in ["accommodation", "hotel"]:
            logger.info("Fetching accommodations from Naver API")
            naver_client = NaverLocalClient()

            query = state.get("user_feedback", "호텔")
            accommodations = await naver_client.search_nearby_accommodations(
                latitude=base_lat,
                longitude=base_lon,
                radius=3000,
                query=query[:20]
            )

            result["accommodations"] = accommodations[:10]
            logger.info(f"Found {len(result['accommodations'])} accommodations")

    except Exception as e:
        logger.error(f"Error fetching context: {e}", exc_info=True)
        # Continue with empty results rather than failing

    return result


def route_feedback(state: ReviewState) -> str:
    """Routing function: determine next action based on feedback type."""
    feedback_type = state.get("feedback_type")

    if feedback_type == "approve":
        return "approve"
    elif feedback_type == "reject":
        return "reject"
    elif feedback_type == "modify":
        return "modify"
    else:
        return "reject"  # Default to reject
