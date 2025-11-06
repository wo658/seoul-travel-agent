"""Planner agent node functions."""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.ai.agents.planner.prompts import (
    COLLECT_INFO_PROMPT,
    GENERATE_PLAN_PROMPT,
    VALIDATE_PLAN_PROMPT,
)
from app.ai.agents.planner.state import PlanningState
from app.config import settings


def get_llm(temperature: float = 0.7, model: str = "gpt-4o") -> ChatOpenAI:
    """Get LLM instance."""
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=model,
        temperature=temperature,
    )


async def collect_info(state: PlanningState) -> dict[str, Any]:
    """Parse user request and extract structured information."""
    llm = get_llm(temperature=0)

    prompt = COLLECT_INFO_PROMPT.format(user_request=state["user_request"])

    messages = [
        SystemMessage(content="You are a travel planning assistant."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)

    try:
        parsed_data = json.loads(response.content)

        return {
            "dates": tuple(parsed_data.get("dates", state.get("dates", ("", "")))),
            "budget": parsed_data.get("budget", state.get("budget", 0)),
            "interests": parsed_data.get("interests", state.get("interests", [])),
        }
    except json.JSONDecodeError:
        return {
            "errors": ["Failed to parse user request. Please provide clearer information."]
        }


async def fetch_venues(state: PlanningState) -> dict[str, Any]:
    """Fetch relevant venues using vector search (SEO-33 integration)."""
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

    return {
        "attractions": [],
        "restaurants": [],
        "accommodations": [],
    }


async def generate_plan(state: PlanningState) -> dict[str, Any]:
    """Generate travel plan using LLM."""
    llm = get_llm(temperature=0.5, model="gpt-4o")

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

    try:
        travel_plan = json.loads(response.content)

        return {
            "travel_plan": travel_plan,
            "attempts": state.get("attempts", 0) + 1,
        }
    except json.JSONDecodeError:
        return {
            "errors": ["Failed to generate valid plan structure."],
            "attempts": state.get("attempts", 0) + 1,
        }


async def validate_plan(state: PlanningState) -> dict[str, Any]:
    """Validate generated plan for logical consistency."""
    if not state.get("travel_plan"):
        return {"errors": ["No plan to validate"]}

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

    try:
        validation_result = json.loads(response.content)

        if not validation_result.get("is_valid", False):
            errors = validation_result.get("errors", [])
            return {
                "errors": errors,
                "travel_plan": None,  # Clear invalid plan
            }

        return {}  # Valid plan, no changes needed

    except json.JSONDecodeError:
        return {"errors": ["Validation check failed"]}


def should_retry(state: PlanningState) -> str:
    """Routing function: decide whether to retry plan generation."""
    max_attempts = 3

    # If there are errors and haven't exceeded max attempts
    if state.get("errors") and state.get("attempts", 0) < max_attempts:
        return "retry"

    # If validation passed or max attempts reached
    return "end"
