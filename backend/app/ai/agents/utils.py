"""Shared utilities for LangGraph agents.

Only contains minimal shared utilities that are truly common.
Each agent maintains its own independence and responsibility.
"""

from langchain_openai import ChatOpenAI

from app.config import settings


def get_llm(temperature: float = 0.7) -> ChatOpenAI:
    """Get configured LLM instance.

    Args:
        temperature: Sampling temperature (0.0-1.0)

    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=temperature,
    )
