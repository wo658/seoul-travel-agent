"""Planner agent graph configuration."""

import logging

from langgraph.graph import START, StateGraph

from app.ai.agents.planner.nodes import (
    collect_info,
    fetch_venues,
    generate_plan,
)
from app.ai.agents.planner.state import PlanningState

logger = logging.getLogger(__name__)


def create_planner_graph() -> StateGraph:
    """Create and configure the planner agent graph.

    Flow (using Command-based routing):
    START → collect_info → fetch_venues → generate_plan → END

    Note: Validation step temporarily disabled, but validate_plan node
    has been updated to use Command-based routing for future use.

    All routing is handled by Command objects returned from nodes:
    - collect_info routes to: fetch_venues
    - fetch_venues routes to: generate_plan
    - generate_plan routes to: END
    - validate_plan (disabled) routes to: generate_plan (retry) or END (valid/max attempts)
    """
    logger.info("🏗️ Creating planner graph with Command-based routing")

    # Initialize graph with PlanningState
    graph = StateGraph(PlanningState)

    # Add nodes
    graph.add_node("collect_info", collect_info)
    graph.add_node("fetch_venues", fetch_venues)
    graph.add_node("generate_plan", generate_plan)
    # graph.add_node("validate", validate_plan)  # Temporarily disabled
    logger.debug("📦 Added 3 nodes: collect_info, fetch_venues, generate_plan")

    # Define entry edge
    graph.add_edge(START, "collect_info")
    logger.debug("🔗 Added entry edge from START to collect_info")

    # Note: All other routing is handled by Command objects returned from nodes
    # No need for explicit edges between nodes - Command handles routing

    logger.info("✅ Planner graph created successfully with Command-based routing (validation disabled)")
    return graph


# Compile the graph
planner_graph = create_planner_graph().compile()
