"""Planner agent graph configuration."""

from langgraph.graph import END, START, StateGraph

from app.ai.agents.planner.nodes import (
    collect_info,
    fetch_venues,
    generate_plan,
    should_retry,
    validate_plan,
)
from app.ai.agents.planner.state import PlanningState


def create_planner_graph() -> StateGraph:
    """Create and configure the planner agent graph.

    Flow:
    START → collect_info → fetch_venues → generate_plan → validate
                                                              ↓
                                                          [valid] → END
                                                              ↓
                                                          [invalid] → generate_plan (retry max 3x)
    """
    # Initialize graph with PlanningState
    graph = StateGraph(PlanningState)

    # Add nodes
    graph.add_node("collect_info", collect_info)
    graph.add_node("fetch_venues", fetch_venues)
    graph.add_node("generate_plan", generate_plan)
    graph.add_node("validate", validate_plan)

    # Define edges
    graph.add_edge(START, "collect_info")
    graph.add_edge("collect_info", "fetch_venues")
    graph.add_edge("fetch_venues", "generate_plan")
    graph.add_edge("generate_plan", "validate")

    # Conditional routing: retry or end
    graph.add_conditional_edges(
        "validate",
        should_retry,
        {
            "retry": "generate_plan",
            "end": END,
        },
    )

    return graph


# Compile the graph
planner_graph = create_planner_graph().compile()
