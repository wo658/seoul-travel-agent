# Seoul Travel Agent - Backend

FastAPI backend with Python 3.13 + uv

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv

# Or via pip
pip install uv
```

## Quick Start

### Local Development (SQLite)

```bash
# Install dependencies with uv (blazingly fast! ⚡)
uv pip install -e .

# Or install with dev dependencies
uv pip install -e ".[dev]"

# Run the server
uvicorn seoul_travel.main:app --reload

# Access API docs
open http://localhost:8000/api/docs
```

### Using Makefile (Recommended)

```bash
# Show all available commands
make help

# Install dependencies
make install        # production dependencies
make install-dev    # with dev dependencies

# Run development server
make run

# Run tests
make test
make test-cov      # with coverage

# Code quality
make lint          # check code
make format        # auto-format
make type-check    # type checking
```

## Dependency Management with uv

### Add New Dependency

```bash
# Using uv directly (automatically updates pyproject.toml)
uv add fastapi-cache2

# Or manually add to pyproject.toml, then sync
uv pip install -e .
```

### Update Dependencies

```bash
# Update all to latest compatible versions
make update

# Or update specific package
uv pip install --upgrade fastapi
```

### Remove Dependency

```bash
# Using uv
uv remove fastapi-cache2

# Or manually remove from pyproject.toml, then sync
uv pip install -e .
```

### Docker Development (PostgreSQL)

```bash
# From project root
docker-compose up -d backend

# View logs
docker-compose logs -f backend
```

## Project Structure

```
backend/
├── src/
│   └── seoul_travel/
│       ├── ai/              # AI domain (LLM integration)
│       ├── auth/            # Authentication
│       ├── plan/            # Travel plans
│       ├── database/        # SQLAlchemy models
│       ├── config/          # Settings
│       └── main.py          # FastAPI app
├── pyproject.toml           # Dependencies (uv/pip)
├── .python-version          # Python 3.13
└── Dockerfile
```

## Development

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=seoul_travel
```

### Code Quality

```bash
# Format and lint with ruff
ruff check .
ruff format .

# Type checking with mypy
mypy src/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key variables:
- `DATABASE_URL` - SQLite (local) or PostgreSQL (Docker)
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `SECRET_KEY` - JWT secret key

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## Performance

Using `uv` instead of `pip`:
- 10-100x faster dependency resolution
- Deterministic installs
- Better dependency management
- Native Python 3.13 support
