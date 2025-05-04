import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_book():
    response = client.post("/v1/books", json={
        "title": "Test Book",
        "author_id": "123",
        "price": 29.99,
        "stock": 100
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"