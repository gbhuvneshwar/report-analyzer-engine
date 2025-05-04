import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_author():
    response = client.post("/v1/authors", json={
        "name": "Test Author",
        "bio": "Bio"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Author"