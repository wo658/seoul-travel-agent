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
    """Parse user request and extract structured information.

    Priority:
    1. Use structured data already in state (dates, budget, interests)
    2. Only use LLM parsing if data is missing from state
    """
    logger.info("🔵 [collect_info] Node started")
    logger.debug(f"📥 Input state: dates={state.get('dates')}, budget={state.get('budget')}, interests={state.get('interests')}")

    result = {}

    # Priority 1: Use existing structured data from state
    if state.get("dates") and state["dates"] != ("", ""):
        result["dates"] = state["dates"]
        logger.info(f"✅ [collect_info] Using provided dates: {result['dates']}")

    if state.get("budget") and state["budget"] > 0:
        result["budget"] = state["budget"]
        logger.info(f"✅ [collect_info] Using provided budget: {result['budget']:,} KRW")

    if state.get("interests") and len(state["interests"]) > 0:
        result["interests"] = state["interests"]
        logger.info(f"✅ [collect_info] Using provided interests: {result['interests']}")

    # Priority 2: Only parse from user_request if data is still missing
    missing_fields = []
    if "dates" not in result:
        missing_fields.append("dates")
    if "budget" not in result:
        missing_fields.append("budget")
    if "interests" not in result:
        missing_fields.append("interests")

    if missing_fields:
        logger.info(f"🔍 [collect_info] Parsing missing fields from user_request: {missing_fields}")

        llm = get_llm(temperature=0)
        prompt = COLLECT_INFO_PROMPT.format(user_request=state["user_request"])

        messages = [
            SystemMessage(content="You are a travel planning assistant."),
            HumanMessage(content=prompt),
        ]

        try:
            response = await llm.ainvoke(messages)
            parsed_data = json.loads(response.content)
            logger.debug(f"🤖 LLM parsed: {parsed_data}")

            # Fill in missing fields only
            if "dates" in missing_fields and parsed_data.get("dates"):
                result["dates"] = tuple(parsed_data["dates"])
            if "budget" in missing_fields and parsed_data.get("budget"):
                result["budget"] = parsed_data["budget"]
            if "interests" in missing_fields and parsed_data.get("interests"):
                result["interests"] = parsed_data["interests"]

        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"❌ [collect_info] LLM parsing failed: {e}")
            return {
                "errors": ["Failed to parse user request. Please provide clearer information."]
            }

    logger.info(f"✅ [collect_info] Final result: dates={result.get('dates')}, budget={result.get('budget')}, interests={result.get('interests')}")
    return result


async def fetch_venues(state: PlanningState) -> dict[str, Any]:
    """Fetch tourist attractions using ChromaDB and search nearby venues via Naver API."""
    logger.info("🔵 [fetch_venues] Node started")
    logger.debug(f"📥 Input state: interests={state.get('interests')}, budget={state.get('budget')}, dates={state.get('dates')}")

    from datetime import datetime
    from app.database import SessionLocal
    from app.tourist_attraction.models import TouristAttraction
    from app.tourist_attraction.vector_store import TouristAttractionVectorStore
    from app.naver.client import NaverLocalClient

    db = SessionLocal()

    try:
        # Step 1: Calculate number of days
        dates = state.get("dates", ("", ""))
        num_days = 1
        if dates and len(dates) == 2:
            try:
                start_date = datetime.strptime(dates[0], "%Y-%m-%d")
                end_date = datetime.strptime(dates[1], "%Y-%m-%d")
                num_days = (end_date - start_date).days + 1
            except Exception:
                pass

        logger.info(f"📅 [fetch_venues] Trip duration: {num_days} days")

        # Step 2: Use ChromaDB to find attractions matching user interests
        interests = state.get("interests", [])
        query = " ".join(interests) if interests else "서울 관광"

        logger.info(f"🔍 [fetch_venues] Searching attractions with ChromaDB: '{query}'")
        vector_store = TouristAttractionVectorStore(persist_directory="chroma_db")

        # Search for attractions (1 per day)
        attraction_results = vector_store.search_attractions(
            query=query,
            n_results=num_days,  # 하루당 관광지 1개
        )

        # Get full attraction data from DB
        selected_attractions = []
        for metadata, similarity in attraction_results:
            attraction_id = int(metadata["id"])
            attraction = db.query(TouristAttraction).filter(
                TouristAttraction.id == attraction_id
            ).first()

            if attraction:
                selected_attractions.append({
                    "id": attraction.id,
                    "name": attraction.name,
                    "category": attraction.category,
                    "description": attraction.introduction or "정보 없음",
                    "address": attraction.road_address or attraction.jibun_address or "",
                    "phone": attraction.phone or "",
                    "latitude": attraction.latitude,
                    "longitude": attraction.longitude,
                    "similarity_score": round(similarity, 3),
                })

        logger.info(f"✅ [fetch_venues] Selected {len(selected_attractions)} attractions via ChromaDB")
        for idx, attr in enumerate(selected_attractions, 1):
            logger.info(f"   {idx}. {attr['name']} (similarity: {attr['similarity_score']})")

        # Step 3: Search nearby restaurants and accommodations for each attraction
        all_restaurants = []
        all_accommodations = []

        try:
            naver_client = NaverLocalClient()

            for attraction in selected_attractions:
                attr_name = attraction["name"]
                # Extract location keyword from address
                address = attraction.get("address", "")
                location_keyword = address.split()[1] if len(address.split()) > 1 else "서울"

                # Search nearby restaurants
                logger.info(f"🔍 [fetch_venues] Searching restaurants near {attr_name} ({location_keyword})")
                restaurant_results = await naver_client.search_local(
                    query=f"{location_keyword} 맛집",
                    display=2,  # 관광지당 2개
                    sort="random",
                )

                for item in restaurant_results:
                    all_restaurants.append({
                        "name": item.get("title", ""),
                        "category": item.get("category", ""),
                        "address": item.get("roadAddress") or item.get("address", ""),
                        "phone": item.get("telephone", ""),
                        "latitude": item.get("latitude"),
                        "longitude": item.get("longitude"),
                        "description": f"카테고리: {item.get('category', '정보없음')}",
                        "near_attraction": attr_name,
                    })

            logger.info(f"✅ [fetch_venues] Found {len(all_restaurants)} restaurants via Naver API")

            # Search accommodations once (not per attraction)
            if selected_attractions:
                first_attr = selected_attractions[0]
                address = first_attr.get("address", "")
                location_keyword = address.split()[1] if len(address.split()) > 1 else "서울"

                logger.info(f"🔍 [fetch_venues] Searching accommodations in {location_keyword}")
                accommodation_results = await naver_client.search_local(
                    query=f"{location_keyword} 호텔 숙박",
                    display=5,
                    sort="random",
                )

                for item in accommodation_results:
                    all_accommodations.append({
                        "name": item.get("title", ""),
                        "category": item.get("category", ""),
                        "address": item.get("roadAddress") or item.get("address", ""),
                        "phone": item.get("telephone", ""),
                        "latitude": item.get("latitude"),
                        "longitude": item.get("longitude"),
                        "description": f"카테고리: {item.get('category', '정보없음')}",
                    })

                logger.info(f"✅ [fetch_venues] Found {len(all_accommodations)} accommodations via Naver API")

        except Exception as e:
            logger.warning(f"⚠️ [fetch_venues] Naver API error (continuing with attractions only): {e}")

        return {
            "attractions": selected_attractions,
            "restaurants": all_restaurants,
            "accommodations": all_accommodations,
        }

    except Exception as e:
        logger.error(f"❌ [fetch_venues] Error during venue search: {e}", exc_info=True)
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

    # Calculate trip details
    from datetime import datetime
    start_date = dates[0] if dates and len(dates) > 0 else ""
    end_date = dates[1] if dates and len(dates) > 1 else ""

    num_days = 1
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            num_days = (end - start).days + 1
        except Exception:
            pass

    prompt = GENERATE_PLAN_PROMPT.format(
        user_request=state["user_request"],
        start_date=start_date,
        end_date=end_date,
        num_days=num_days,
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
