import httpx
import pytest

BASE_URL = "http://localhost:8000"

def test_integration_read_root():
    resp = httpx.get(f"{BASE_URL}/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello, World!"}

@pytest.mark.parametrize("item, expected_status", [
    ({"id":1, "name":"foo", "price":9.99}, 200),
    ({"id":2, "name":"bar", "price":-1}, 422),
])
def test_integration_items(item, expected_status):
    resp = httpx.post(f"{BASE_URL}/items/", json=item)
    assert resp.status_code == expected_status