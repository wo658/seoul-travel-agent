"""Reviewer agent graph configuration."""

from langgraph.graph import END, START, StateGraph

from app.ai.agents.reviewer.nodes import (
    fetch_context,
    modify_plan,
    parse_feedback,
    route_feedback,
    validate_modification,
)
from app.ai.agents.reviewer.state import ReviewState


def create_reviewer_graph() -> StateGraph:
    """Create and configure the reviewer agent graph.

    Flow:
    START → parse_feedback → [approve] → END
                           ↓
                       [reject] → END (Planner needs to be called again)
                           ↓
                       [modify] → fetch_context → modify_plan → validate → END

    The fetch_context node retrieves relevant data (attractions, restaurants, accommodations)
    based on the modification type, enabling data-driven plan modifications.
    """
    # Initialize graph with ReviewState
    graph = StateGraph(ReviewState)

    # Add nodes
    graph.add_node("parse_feedback", parse_feedback)
    graph.add_node("fetch_context", fetch_context)
    graph.add_node("modify_plan", modify_plan)
    graph.add_node("validate", validate_modification)

    # Define edges
    graph.add_edge(START, "parse_feedback")

    # Conditional routing based on feedback type
    graph.add_conditional_edges(
        "parse_feedback",
        route_feedback,
        {
            "approve": END,
            "reject": END,
            "modify": "fetch_context",
        },
    )

    # Edges for modification flow
    graph.add_edge("fetch_context", "modify_plan")
    graph.add_edge("modify_plan", "validate")
    graph.add_edge("validate", END)

    return graph


# Compile the graph
reviewer_graph = create_reviewer_graph().compile()
