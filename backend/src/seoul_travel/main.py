"""Main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from seoul_travel.ai.router import router as ai_router
from seoul_travel.auth.router import router as auth_router
from seoul_travel.plan.router import router as plan_router
from seoul_travel.config.settings import settings


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Seoul Travel Agent API",
        description="AI-powered travel planning for Seoul",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
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
