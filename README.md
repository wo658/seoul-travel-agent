# Seoul Travel Agent

AI-powered travel planning platform for Seoul

## Project Structure

```
seoul-travel-agent/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   └── seoul_travel/
│   │       ├── ai/         # AI domain (LLM integration)
│   │       ├── auth/       # Authentication domain
│   │       ├── plan/       # Travel plan domain
│   │       ├── database/   # Database models
│   │       ├── config/     # Configuration
│   │       └── main.py     # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # React Native app
└── docker-compose.yml       # Docker orchestration
```

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **LLM**: OpenAI / Anthropic Claude

### Frontend
- **Framework**: React Native (Expo)

## Quick Start

### Prerequisites

**Backend:**
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via Homebrew
brew install uv
```

### Option 1: Local Development (Recommended - Fast!)

**SQLite + Hot Reload - No Docker needed!**

```bash
# Install all dependencies
make install

# Run in separate terminals:
# Terminal 1 - Backend
make dev-backend

# Terminal 2 - Frontend
make dev-frontend
```

**Quick Commands:**
```bash
make help           # Show all commands
make install        # Install all dependencies
make dev-backend    # Run backend only
make dev-frontend   # Run frontend only
make test           # Run tests
make lint           # Check code quality
```

### Option 2: Docker (Full Stack - Production-like)

**PostgreSQL + Full Integration**

```bash
# Build and start all services
make up

# View logs
make logs
make logs-backend   # Backend only
make logs-frontend  # Frontend only

# Stop services
make down
```

**Docker Commands:**
```bash
make help           # Show all commands
make up             # Start all services
make down           # Stop all services
make restart        # Restart services
make ps             # Show status
make backend-shell  # Access backend container
make db-shell       # Access PostgreSQL
```

### Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **PostgreSQL** (Docker only): localhost:5432

## Development Workflows

### Local Development (⚡ Fastest)
```bash
make install        # One-time setup
make dev-backend    # Terminal 1
make dev-frontend   # Terminal 2
```
- ✅ No Docker needed
- ✅ SQLite database (auto-created)
- ✅ Hot reload on both stacks
- ✅ 10-100x faster with uv
- ✅ Best for rapid prototyping

### Docker Development (🐳 Production-like)
```bash
make up            # Start everything
make logs          # Monitor logs
make down          # Stop when done
```
- ✅ Full stack integration
- ✅ PostgreSQL database
- ✅ Container isolation
- ✅ Matches production environment
- ✅ Best for integration testing

### API Endpoints

#### Health Check
- `GET /api/health`

#### AI Domain
- `POST /api/ai/chat` - Chat with AI assistant
- `POST /api/ai/recommendations` - Get travel recommendations

#### Auth Domain
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

#### Plan Domain
- `GET /api/plans/` - List travel plans
- `POST /api/plans/` - Create plan
- `GET /api/plans/{id}` - Get plan
- `PATCH /api/plans/{id}` - Update plan
- `DELETE /api/plans/{id}` - Delete plan

## Domain Architecture

Following Netflix Dispatch patterns:

### AI Domain
- LLM integration (OpenAI, Anthropic)
- Travel recommendations
- Chat interface

### Auth Domain
- User registration/login
- JWT authentication
- User management

### Plan Domain
- Travel plan CRUD
- Itinerary management
- User plans relationship

## TODO

- [ ] Implement actual LLM integration
- [ ] Add database migrations (Alembic)
- [ ] Implement authentication logic
- [ ] Add tests
- [ ] Frontend integration
