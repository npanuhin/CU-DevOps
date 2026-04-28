"""Integration tests: real FastAPI app + real in-memory store via TestClient."""
import pytest
from fastapi.testclient import TestClient

from app.app import create_app
from app.store.store import store as shared_store


@pytest.fixture()
def client() -> TestClient:
    shared_store.reset()
    shared_store.seed_defaults()
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_fruits(client: TestClient) -> None:
    response = client.get("/fruits")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_fruits_in_season_filter(client: TestClient) -> None:
    response = client.get("/fruits", params={"in_season": "false"})
    assert response.status_code == 200
    fruits = response.json()
    assert len(fruits) == 1
    assert fruits[0]["name"] == "Orange"


def test_full_crud_lifecycle(client: TestClient) -> None:
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
    assert response.content == b""

    # READ again -> 404
    response = client.get(f"/fruits/{fruit_id}")
    assert response.status_code == 404


def test_get_one_404(client: TestClient) -> None:
    response = client.get("/fruits/424242")
    assert response.status_code == 404


def test_update_404(client: TestClient) -> None:
    response = client.put("/fruits/424242", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_404(client: TestClient) -> None:
    response = client.delete("/fruits/424242")
    assert response.status_code == 404


def test_cheapest_fruit(client: TestClient) -> None:
    response = client.get("/fruits/cheapest")
    assert response.status_code == 200
    cheapest = response.json()

    all_fruits = client.get("/fruits").json()
    assert cheapest["price"] == min(f["price"] for f in all_fruits)
