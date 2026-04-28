from fastapi import APIRouter, HTTPException, Query, Response

from app.models.fruit import FruitCreate, FruitUpdate
from app.store.store import FruitStore, store as default_store


def build_router(store: FruitStore) -> APIRouter:
    """Build a router bound to a specific store. Lets tests inject a fake store."""
    router = APIRouter()

    @router.get("/health")
    def health():
        return {"status": "ok"}

    @router.get("/fruits/cheapest")
    def get_cheapest_fruit():
        cheapest = store.cheapest()
        if cheapest is None:
            raise HTTPException(status_code=404, detail="No fruits")
        return cheapest

    @router.get("/fruits")
    def list_fruits(
        in_season: bool | None = Query(None, description="Filter by in_season"),
    ):
        return store.list(in_season=in_season)

    @router.get("/fruits/{fruit_id:int}")
    def get_fruit(fruit_id: int):
        fruit = store.get(fruit_id)
        if fruit is None:
            raise HTTPException(status_code=404, detail="Fruit not found")
        return fruit

    @router.post("/fruits")
    def add_fruit(body: FruitCreate):
        return store.create(body)

    @router.put("/fruits/{fruit_id:int}")
    def update_fruit(fruit_id: int, body: FruitUpdate):
        updated = store.update(fruit_id, body)
        if updated is None:
            raise HTTPException(status_code=404, detail="Fruit not found")
        return updated

    @router.delete("/fruits/{fruit_id:int}", status_code=204)
    def delete_fruit(fruit_id: int):
        if not store.delete(fruit_id):
            raise HTTPException(status_code=404, detail="Fruit not found")
        return Response(status_code=204)

    return router


router = build_router(default_store)
