import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_basic_api_reachability(client: AsyncClient):
    """
    Smoke test: Ensure the API is up and responding to health check.
    """
    response = await client.get("/health")
    assert response.status_code in [200, 503] # 503 is acceptable for smoke if DBs aren't up yet

@pytest.mark.asyncio
async def test_static_files_reachability(client: AsyncClient):
    """
    Smoke test: Ensure docs are accessible.
    """
    response = await client.get("/docs")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_unauthenticated_redirection(client: AsyncClient):
    """
    Smoke test: Ensure security middleware is active.
    """
    response = await client.get("/assets")
    assert response.status_code == 401
