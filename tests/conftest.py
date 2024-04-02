import pytest
from httpx import AsyncClient, ASGITransport
from odmantic import AIOEngine
from app.main import app, get_database


async def mock_db():
    engine = AIOEngine()
    yield engine


@pytest.fixture()
async def engine():
    engine = AIOEngine()
    yield engine
    await engine.client.drop_database("test")


@pytest.fixture()
async def client():
    app.dependency_overrides[get_database] = mock_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

