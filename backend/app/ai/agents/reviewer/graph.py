"""Reviewer agent graph configuration."""

from langgraph.graph import END, START, StateGraph

from app.ai.agents.reviewer.nodes import (
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
                       [modify] → modify_plan → validate → END
    """
    # Initialize graph with ReviewState
    graph = StateGraph(ReviewState)

    # Add nodes
    graph.add_node("parse_feedback", parse_feedback)
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
            "modify": "modify_plan",
        },
    )

    # Edges for modification flow
    graph.add_edge("modify_plan", "validate")
    graph.add_edge("validate", END)

    return graph


# Compile the graph
reviewer_graph = create_reviewer_graph().compile()
