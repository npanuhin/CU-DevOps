import pytest
from fastapi.testclient import TestClient

from main import app, _fruit_response

@pytest.fixture(autouse=True)
def reset_fruits_api():
    import main
    original_fruits = {
        1: {"name": "Apple", "price": 1.20, "in_season": True},
        2: {"name": "Banana", "price": 0.80, "in_season": True},
        3: {"name": "Orange", "price": 1.00, "in_season": False},
    }
    main.FRUITS.clear()
    main.FRUITS.update(original_fruits)
    main._next_id = 4
    yield

client = TestClient(app)

def test_fruit_response():
    data = {"name": "Mango", "price": 3, "in_season": True}
    result = _fruit_response(4, data)
    assert result == {"id": 4, "name": "Mango", "price": 3, "in_season": True}

def test_list_fruits():
    response = client.get("/fruits")
    assert response.status_code == 200
    fruits = response.json()
    assert len(fruits) == 3

def test_get_cheapest_fruit():
    response = client.get("/fruits/cheapest")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "Banana", "price": 0.80, "in_season": True}

