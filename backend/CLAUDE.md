# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Seoul Travel Agent backend - FastAPI application with Python 3.13 and AI-powered travel planning for Seoul.

## Development Commands

### Essential Commands (using uv - blazingly fast package manager)

```bash
# Install dependencies
uv pip install -e .              # Production dependencies
uv pip install -e ".[dev]"       # Include dev dependencies

# Run server
uv run uvicorn app.main:app --reload --port 8000

# Testing
uv run pytest                    # Run all tests
uv run pytest --cov=app          # With coverage

# Code quality
uv run ruff check .              # Lint
uv run ruff format .             # Format
uv run mypy app/                 # Type check

# Dependency management
uv add <package>                 # Add new dependency
uv remove <package>              # Remove dependency
```

### Makefile Commands (Recommended)

```bash
make help           # Show all commands
make install-dev    # Install with dev dependencies
make run            # Run development server
make test           # Run tests
make test-cov       # Tests with coverage
make lint           # Lint code
make format         # Format code
make type-check     # Type checking
```

### Database Migrations

```bash
# Note: Alembic not yet configured, database.py contains models
# When setting up:
uv run alembic init alembic
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
uv run alembic downgrade -1
```

## Architecture

### Project Structure (Nest.js Style)

```
backend/
├── app/                         # Main application package
│   ├── ai/                      # AI domain module
│   │   ├── ai_router.py         # FastAPI routes
│   │   ├── ai_schemas.py        # Pydantic models
│   │   └── ai_service.py        # Business logic
│   ├── auth/                    # Authentication domain
│   │   ├── auth_router.py
│   │   └── auth_schemas.py
│   ├── plan/                    # Travel plans domain
│   │   ├── plan_router.py
│   │   └── plan_schemas.py
│   ├── config.py                # App settings (pydantic-settings)
│   ├── database.py              # SQLAlchemy models (User, TravelPlan)
│   └── main.py                  # FastAPI app factory
├── pyproject.toml               # Dependencies managed by uv
└── seoul_travel.db              # SQLite database (development)
```

### Domain Module Pattern

Each domain (ai, auth, plan) follows Nest.js-style naming:
- `{domain}_router.py` - FastAPI endpoint definitions
- `{domain}_schemas.py` - Pydantic request/response models
- `{domain}_service.py` - Business logic (if needed)
- `__init__.py` - Exports router for app registration

### Application Factory Pattern

The app is created via `create_application()` factory in [app/main.py](app/main.py:12:0-12:0):
1. Creates FastAPI instance with API prefix configuration
2. Adds CORS middleware (configured in [app/config.py](app/config.py:16:0-17:0))
3. Registers domain routers with prefixes:
   - `/api/ai` - AI chat and recommendations
   - `/api/auth` - User authentication
   - `/api/plans` - Travel plan CRUD

### Configuration Management

Settings loaded from [app/config.py](app/config.py:8:0-8:0) using `pydantic-settings`:
- Environment-based configuration (`.env` file)
- Database URL switches between SQLite (dev) and PostgreSQL (docker/prod)
- API keys for OpenAI/Anthropic LLM integration
- JWT auth configuration

### Database Layer

SQLAlchemy models in [app/database.py](app/database.py:1:0-1:0):
- `User` - User accounts with hashed passwords
- `TravelPlan` - Travel plans with AI-generated content (JSON fields)
- Relationship: User 1-to-many TravelPlan

**Important**: Database migrations not yet configured. Models exist but no Alembic setup.

## Key Patterns

### Router Registration
Routers are imported from domain `__init__.py` and registered with prefix + tags:
```python
from app.ai import router as ai_router
app.include_router(ai_router, prefix="/api/ai", tags=["AI"])
```

### Import Paths
All imports use absolute `app.*` paths (not relative):
```python
from app.ai.ai_schemas import ChatRequest      # Correct
from .ai_schemas import ChatRequest            # Avoid
```

### Service Singleton Pattern
Services are instantiated as module-level singletons:
```python
ai_service = AIService()  # In ai_service.py
```

## Environment Setup

Copy `.env.example` to `.env` and configure:
- `DATABASE_URL` - SQLite for local, PostgreSQL for docker
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` - LLM API keys
- `SECRET_KEY` - JWT signing key (change in production)
- `CORS_ORIGINS` - Frontend URLs (default: localhost:3000, localhost:8081)

## API Documentation

When server is running:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI spec: http://localhost:8000/api/openapi.json

## Technology Stack

- **FastAPI** - Modern async web framework
- **Python 3.13** - Latest Python with performance improvements
- **uv** - Ultra-fast package manager (10-100x faster than pip)
- **SQLAlchemy** - ORM with async support
- **Pydantic v2** - Data validation and settings
- **Ruff** - Fast linting and formatting
- **mypy** - Static type checking

## Development Notes

### uv vs pip
This project uses `uv` instead of `pip` for 10-100x faster installs. All `pip` commands work but prefer `uv`:
- `uv pip install` instead of `pip install`
- `uv add/remove` for dependency management

### Testing Strategy
Currently no tests implemented. When adding:
- Use `pytest` with `pytest-asyncio` for async tests
- Test client: `httpx.AsyncClient` for FastAPI testing
- Follow structure: `tests/{domain}/test_{module}.py`

### LLM Integration Status
AI service ([app/ai/ai_service.py](app/ai/ai_service.py:11:0-11:0)) has stub implementations marked with TODO:
- OpenAI/Anthropic integration not yet implemented
- API keys configured but not used yet
- Returns mock data for chat and recommendations

### Database Migration Setup
When ready to add Alembic:
1. Run `uv run alembic init alembic`
2. Update `alembic/env.py` to import `app.database.Base`
3. Set `sqlalchemy.url` in `alembic.ini` to use `app.config.settings.DATABASE_URL`
