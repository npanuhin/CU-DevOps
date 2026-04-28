"""Integration tests: real HTTP client against a running FruitAPI.

Run a server first (locally: `uvicorn main:app` or via Docker on port 8000),
then `pytest tests`. BASE_URL can be overridden via env var.
"""
import os

import httpx
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")


@pytest.fixture()
def client():
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as c:
        yield c


def test_health(client: httpx.Client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_full_crud_lifecycle(client: httpx.Client) -> None:
    # CREATE
    response = client.post(
        "/fruits", json={"name": "Mango", "price": 3.0, "in_season": True}
    )
    assert response.status_code == 200
    created = response.json()
    assert created["name"] == "Mango"
    fruit_id = created["id"]

    # READ
    response = client.get(f"/fruits/{fruit_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Mango"

    # UPDATE (partial)
    response = client.put(f"/fruits/{fruit_id}", json={"price": 2.5})
    assert response.status_code == 200
    body = response.json()
    assert body["price"] == 2.5
    assert body["name"] == "Mango"

    # DELETE
    response = client.delete(f"/fruits/{fruit_id}")
    assert response.status_code == 204

    # READ again -> 404
    response = client.get(f"/fruits/{fruit_id}")
    assert response.status_code == 404


def test_cheapest_consistency(client: httpx.Client) -> None:
    cheapest = client.get("/fruits/cheapest")
    assert cheapest.status_code == 200

    all_fruits = client.get("/fruits")
    assert all_fruits.status_code == 200
    min_price = min(f["price"] for f in all_fruits.json())

    assert cheapest.json()["price"] == min_price


def test_post_then_appears_in_list(client: httpx.Client) -> None:
    """Extra scenario: a created fruit shows up in GET /fruits, then is cleaned up."""
    response = client.post(
        "/fruits", json={"name": "Kiwi", "price": 1.5, "in_season": True}
    )
    assert response.status_code == 200
    fruit_id = response.json()["id"]

    try:
        all_fruits = client.get("/fruits").json()
        assert any(f["id"] == fruit_id and f["name"] == "Kiwi" for f in all_fruits)
    finally:
        client.delete(f"/fruits/{fruit_id}")
