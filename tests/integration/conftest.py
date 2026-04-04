import pytest
import asyncio
from unittest.mock import MagicMock, patch
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator, Generator

from precognito.work_orders.database import Base, engine

# Mock database and influx before importing app
with patch("asyncpg.create_pool"), patch("influxdb_client.InfluxDBClient"):
    from precognito.api import app

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create all tables in the test database once per session."""
    Base.metadata.create_all(bind=engine)
    yield
    # We could drop tables here, but since it's a file-based sqlite,
    # it's usually fine to leave it or delete the file in clean-up

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provides a base test client for the FastAPI app."""
    app.db_pool = MagicMock()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

@pytest.fixture
async def auth_client(mock_admin_user) -> AsyncGenerator[AsyncClient, None]:
    """Provides an authenticated test client for the FastAPI app."""
    from precognito.auth import get_current_user
    app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def mock_admin_user():
    """Returns a mock admin user record."""
    return {
        "id": "user_123",
        "email": "admin@precognito.ai",
        "role": "ADMIN",
        "name": "Admin User"
    }

@pytest.fixture
def authenticated_admin(mocker, mock_admin_user):
    """Mocks the authentication dependency to return an admin user."""
    return mocker.patch("precognito.auth.get_current_user", return_value=mock_admin_user)
