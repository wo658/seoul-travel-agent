"""Reviewer agent node functions."""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.ai.agents.reviewer.prompts import MODIFY_PLAN_PROMPT, PARSE_FEEDBACK_PROMPT
from app.ai.agents.reviewer.state import ReviewState
from app.config import settings


def get_llm(temperature: float = 0, model: str = "gpt-4o") -> ChatOpenAI:
    """Get LLM instance."""
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=model,
        temperature=temperature,
    )


async def parse_feedback(state: ReviewState) -> dict[str, Any]:
    """Parse user feedback to determine action type."""
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
            "iteration": state.get("iteration", 0) + 1,
        }
    except json.JSONDecodeError:
        return {
            "feedback_type": "reject",  # Default to reject on parse error
            "target_section": None,
            "iteration": state.get("iteration", 0) + 1,
        }


async def modify_plan(state: ReviewState) -> dict[str, Any]:
    """Modify specific section of the plan based on feedback."""
    llm = get_llm(temperature=0.3)

    # Extract modification requests from parsed feedback
    modification_requests = state.get("modification_requests", [])

    prompt = MODIFY_PLAN_PROMPT.format(
        original_plan=json.dumps(state["original_plan"], ensure_ascii=False),
        feedback_type=state["feedback_type"],
        target_section=state["target_section"],
        modification_requests=json.dumps(modification_requests, ensure_ascii=False),
    )

    messages = [
        SystemMessage(content="You are a travel plan modification expert."),
        HumanMessage(content=prompt),
    ]

    response = await llm.ainvoke(messages)

    try:
        modified_plan = json.loads(response.content)

        return {
            "modified_plan": modified_plan,
        }
    except json.JSONDecodeError:
        return {
            "modified_plan": state["original_plan"],  # Return original on error
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
