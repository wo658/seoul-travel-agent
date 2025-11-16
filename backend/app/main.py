"""Main application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.ai import router as ai_router
from app.auth import router as auth_router
from app.config import settings
from app.database import create_tables
from app.plan import router as plan_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler."""
    logger.info("Starting Seoul Travel Agent API")
    create_tables()
    logger.info("Database tables created/verified")
    yield
    logger.info("Shutting down Seoul Travel Agent API")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Seoul Travel Agent API",
        description="AI-powered travel planning for Seoul",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
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

    @app.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "seoul-travel-agent"}

    return app


app = create_application()
