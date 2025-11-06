"""Test API endpoints integration."""

import pytest


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns healthy status."""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "seoul-travel-agent"


class TestAuthEndpoints:
    """Test authentication endpoints."""

    def test_auth_router_registered(self, client):
        """Test that auth router is registered."""
        # Try to access auth endpoint (should return 405 or 422, not 404)
        response = client.get("/api/auth/")
        assert response.status_code != 404


class TestPlanEndpoints:
    """Test plan endpoints."""

    def test_plan_router_registered(self, client):
        """Test that plan router is registered."""
        # Try to access plan endpoint
        response = client.get("/api/plans/")
        # Should not return 404 (router is registered)
        assert response.status_code != 404


class TestAIEndpoints:
    """Test AI endpoints."""

    def test_ai_router_registered(self, client):
        """Test that AI router is registered."""
        # Try to access AI endpoint
        response = client.get("/api/ai/")
        # Should not return 404 (router is registered)
        assert response.status_code != 404

    def test_generate_plan_endpoint_exists(self, client):
        """Test that plan generation endpoint exists."""
        # POST request without proper data should return 422, not 404
        response = client.post("/api/ai/plans/generate", json={})
        assert response.status_code != 404


class TestCORSMiddleware:
    """Test CORS middleware configuration."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )

        # Check CORS headers are present
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation endpoints."""

    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON is available."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_swagger_docs_available(self, client):
        """Test that Swagger UI docs are available."""
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Test that ReDoc documentation is available."""
        response = client.get("/api/redoc")
        assert response.status_code == 200
