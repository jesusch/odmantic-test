import pytest
from app.main import Tree

pytestmark = pytest.mark.anyio


async def test_get_trees(client):
    response = await client.get("/trees/")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}

async def test_create_tree(client):
    tree = Tree(name="Tomato", average_size=0.1, discovery_year=1500)
    response = await client.put("/trees/", data=tree.model_dump_json())
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}

async def test_count_trees(client):
    response = await client.get("/trees/count")
    assert response.status_code == 200
    assert response.json() == 1


async def test_get_tree_by_id(client):
    tree = Tree(name="Tomato", average_size=0.1, discovery_year=1500)
    response = await client.get(f"/trees/{tree.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}