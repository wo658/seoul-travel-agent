.PHONY: help install dev build up down logs clean restart ps backend-shell db-shell test

help: ## Show this help message
	@echo "Seoul Travel Agent - Development Commands"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Local Development (Fast - SQLite)
install: ## Install all dependencies locally (no Docker)
	@echo "📦 Installing backend dependencies..."
	cd backend && uv pip install -e ".[dev]"
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ All dependencies installed!"

dev: install ## Start local development servers (SQLite + hot reload)
	@echo "🚀 Starting local development..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@echo ""
	@echo "Run in separate terminals:"
	@echo "  Terminal 1: cd backend && make run"
	@echo "  Terminal 2: cd frontend && npm run web"

dev-backend: ## Run backend only (local SQLite)
	cd backend && uvicorn seoul_travel.main:app --reload --port 8000

dev-frontend: ## Run frontend only (local)
	cd frontend && npm run web

# Docker Commands (Full Stack)
build: ## Build Docker images
	docker-compose build

up: ## Start all services with Docker (PostgreSQL)
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/api/docs"

down: ## Stop all Docker services
	docker-compose down

restart: down up ## Restart all Docker services

logs: ## Show Docker logs (all services)
	docker-compose logs -f

logs-backend: ## Show backend logs only
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs only
	docker-compose logs -f frontend

logs-db: ## Show database logs only
	docker-compose logs -f db

ps: ## Show running containers
	docker-compose ps

# Shell Access
backend-shell: ## Access backend container shell
	docker-compose exec backend bash

db-shell: ## Access PostgreSQL shell
	docker-compose exec db psql -U postgres -d seoul_travel

# Testing & Quality
test: ## Run all tests
	cd backend && pytest
	@echo "Frontend tests not configured yet"

test-backend: ## Run backend tests only
	cd backend && pytest --cov=seoul_travel

lint: ## Lint all code
	cd backend && ruff check src/
	cd frontend && npm run lint

format: ## Format all code
	cd backend && ruff format src/

# Database
db-migrate: ## Create database migration
	cd backend && alembic revision --autogenerate -m "$(msg)"

db-upgrade: ## Apply database migrations
	cd backend && alembic upgrade head

db-downgrade: ## Rollback last migration
	cd backend && alembic downgrade -1

# Cleanup
clean: ## Clean up Docker resources and build artifacts
	docker-compose down -v
	cd backend && make clean
	cd frontend && rm -rf node_modules .expo dist web-build
	@echo "✅ Cleanup complete!"

clean-db: ## Remove database volume
	docker-compose down -v
	rm -f backend/seoul_travel.db

# Quick Start Aliases
start: up ## Alias for 'up'
stop: down ## Alias for 'down'
