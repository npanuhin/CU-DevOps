"""
Fruits API — complete version (after Module 1 homework).
Same as live_demo plus: GET /fruits/cheapest, GET /fruits?in_season=, PUT, DELETE, POST with JSON body.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Fruits API (complete)", version="0.2.0")


class FruitCreate(BaseModel):
    name: str
    price: float = 0.0
    in_season: bool = True


class FruitUpdate(BaseModel):
    name: str  = None
    price: float  = None
    in_season: bool  = None


# In-memory store: id -> {name, price, in_season}
FRUITS = {
    1: {"name": "Apple", "price": 1.20, "in_season": True},
    2: {"name": "Banana", "price": 0.80, "in_season": True},
    3: {"name": "Orange", "price": 1.00, "in_season": False},
}
_next_id = 4


def _fruit_response(fruit_id: int, data: dict) -> dict:
    return {"id": fruit_id, **data}


@app.get("/health")
def health():
    """Health check for load balancers / ECS."""
    return {"status": "ok"}


@app.get("/fruits/cheapest")
def get_cheapest_fruit():
    """Return the fruit with the lowest price. (Homework endpoint.)"""
    if not FRUITS:
        raise HTTPException(status_code=404, detail="No fruits")
    cheapest_id = min(FRUITS.keys(), key=lambda i: FRUITS[i]["price"])
    return _fruit_response(cheapest_id, FRUITS[cheapest_id])


@app.get("/fruits")
def list_fruits(
        in_season: bool = Query(None, description="Filter by in_season (true/false)"),
):
    """List all fruits. Optional filter: ?in_season=true or ?in_season=false."""
    items = [{"id": id_, **data} for id_, data in FRUITS.items()]
    if in_season is not None:
        items = [f for f in items if f["in_season"] is in_season]
    return items


@app.get("/fruits/{fruit_id:int}")
def get_fruit(fruit_id: int):
    """Get one fruit by id."""
    if fruit_id not in FRUITS:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return _fruit_response(fruit_id, FRUITS[fruit_id])


@app.post("/fruits")
def add_fruit(body: FruitCreate):
    """Add a new fruit (JSON body)."""
    global _next_id
    fruit_id = _next_id
    _next_id += 1
    data = {"name": body.name, "price": body.price, "in_season": body.in_season}
    FRUITS[fruit_id] = data
    return _fruit_response(fruit_id, data)


@app.put("/fruits/{fruit_id:int}")
def update_fruit(fruit_id: int, body: FruitUpdate):
    """Update a fruit (partial update)."""
    if fruit_id not in FRUITS:
        raise HTTPException(status_code=404, detail="Fruit not found")
    data = FRUITS[fruit_id].copy()
    if body.name is not None:
        data["name"] = body.name
    if body.price is not None:
        data["price"] = body.price
    if body.in_season is not None:
        data["in_season"] = body.in_season
    FRUITS[fruit_id] = data
    return _fruit_response(fruit_id, data)


@app.delete("/fruits/{fruit_id:int}", status_code=204)
def delete_fruit(fruit_id: int):
    """Delete a fruit."""
    if fruit_id not in FRUITS:
        raise HTTPException(status_code=404, detail="Fruit not found")
    del FRUITS[fruit_id]
