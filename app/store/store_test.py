import pytest

from app.models.fruit import FruitCreate, FruitUpdate
from app.store.store import FruitStore


@pytest.fixture()
def store() -> FruitStore:
    s = FruitStore()
    s.seed_defaults()
    return s


def test_seed_defaults_populates_three_fruits(store: FruitStore) -> None:
    assert len(store) == 3
    names = {f["name"] for f in store.list()}
    assert names == {"Apple", "Banana", "Orange"}


def test_create_assigns_increasing_ids(store: FruitStore) -> None:
    a = store.create(FruitCreate(name="Mango", price=3.0, in_season=True))
    b = store.create(FruitCreate(name="Pear", price=2.0, in_season=False))
    assert b["id"] == a["id"] + 1
    assert a["name"] == "Mango"


def test_get_returns_none_for_missing_id(store: FruitStore) -> None:
    assert store.get(9999) is None


def test_get_returns_fruit_when_present(store: FruitStore) -> None:
    fruit = store.get(1)
    assert fruit is not None
    assert fruit["name"] == "Apple"
    assert fruit["id"] == 1


def test_update_returns_none_when_missing(store: FruitStore) -> None:
    assert store.update(9999, FruitUpdate(price=10.0)) is None


def test_update_partial_fields(store: FruitStore) -> None:
    updated = store.update(1, FruitUpdate(price=9.99))
    assert updated is not None
    assert updated["price"] == 9.99
    assert updated["name"] == "Apple"  # unchanged


def test_delete_returns_true_then_false(store: FruitStore) -> None:
    assert store.delete(1) is True
    assert store.delete(1) is False
    assert store.get(1) is None


def test_list_filters_by_in_season(store: FruitStore) -> None:
    in_season = store.list(in_season=True)
    out_of_season = store.list(in_season=False)
    assert all(f["in_season"] is True for f in in_season)
    assert all(f["in_season"] is False for f in out_of_season)
    assert len(in_season) + len(out_of_season) == len(store)


def test_cheapest_returns_lowest_price(store: FruitStore) -> None:
    cheapest = store.cheapest()
    assert cheapest is not None
    assert cheapest["name"] == "Banana"  # 0.80


def test_cheapest_returns_none_when_empty() -> None:
    s = FruitStore()
    assert s.cheapest() is None
