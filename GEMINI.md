# Project Overview

This is a full-stack application for a Seoul travel agent. It consists of a React Native frontend and a FastAPI backend.

- **Frontend:** The frontend is a React Native application built with Expo. It uses TypeScript, NativeWind for styling, and Zustand for state management. The app includes screens for viewing the home page, managing travel plans, and adjusting settings.

- **Backend:** The backend is a Python-based API built with FastAPI. It uses SQLAlchemy for database interactions, Pydantic for data validation, and includes features for AI-powered travel planning, user authentication, and managing travel plans. It's set up to work with both SQLite for local development and PostgreSQL for production. It utilizes LangChain and OpenAI for its AI features.

- **Architecture:** The project is set up as a monorepo with separate `frontend` and `backend` directories. It's designed to be run either locally or with Docker. The `docker-compose.yml` file defines services for the database, backend, and frontend.

# Building and Running

The project can be run locally or using Docker. The `Makefile` provides convenient commands for both.

**One-Command Quick Start (Recommended):**

This command starts all services (frontend, backend with SQLite) automatically.

```bash
make webapp
```

After about 30 seconds, the application will be available at `http://localhost:8081`.

**Docker Mode:**

This is the recommended way to run the full stack with PostgreSQL.

```bash
# Build and start all services
make web

# Stop all services
make down
```

The web app will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

**Local Development:**

For more granular control, you can run the frontend and backend separately.

1.  **Install Dependencies:**
    ```bash
    make install
    ```

2.  **Run Backend:**
    ```bash
    make dev-backend
    ```

3.  **Run Frontend:**
    ```bash
    make dev-frontend
    ```

# Development Conventions

## Testing

-   **Run all tests:**
    ```bash
    make test
    ```
    *Note: Frontend tests are not yet configured.*

-   **Run backend tests:**
    ```bash
    make test-backend
    ```

## Linting and Formatting

-   **Lint all code:**
    ```bash
    make lint
    ```

-   **Format all code:**
    ```bash
    make format
    ```

## API Type Generation

The frontend uses `openapi-typescript` to generate TypeScript types from the backend's OpenAPI specification. This ensures type safety between the frontend and backend.

-   **Generate types once:**
    ```bash
    npm run types:generate
    ```

-   **Watch for changes and regenerate types:**
    ```bash
    npm run types:watch
    ```
