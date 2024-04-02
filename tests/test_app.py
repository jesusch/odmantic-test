import pytest
from httpx import AsyncClient, ASGITransport
from odmantic import AIOEngine
from app.main import Item  # Import your FastAPI app here
# from yourapp.models import Item  # Adjust the import path according to your project structure

pytestmark = pytest.mark.asyncio




async def test_create_item(client):
    response = await client.post("/items/", json={"name": "Test Item", "description": "A test item", "price": 10.99, "in_stock": True})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

async def test_read_item(client, engine):
    item = Item(name="Test Item", description="A test item", price=10.99, in_stock=True)
    await engine.save(item)
    response = await client.get(f"/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"

async def test_read_items(client, engine):
    item1 = Item(name="Test Item 1", description="A test item", price=10.99, in_stock=True)
    item2 = Item(name="Test Item 2", description="Another test item", price=15.99, in_stock=False)
    await engine.save(item1)
    await engine.save(item2)
    response = await client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

async def test_update_item(client, engine):
    item = Item(name="Old Item", description="An item to be updated", price=9.99, in_stock=True)
    await engine.save(item)
    response = await client.put(f"/items/{item.id}", json={"name": "Updated Item", "description": "An updated test item", "price": 11.99, "in_stock": False})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"

async def test_delete_item(client, engine):
    item = Item(name="Item to Delete", description="This item will be deleted", price=19.99, in_stock=True)
    await engine.save(item)

    response = await client.delete(f"/items/{item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Item to Delete"
    # Verify item is deleted
    response = await client.get(f"/items/{item.id}")
    assert response.status_code == 404
