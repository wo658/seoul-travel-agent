"""Reviewer agent graph configuration."""

import logging

from langgraph.graph import START, StateGraph

from app.ai.agents.reviewer.nodes import (
    fetch_context,
    modify_plan,
    parse_feedback,
    validate_modification,
)
from app.ai.agents.reviewer.state import ReviewState

logger = logging.getLogger(__name__)


def create_reviewer_graph() -> StateGraph:
    """Create and configure the reviewer agent graph.

    Flow (using Command-based routing):
    START → parse_feedback → [Command routes to:]
                           ↓ approve → END
                           ↓ reject → END (Planner needs to be called again)
                           ↓ modify → fetch_context → modify_plan → validate → END

    The fetch_context node retrieves relevant data (attractions, restaurants, accommodations)
    based on the modification type, enabling data-driven plan modifications.

    Note: Routing is now handled by Command objects returned from nodes,
    replacing the previous conditional_edges approach.
    """
    logger.info("🏗️ Creating reviewer graph with Command-based routing")

    # Initialize graph with ReviewState
    graph = StateGraph(ReviewState)

    # Add nodes
    graph.add_node("parse_feedback", parse_feedback)
    graph.add_node("fetch_context", fetch_context)
    graph.add_node("modify_plan", modify_plan)
    graph.add_node("validate", validate_modification)
    logger.debug("📦 Added 4 nodes: parse_feedback, fetch_context, modify_plan, validate")

    # Define entry edge
    graph.add_edge(START, "parse_feedback")
    logger.debug("🔗 Added entry edge from START to parse_feedback")

    # Note: All other routing is handled by Command objects returned from nodes
    # - parse_feedback routes to: END (approve/reject) or fetch_context (modify)
    # - fetch_context routes to: modify_plan
    # - modify_plan routes to: validate
    # - validate routes to: END

    logger.info("✅ Reviewer graph created successfully with Command-based routing")
    return graph


# Compile the graph
reviewer_graph = create_reviewer_graph().compile()
