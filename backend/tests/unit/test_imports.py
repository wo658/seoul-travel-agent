"""Test that all modules can be imported without errors."""

import sys
from pathlib import Path

import pytest

# Add app directory to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))


class TestImports:
    """Test module imports to catch circular dependencies and import errors."""

    def test_import_main(self):
        """Test main application module can be imported."""
        from app.main import app, create_application

        assert app is not None
        assert create_application is not None

    def test_import_config(self):
        """Test configuration module can be imported."""
        from app.config import settings

        assert settings is not None

    def test_import_database(self):
        """Test database module can be imported."""
        from app.database import Base, SessionLocal, create_tables, get_db

        assert Base is not None
        assert SessionLocal is not None
        assert create_tables is not None
        assert get_db is not None

    def test_import_auth_modules(self):
        """Test auth domain modules can be imported."""
        from app.auth import router
        from app.auth.models import User

        assert router is not None
        assert User is not None

    def test_import_plan_modules(self):
        """Test plan domain modules can be imported."""
        from app.plan import router
        from app.plan.models import TravelPlan

        assert router is not None
        assert TravelPlan is not None

    def test_import_tourist_attraction_modules(self):
        """Test tourist attraction domain modules can be imported."""
        from app.tourist_attraction.models import TouristAttraction

        assert TouristAttraction is not None

    def test_import_ai_modules(self):
        """Test AI domain modules can be imported."""
        from app.ai import router
        from app.ai.ai_service import AIService, ai_service

        assert router is not None
        assert AIService is not None
        assert ai_service is not None

    def test_import_ai_agents_planner(self):
        """Test AI planner agent modules can be imported."""
        from app.ai.agents.planner.graph import create_planner_graph
        from app.ai.agents.planner.state import PlanningState

        assert create_planner_graph is not None
        assert PlanningState is not None

    def test_import_ai_agents_reviewer(self):
        """Test AI reviewer agent modules can be imported."""
        from app.ai.agents.reviewer.graph import create_reviewer_graph
        from app.ai.agents.reviewer.state import ReviewState

        assert create_reviewer_graph is not None
        assert ReviewState is not None

    def test_no_circular_imports(self):
        """Test that importing all modules doesn't cause circular import errors."""
        # Import all major modules in sequence
        from app.config import settings
        from app.database import Base
        from app.auth.models import User
        from app.plan.models import TravelPlan
        from app.tourist_attraction.models import TouristAttraction
        from app.ai.ai_service import ai_service
        from app.main import app

        # If we got here, no circular imports detected
        assert True


class TestLangGraphDependencies:
    """Test LangGraph dependencies are properly installed."""

    def test_langgraph_import(self):
        """Test that langgraph can be imported."""
        import langgraph
        from langgraph.graph import END, START, StateGraph

        assert langgraph is not None
        assert StateGraph is not None
        assert START is not None
        assert END is not None

    def test_langchain_imports(self):
        """Test that langchain dependencies can be imported."""
        import langchain
        import langchain_core
        import langchain_openai

        assert langchain is not None
        assert langchain_core is not None
        assert langchain_openai is not None

    def test_planner_graph_creation(self):
        """Test that planner graph can be created."""
        from app.ai.agents.planner.graph import create_planner_graph

        graph = create_planner_graph()
        assert graph is not None

    def test_reviewer_graph_creation(self):
        """Test that reviewer graph can be created."""
        from app.ai.agents.reviewer.graph import create_reviewer_graph

        graph = create_reviewer_graph()
        assert graph is not None
