# Seoul Travel Agent - Project Structure & Analysis

**Analysis Date:** 2025-11-05  
**Project Status:** Active Development (MVP Phase)  
**Branch:** master (clean status)

---

## 1. PROJECT OVERVIEW

### Purpose
AI-powered Seoul travel planning assistant with React Native + FastAPI backend integration for Korean tourism data.

### Key Objective (SEO-33 Context)
Integrate Seoul Tourism OpenAPI with three main datasets:
- **TbVwNature** - Natural attractions & parks
- **TbVwRestaurants** - Dining establishments 
- **TbVwAttractions** - Tourist attractions & POIs

### Tech Stack
- **Frontend:** React Native 0.81 + Expo 54 + NativeWind + TypeScript
- **Backend:** FastAPI + SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **AI Integration:** OpenAI (GPT-4) or Anthropic Claude
- **Package Management:** uv (ultra-fast Python PM)
- **Environment:** Docker support with docker-compose

---

## 2. PROJECT DIRECTORY STRUCTURE

```
seoul-travel-agent/
├── .claude/                           # Claude Code Integration
│   └── skills/                        # Custom skills & utilities
│       ├── issue-workflow-manager/    # Linear issue lifecycle management
│       ├── webapp-testing/            # Playwright-based E2E testing
│       ├── skill-creator/             # Skill development guide
│       └── pyproject.toml             # Shared skill dependencies
│
├── backend/                           # FastAPI Application
│   ├── app/
│   │   ├── main.py                    # FastAPI app factory & router registration
│   │   ├── config.py                  # Environment settings (Pydantic)
│   │   ├── database.py                # SQLAlchemy setup & session management
│   │   │
│   │   ├── ai/                        # AI Domain Module
│   │   │   ├── ai_router.py           # Conversation & chat endpoints
│   │   │   ├── ai_schemas.py          # Pydantic models (request/response)
│   │   │   ├── ai_service.py          # LLM integration logic (OpenAI/Anthropic)
│   │   │   ├── models.py              # SQLAlchemy: Conversation, Message
│   │   │   ├── prompts.py             # Seoul expert system prompt
│   │   │   └── __init__.py
│   │   │
│   │   ├── auth/                      # Authentication Domain Module
│   │   │   ├── auth_router.py         # Auth endpoints (login/register)
│   │   │   ├── auth_schemas.py        # User schemas
│   │   │   ├── models.py              # SQLAlchemy: User model
│   │   │   └── __init__.py
│   │   │
│   │   ├── plan/                      # Travel Plans Domain Module
│   │   │   ├── plan_router.py         # CRUD endpoints for travel plans
│   │   │   ├── plan_schemas.py        # Travel plan Pydantic models
│   │   │   ├── models.py              # SQLAlchemy: TravelPlan model
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── pyproject.toml                 # Python dependencies (uv)
│   ├── Dockerfile                     # Container image definition
│   ├── Makefile                       # Backend-specific commands
│   ├── CLAUDE.md                      # Backend development guide
│   └── README.md
│
├── frontend/                          # React Native Web App
│   ├── src/
│   │   ├── screens/                   # Screen components
│   │   │   ├── HomeScreen.tsx
│   │   │   ├── ChatScreen.tsx
│   │   │   ├── ConversationListScreen.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── components/                # Reusable UI components
│   │   │   ├── ui/                    # Base components (button, card, input, etc)
│   │   │   ├── chat/                  # Chat-specific components
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   ├── MessageInput.tsx
│   │   │   │   ├── StreamingIndicator.tsx
│   │   │   │   └── index.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── contexts/                  # State management (React Context)
│   │   │   ├── ChatContext.tsx        # Chat state management
│   │   │   └── index.ts
│   │   │
│   │   ├── hooks/                     # Custom hooks
│   │   │   ├── useChat.ts             # Chat logic hook
│   │   │   └── index.ts
│   │   │
│   │   ├── services/                  # API layer
│   │   │   ├── api/
│   │   │   │   ├── chat.ts            # Chat API client
│   │   │   │   └── index.ts
│   │   │   └── index.ts
│   │   │
│   │   ├── types/                     # TypeScript type definitions
│   │   │   ├── chat.ts                # Chat-related types
│   │   │   └── index.ts
│   │   │
│   │   ├── lib/                       # Utility functions
│   │   │   ├── utils.ts
│   │   │   ├── icons/
│   │   │   └── index.ts
│   │   │
│   │   └── App.tsx                    # Root component
│   │
│   ├── app.json                       # Expo config
│   ├── App.tsx                        # Entry point
│   ├── package.json                   # Node dependencies
│   ├── tsconfig.json                  # TypeScript config
│   ├── tailwind.config.js             # Tailwind CSS config
│   ├── metro.config.js                # Metro bundler config
│   ├── Dockerfile                     # Container image
│   ├── README.md                      # Frontend guide
│   ├── README_STRUCTURE.md            # Detailed structure doc
│   └── babel.config.js
│
├── docker-compose.yml                 # Multi-container orchestration
├── Makefile                           # Root-level make commands
├── README.md                          # Project overview
└── .env.docker                        # Docker environment config

```

---

## 3. CURRENT DATA MODELS

### 3.1 User Model (auth/models.py)

```python
class User(Base):
    __tablename__ = "users"
    
    id: int (PK)
    email: str (unique)
    hashed_password: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - plans: List[TravelPlan]
    - conversations: List[Conversation]
```

### 3.2 Conversation Model (ai/models.py)

```python
class Conversation(Base):
    __tablename__ = "conversations"
    
    id: int (PK)
    user_id: int (FK → users)
    travel_plan_id: int (FK → travel_plans, nullable)
    title: str
    status: str ("active" | "completed" | "archived")
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - user: User
    - travel_plan: TravelPlan
    - messages: List[Message]
```

### 3.3 Message Model (ai/models.py)

```python
class Message(Base):
    __tablename__ = "messages"
    
    id: int (PK)
    conversation_id: int (FK → conversations)
    role: str ("user" | "assistant" | "system")
    content: str (Text)
    model: str (nullable) - e.g., "gpt-4", "claude-3-sonnet"
    tokens_used: int (nullable)
    finish_reason: str (nullable)
    created_at: datetime
    
    Relationships:
    - conversation: Conversation
```

### 3.4 TravelPlan Model (plan/models.py)

```python
class TravelPlan(Base):
    __tablename__ = "travel_plans"
    
    id: int (PK)
    user_id: int (FK → users)
    conversation_id: int (FK → conversations, nullable)
    title: str
    description: str (Text)
    itinerary: dict (JSON) - AI-generated itinerary
    recommendations: dict (JSON) - Places, restaurants, activities
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    
    Relationships:
    - user: User
    - conversation: Conversation (one-to-one)
```

---

## 4. API ENDPOINTS (CURRENT)

### 4.1 AI Routes (`/api/ai`)

**Conversations:**
- `POST /api/ai/conversations` - Create new conversation with initial message
- `GET /api/ai/conversations` - List all conversations (user-scoped)
- `GET /api/ai/conversations/{id}` - Get conversation with full history
- `DELETE /api/ai/conversations/{id}` - Delete conversation

**Messages:**
- `POST /api/ai/conversations/{id}/messages` - Send message & get response
- `POST /api/ai/conversations/{id}/messages/stream` - SSE streaming response

**Recommendations:**
- `POST /api/ai/recommendations` - Get AI travel recommendations (legacy)

### 4.2 Plans Routes (`/api/plans`)

- `GET /api/plans/` - List user's plans
- `POST /api/plans/` - Create new plan
- `GET /api/plans/{plan_id}` - Get specific plan
- `PATCH /api/plans/{plan_id}` - Update plan
- `DELETE /api/plans/{plan_id}` - Delete plan

**Status:** Routes exist but most CRUD operations are TODO

### 4.3 Auth Routes (`/api/auth`)

- TODO - authentication endpoints not yet fully implemented

### 4.4 Health Check

- `GET /api/health` - Health check endpoint

---

## 5. API INTEGRATION GAPS (For SEO-33 Implementation)

### 5.1 Missing External API Integration

**Current State:**
- No HTTP client library in dependencies (requests/httpx/aiohttp missing)
- AI service has mock recommendations returning hardcoded data
- No Seoul Tourism OpenAPI integration

**Recommendation Endpoint (Current Mock):**
```python
async def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """Get AI-powered travel recommendations."""
    # TODO: Implement LLM-based recommendation logic
    return RecommendationResponse(
        places=[{"name": "Gyeongbokgung Palace", ...}],
        restaurants=[{"name": "Gwangjang Market", ...}],
        activities=[{"name": "Han River Cruise", ...}],
    )
```

### 5.2 SEO-33 Issue Context

**Referenced in:** `/home/whdgn/seoul-travel-agent/.claude/skills/issue-workflow-manager/templates/issues/feature.md`

Example template shows SEO-33 would be created for implementing LangGraph-based Agent with TourAPI integration. The issue template demonstrates the project structure for:
- LangGraph StateGraph workflow
- TourAPI (version 4.0) data integration
- PostgreSQL state checkpointing
- FastAPI SSE streaming
- Implementation location: `backend/app/agents/workflow.py`

---

## 6. FRONTEND ARCHITECTURE

### 6.1 Chat Service Layer (services/api/chat.ts)

**Key Functions:**
```typescript
createConversation(data: CreateConversationRequest): Promise<CreateConversationResponse>
getConversation(id: string): Promise<Conversation>
getConversations(): Promise<ConversationListItem[]>
streamChatMessage(conversationId: string, data: SendMessageRequest): AsyncGenerator<StreamChunk>
sendMessage(conversationId: string, data: SendMessageRequest): Promise<{message: string}>
generatePlan(conversationId: string, data?: GeneratePlanRequest): Promise<GeneratePlanResponse>
deleteConversation(id: string): Promise<void>
```

**API Base URL:** `process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000'`

### 6.2 State Management

Uses React Context API (ChatContext.tsx) instead of Redux/Zustand for simplicity.

### 6.3 UI Components

- Built with TypeScript + NativeWind (Tailwind CSS for React Native)
- shadcn/ui-inspired component library (button, card, input, separator, text)
- Custom chat components: MessageBubble, MessageInput, StreamingIndicator

---

## 7. TECHNOLOGY STACK DETAILS

### Backend Dependencies

```
Core Framework:
- fastapi>=0.115.0
- uvicorn[standard]>=0.32.0
- pydantic[email]>=2.9.0
- pydantic-settings>=2.6.0

Database:
- sqlalchemy>=2.0.36
- aiosqlite>=0.20.0
- asyncpg>=0.30.0
- alembic>=1.14.0

Authentication:
- python-jose[cryptography]>=3.3.0
- passlib[bcrypt]>=1.7.4

AI/LLM:
- openai>=1.54.0
- anthropic>=0.39.0

Utilities:
- python-multipart>=0.0.12
- python-dotenv>=1.0.1

Dev Dependencies:
- pytest>=8.3.0
- pytest-asyncio>=0.24.0
- httpx>=0.27.0
- ruff>=0.7.0
- mypy>=1.13.0
```

**Missing for OpenAPI Integration:**
- httpx (async HTTP) or aiohttp
- requests (sync HTTP) 
- openapi-python-client or similar codegen tools

### Frontend Dependencies

```
Key Packages:
- react-native 0.81
- expo 54
- typescript
- nativewind (Tailwind CSS)
- @react-navigation/* (navigation)
- react-native-svg, react-native-skia

Development:
- expo-router
- jest
- @testing-library/react-native
```

---

## 8. CONFIGURATION MANAGEMENT

### Backend Settings (app/config.py)

```python
Settings(pydantic-settings):
    APP_NAME: str = "Seoul Travel Agent"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8081"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./seoul_travel.db"
    
    # AI/LLM
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Auth
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
```

**Environment Variables:** Loaded from `.env` file (pydantic-settings)

### Docker Environment (.env.docker)

- Configures PostgreSQL connection
- Sets appropriate API keys for production

---

## 9. DEVELOPMENT WORKFLOW

### Quick Start Commands

```bash
# One-command full stack (recommended)
make webapp

# Docker deployment (with PostgreSQL)
make web

# Local development (fast iteration)
make install
make dev-backend  # Terminal 1
make dev-frontend # Terminal 2
```

### Available Make Commands

**Frontend/Backend:**
- `make install` - Install dependencies (uv + npm)
- `make dev-backend` - Run FastAPI dev server (reload on changes)
- `make dev-frontend` - Run Expo web dev server

**Docker:**
- `make build` - Build images
- `make up` - Start services
- `make down` - Stop services
- `make logs` - View logs

**Quality:**
- `make test` - Run tests
- `make lint` - Lint code
- `make format` - Format code

**Database (Docker):**
- `make db-migrate` - Create migration
- `make db-upgrade` - Apply migrations
- `make db-shell` - Access PostgreSQL

---

## 10. SEO-33 IMPLEMENTATION ROADMAP

### Prerequisites
1. Add async HTTP client (httpx recommended)
2. Create OpenAPI service module: `backend/app/openapi/` or `backend/app/services/`
3. Design schema mappers from Seoul Tourism OpenAPI to internal models

### Implementation Plan

**Phase 1: OpenAPI Integration Foundation**
- Create `backend/app/openapi/` module with:
  - `client.py` - Async HTTP client wrapper
  - `schemas.py` - OpenAPI response models (TbVwNature, TbVwRestaurants, TbVwAttractions)
  - `service.py` - Business logic to fetch & cache data
  
**Phase 2: Data Models Enhancement**
- Extend `TravelPlan.recommendations` JSON schema to include:
  - `attractions: List[AttractionDetail]` from TbVwAttractions
  - `restaurants: List[RestaurantDetail]` from TbVwRestaurants
  - `nature: List[NatureAttractionDetail]` from TbVwNature
  
**Phase 3: API Endpoint Integration**
- Add endpoints to leverage OpenAPI data:
  - `POST /api/plans/generate-from-preferences` - Use OpenAPI data + AI
  - `GET /api/attractions/nearby` - Filter TbVwAttractions by location
  - `GET /api/restaurants/by-type` - Filter TbVwRestaurants by cuisine
  - `GET /api/nature-spots/by-keyword` - Search TbVwNature
  
**Phase 4: Frontend Integration**
- Update ChatContext to provide OpenAPI-enhanced recommendations
- Create recommendation cards showing:
  - Real Seoul data (opening hours, addresses, phone)
  - AI-curated explanations
  - Integration with travel plan generation

### Critical Notes

1. **Rate Limiting:** Seoul Tourism OpenAPI likely has request limits
   - Implement caching layer (Redis recommended for production)
   - Consider batch fetching during off-peak hours

2. **Data Freshness:** Tourism data changes seasonally
   - Implement TTL for cached data
   - Provide manual refresh endpoint

3. **Error Handling:** External API failures shouldn't break user experience
   - Fallback to LLM-only recommendations
   - Graceful degradation

---

## 11. CLAUDE CODE INTEGRATION

### Custom Skills

**issue-workflow-manager**
- Linear issue lifecycle management
- Feature/bug/task templates with SEO-33 pattern examples
- Git workflow integration

**webapp-testing**
- Playwright-based E2E testing for React Native web
- Automated server management (backend + frontend)
- DOM element discovery and interaction

**skill-creator**
- Guide for creating new custom skills

### Usage
```bash
# Run skills from project root
uv run python .claude/skills/webapp-testing/scripts/with_server.py
uv run python .claude/skills/issue-workflow-manager/...
```

---

## 12. KEY FILES REFERENCE

| File | Purpose | Status |
|------|---------|--------|
| `backend/app/main.py` | FastAPI app factory | Complete |
| `backend/app/database.py` | SQLAlchemy setup | Complete |
| `backend/app/ai/ai_service.py` | LLM integration | Partial (mock data) |
| `backend/app/plan/models.py` | TravelPlan schema | Complete |
| `frontend/src/services/api/chat.ts` | API client layer | Complete |
| `frontend/src/contexts/ChatContext.tsx` | State management | Complete |
| `.claude/skills/issue-workflow-manager/` | SEO-33 workflow reference | Complete |

---

## 13. IMPORTANT NOTES FOR SEO-33

1. **SEO-33 is referenced in feature template** at `.claude/skills/issue-workflow-manager/templates/issues/feature.md`
   - Demonstrates expected structure for complex features
   - Shows pattern: Korean title + original tech names (TourAPI, LangGraph, PostgreSQL)

2. **No existing OpenAPI integration** - completely greenfield opportunity
   - No existing HTTP client libraries
   - Mock data still in use
   - Recommendations endpoint still returns hardcoded values

3. **Recommended approach for MVP:**
   - Simplify to essential TourAPI endpoints (no LangGraph initially)
   - Focus on static data integration first (Nature, Restaurants, Attractions)
   - Plan LangGraph Agent work for Phase 2

4. **Database is ready** for enhancement:
   - TravelPlan.recommendations can store OpenAPI data as JSON
   - Message history supports context for iterative planning
   - No migration conflicts (using Alembic-ready SQLAlchemy setup)

---

**Report Generated:** 2025-11-05  
**Analysis Completeness:** Comprehensive - covering structure, models, APIs, tech stack, and SEO-33 context
