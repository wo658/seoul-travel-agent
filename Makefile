.PHONY: help install dev build up down logs clean restart ps backend-shell db-shell test web webapp start-all

help: ## Show this help message
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  Seoul Travel Agent - Development Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🚀 ONE-COMMAND QUICK START:"
	@echo "  make webapp     - Frontend + Backend + SQLite + Web hosting 모두 자동 실행"
	@echo "                    (Docker 불필요, 모든 주소 자동 출력)"
	@echo ""
	@echo "🐳 DOCKER MODE (추천):"
	@echo "  make web        - Docker로 전체 스택 실행 (PostgreSQL)"
	@echo ""
	@echo "📦 LOCAL MODE (빠른 개발):"
	@echo "  make dev        - 로컬 개발 서버 안내"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ============================================================================
# 🎯 ONE-COMMAND WEB-APP LAUNCHER
# ============================================================================
webapp: install ## 🚀 한 번에 모든 것 실행 (Frontend + Backend + SQLite + Web hosting)
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 Seoul Travel Agent - Full Stack Web-App Launcher"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "📦 Starting Backend (FastAPI + SQLite)..."
	@cd backend && . .venv/bin/activate && nohup uvicorn app.main:app --reload --port 8000 > ../backend.log 2>&1 & echo $$! > ../backend.pid
	@sleep 3
	@echo "✅ Backend started on http://localhost:8000"
	@echo ""
	@echo "📦 Starting Frontend (React Native Web)..."
	@cd frontend && nohup npm run web > ../frontend.log 2>&1 & echo $$! > ../frontend.pid
	@echo "⏳ Waiting for Expo to start (this may take 20-30 seconds)..."
	@sleep 25
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ 모든 서비스가 실행되었습니다!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🌐 Web App URLs:"
	@echo "   📱 Frontend:     http://localhost:8081"
	@echo "   🔧 Backend API:  http://localhost:8000"
	@echo "   📖 API Docs:     http://localhost:8000/api/docs"
	@echo "   📊 API Redoc:    http://localhost:8000/api/redoc"
	@echo ""
	@echo "📝 Logs:"
	@echo "   make logs-webapp     - 실시간 로그 보기"
	@echo "   tail -f backend.log  - Backend 로그"
	@echo "   tail -f frontend.log - Frontend 로그"
	@echo ""
	@echo "🛑 Stop:"
	@echo "   make stop-webapp     - 모든 서비스 중지"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

stop-webapp: ## 🛑 모든 로컬 서비스 중지
	@echo "🛑 Stopping all services..."
	@if [ -f backend.pid ]; then kill $$(cat backend.pid) 2>/dev/null || true; rm backend.pid; echo "✅ Backend stopped"; fi
	@if [ -f frontend.pid ]; then kill $$(cat frontend.pid) 2>/dev/null || true; rm frontend.pid; echo "✅ Frontend stopped"; fi
	@pkill -f "uvicorn app.main:app" 2>/dev/null || true
	@pkill -f "expo start --web" 2>/dev/null || true
	@pkill -f "react-native" 2>/dev/null || true
	@echo "✅ All services stopped!"

logs-webapp: ## 📝 실시간 로그 보기 (Backend + Frontend)
	@echo "📝 Showing logs (Ctrl+C to exit)..."
	@tail -f backend.log frontend.log

restart-webapp: stop-webapp webapp ## 🔄 모든 서비스 재시작

# ============================================================================
# 📦 LOCAL DEVELOPMENT (Fast - SQLite)
# ============================================================================
install: ## Install all dependencies locally (no Docker)
	@echo "📦 Installing backend dependencies..."
	@cd backend && uv pip install -e ".[dev]"
	@echo "📦 Installing frontend dependencies..."
	@cd frontend && npm install
	@echo "✅ All dependencies installed!"

dev: install ## Start local development servers (SQLite + hot reload)
	@echo "🚀 Starting local development..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:8081"
	@echo ""
	@echo "Run in separate terminals:"
	@echo "  Terminal 1: cd backend && make run"
	@echo "  Terminal 2: cd frontend && npm run web"
	@echo ""
	@echo "Or use: make webapp (자동 실행)"

dev-backend: ## Run backend only (local SQLite)
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000 --log-level info

dev-frontend: ## Run frontend only (local)
	cd frontend && npm run web

# ============================================================================
# 🐳 DOCKER COMMANDS (Full Stack)
# ============================================================================
web: build ## 🚀 웹 뷰 테스트 (Docker) - 권장!
	@echo "🐳 Starting services with Docker..."
	docker-compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo ""
	@echo "📱 Web App:  http://localhost:3000"
	@echo "🔧 Backend:  http://localhost:8000"
	@echo "📖 API Docs: http://localhost:8000/api/docs"
	@echo ""
	@echo "📝 Logs: make logs"
	@echo "🛑 Stop:  make down"

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
