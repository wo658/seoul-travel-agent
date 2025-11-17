"""Pydantic models for reviewer agent structured outputs."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class FeedbackParsing(BaseModel):
    """Structured output for parsing user feedback.

    Example (approve):
        feedback_type: 'approve'
        target_section: None
        modification_type: None
        reasoning: '사용자가 계획에 만족함'

    Example (modify):
        feedback_type: 'modify'
        target_section: 'day_1'
        modification_type: 'restaurant'
        reasoning: '첫째 날 점심 식당을 변경 요청'
    """

    feedback_type: Literal["approve", "reject", "modify"] = Field(
        description="Type of feedback: approve, reject, or modify"
    )
    target_section: Optional[str] = Field(
        None,
        description="Which section to modify (e.g., 'day_1', 'day_2', 'budget', 'accommodation')"
    )
    modification_type: Optional[Literal[
        "restaurant", "food", "meal",
        "attraction", "activity",
        "accommodation", "hotel",
        "budget", "time", "general"
    ]] = Field(
        None,
        description="Category of modification needed"
    )
    reasoning: str = Field(
        description="Explanation of the feedback analysis"
    )
