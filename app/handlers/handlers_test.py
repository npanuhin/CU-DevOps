"""Unit tests for handlers using a fake/isolated store (no real server)."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.handlers.handlers import build_router
from app.store.store import FruitStore


@pytest.fixture()
def client() -> TestClient:
    store = FruitStore()
    store.seed_defaults()
    app = FastAPI()
    app.include_router(build_router(store))
    return TestClient(app)


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_fruits_returns_seeded_three(client: TestClient) -> None:
    response = client.get("/fruits")
    assert response.status_code == 200
    fruits = response.json()
    assert len(fruits) == 3


def test_get_one_404_when_missing(client: TestClient) -> None:
    response = client.get("/fruits/9999")
    assert response.status_code == 404


def test_cheapest_endpoint(client: TestClient) -> None:
    response = client.get("/fruits/cheapest")
    assert response.status_code == 200
    assert response.json()["name"] == "Banana"


def test_update_404_when_missing(client: TestClient) -> None:
    response = client.put("/fruits/9999", json={"price": 1.0})
    assert response.status_code == 404


def test_delete_404_when_missing(client: TestClient) -> None:
    response = client.delete("/fruits/9999")
    assert response.status_code == 404


def test_cheapest_404_when_store_empty() -> None:
    empty_store = FruitStore()
    app = FastAPI()
    app.include_router(build_router(empty_store))
    response = TestClient(app).get("/fruits/cheapest")
    assert response.status_code == 404


def test_list_fruits_in_season_true(client: TestClient) -> None:
    response = client.get("/fruits", params={"in_season": "true"})
    assert response.status_code == 200
    fruits = response.json()
    assert all(f["in_season"] is True for f in fruits)
    assert {f["name"] for f in fruits} == {"Apple", "Banana"}


def test_list_fruits_in_season_false(client: TestClient) -> None:
    response = client.get("/fruits", params={"in_season": "false"})
    assert response.status_code == 200
    fruits = response.json()
    assert all(f["in_season"] is False for f in fruits)
    assert [f["name"] for f in fruits] == ["Orange"]


def test_post_missing_name_returns_422(client: TestClient) -> None:
    response = client.post("/fruits", json={"price": 1.0, "in_season": True})
    assert response.status_code == 422


def test_post_wrong_type_for_price_returns_422(client: TestClient) -> None:
    response = client.post(
        "/fruits", json={"name": "Mango", "price": "not-a-number", "in_season": True}
    )
    assert response.status_code == 422
