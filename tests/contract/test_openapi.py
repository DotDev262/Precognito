import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_openapi_schema_validity(client: AsyncClient):
    """
    Test that the FastAPI application generates a valid OpenAPI JSON schema.
    """
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert "components" in schema
    
    # Check for core paths presence in contract
    assert "/health" in schema["paths"]
    assert "/assets" in schema["paths"]
    assert "/anomalies" in schema["paths"]

@pytest.mark.asyncio
async def test_endpoint_schema_match(auth_client: AsyncClient):
    """
    Verify that an endpoint response structure matches the expected basic keys.
    """
    response = await auth_client.get("/admin-reporting/health")
    assert response.status_code == 200
    data = response.json()
    
    # These keys are defined in SystemHealthResponse Pydantic model
    expected_keys = ["status", "uptime_seconds", "active_user_sessions", "cpu_usage_percent", "memory_usage_percent"]
    for key in expected_keys:
        assert key in data
