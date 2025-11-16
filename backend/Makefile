.PHONY: help install install-dev sync add remove update run test lint format clean

help: ## Show this help message
	@echo "Seoul Travel Agent - Backend Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv pip install -e .

install-dev: ## Install with dev dependencies
	uv pip install -e ".[dev]"

sync: ## Sync all dependencies to latest compatible versions
	uv pip compile pyproject.toml -o requirements.lock
	uv pip sync requirements.lock

add: ## Add a new dependency (usage: make add pkg=fastapi)
	uv pip install $(pkg)
	uv pip freeze | grep $(pkg) >> pyproject.toml

remove: ## Remove a dependency (usage: make remove pkg=fastapi)
	uv pip uninstall $(pkg)

update: ## Update all dependencies to latest versions
	uv pip install --upgrade -e ".[dev]"

run: ## Run development server
	uvicorn seoul_travel.main:app --reload --port 8000

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=seoul_travel --cov-report=html

lint: ## Lint code with ruff
	ruff check src/

format: ## Format code with ruff
	ruff format src/

type-check: ## Type check with mypy
	mypy src/

clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

db-migrate: ## Create database migration
	alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## Apply database migrations
	alembic upgrade head

db-downgrade: ## Rollback last migration
	alembic downgrade -1
