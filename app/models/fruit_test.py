from app.models.fruit import fruit_response


def test_fruit_response_builds_id_plus_fields():
    data = {"name": "Mango", "price": 3, "in_season": True}
    result = fruit_response(4, data)
    assert result == {"id": 4, "name": "Mango", "price": 3, "in_season": True}


def test_fruit_response_does_not_mutate_input():
    data = {"name": "Mango", "price": 3, "in_season": True}
    fruit_response(4, data)
    assert "id" not in data
