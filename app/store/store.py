from typing import Iterator

from app.models.fruit import FruitCreate, FruitUpdate, fruit_response


class FruitStore:
    """In-memory store for fruits, keyed by integer id."""

    def __init__(self) -> None:
        self._items: dict[int, dict] = {}
        self._next_id: int = 1

    def seed_defaults(self) -> None:
        """Populate the store with the default catalog. Useful at startup."""
        self._items = {
            1: {"name": "Apple", "price": 1.20, "in_season": True},
            2: {"name": "Banana", "price": 0.80, "in_season": True},
            3: {"name": "Orange", "price": 1.00, "in_season": False},
        }
        self._next_id = 4

    def reset(self) -> None:
        self._items.clear()
        self._next_id = 1

    def list(self, in_season: bool | None = None) -> list[dict]:
        items = [fruit_response(i, data) for i, data in self._items.items()]
        if in_season is not None:
            items = [f for f in items if f["in_season"] is in_season]
        return items

    def get(self, fruit_id: int) -> dict | None:
        data = self._items.get(fruit_id)
        if data is None:
            return None
        return fruit_response(fruit_id, data)

    def create(self, body: FruitCreate) -> dict:
        fruit_id = self._next_id
        self._next_id += 1
        data = {"name": body.name, "price": body.price, "in_season": body.in_season}
        self._items[fruit_id] = data
        return fruit_response(fruit_id, data)

    def update(self, fruit_id: int, body: FruitUpdate) -> dict | None:
        if fruit_id not in self._items:
            return None
        data = self._items[fruit_id].copy()
        if body.name is not None:
            data["name"] = body.name
        if body.price is not None:
            data["price"] = body.price
        if body.in_season is not None:
            data["in_season"] = body.in_season
        self._items[fruit_id] = data
        return fruit_response(fruit_id, data)

    def delete(self, fruit_id: int) -> bool:
        if fruit_id not in self._items:
            return False
        del self._items[fruit_id]
        return True

    def cheapest(self) -> dict | None:
        if not self._items:
            return None
        cheapest_id = min(self._items.keys(), key=lambda i: self._items[i]["price"])
        return fruit_response(cheapest_id, self._items[cheapest_id])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[dict]:
        return iter(self.list())


store = FruitStore()
store.seed_defaults()
