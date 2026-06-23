from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from routes import get_db
import pytest
from httpx import AsyncClient, ASGITransport

DATABSE_URL = "postgresql+asyncpg://creditcore:creditcore@localhost:5432/creditcore"

async def override_get_db():
    engine = create_async_engine(DATABSE_URL)
    AsyncTestSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncTestSession() as session:
        yield session
    await engine.dispose()

app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_application():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/applications",
            json={"customer_id": "test_cust", "amount": 1000, "purpose": "test"},
            headers={"idempotency-key": "test-key-001"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == "test_cust"
        assert data["status"] == "draft"

@pytest.mark.asyncio
async def test_idempotency():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response1 = await client.post(
            "/applications",
            json={"customer_id": "test_cust", "amount": 1000, "purpose": "test"},
            headers={"idempotency-key": "test-key-002"}
        )
        response2 = await client.post(
            "/applications",
            json={"customer_id": "test_cust", "amount": 1000, "purpose": "test"},
            headers={"idempotency-key": "test-key-002"}
        )
    assert response1.json()["id"] == response2.json()["id"]

@pytest.mark.asyncio
async def test_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/applications/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404