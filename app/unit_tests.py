import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello, World!"}

def test_create_item_success():
    item = {"id": 1, "name": "foo", "price": 9.99}
    resp = client.post("/items/", json=item)
    assert resp.status_code == 200
    assert resp.json()["received"] == item

def test_create_item_invalid_price():
    item = {"id": 2, "name": "bar", "price": -1}
    resp = client.post("/items/", json=item)
    assert resp.status_code == 422
