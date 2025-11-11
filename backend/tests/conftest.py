"""Pytest configuration and fixtures for backend tests."""

import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add app directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database import Base, get_db
from app.main import create_application

# Import all models to ensure they are registered with Base metadata
from app.auth.models import User  # noqa: F401
from app.plan.models import TravelPlan  # noqa: F401
from app.tourist_attraction.models import TouristAttraction  # noqa: F401


@pytest.fixture(scope="function")
def test_db_session():
    """Create a test database session for each test."""
    # Use in-memory SQLite for tests with poolclass=StaticPool to share connection
    from sqlalchemy.pool import StaticPool

    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Share connection across threads
    )
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture(scope="function")
def client(test_db_session):
    """Create a test client with database override."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.config import settings
    from app.ai import router as ai_router
    from app.auth import router as auth_router
    from app.plan import router as plan_router

    # Create app without lifespan to avoid table creation conflicts
    app = FastAPI(
        title="Seoul Travel Agent API (Test)",
        description="Test application",
        version="0.1.0",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(plan_router, prefix="/api/plans", tags=["Travel Plans"])

    # Override database dependency
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def mock_user(test_db_session):
    """Create a mock user for testing."""
    from app.auth.models import User

    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="$2b$12$test_hashed_password",  # Mock password hash
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


@pytest.fixture
def mock_travel_plan(test_db_session, mock_user):
    """Create a mock travel plan for testing."""
    from app.plan.models import TravelPlan

    plan = TravelPlan(
        user_id=mock_user.id,
        title="Test Seoul Travel Plan",
        description="A test travel plan for Seoul",
        itinerary={
            "days": [
                {
                    "day": 1,
                    "date": "2025-01-01",
                    "activities": [
                        {
                            "time": "09:00",
                            "activity": "Visit Gyeongbokgung Palace",
                            "duration": 120,
                        }
                    ],
                }
            ]
        },
        recommendations={"restaurants": [], "attractions": []},
    )
    test_db_session.add(plan)
    test_db_session.commit()
    test_db_session.refresh(plan)
    return plan


@pytest.fixture
def auth_headers(client, mock_user):
    """Get authentication headers for testing protected endpoints."""
    # Mock JWT token creation
    from datetime import datetime, timedelta

    from jose import jwt

    access_token_expires = timedelta(minutes=30)
    expire = datetime.utcnow() + access_token_expires

    to_encode = {"sub": mock_user.email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, "test_secret_key", algorithm="HS256")

    return {"Authorization": f"Bearer {encoded_jwt}"}
