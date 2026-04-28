"""FastAPI application factory for FruitAPI."""
import time

from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from app.handlers.handlers import build_router
from app.store.store import FruitStore


def _init_with_retry(store: FruitStore, attempts: int = 30, delay: float = 2.0) -> None:
    """Wait for DB to be reachable before initializing schema."""
    last_err: Exception | None = None
    for _ in range(attempts):
        try:
            store.init_schema()
            store.seed_defaults_if_empty()
            return
        except OperationalError as e:
            last_err = e
            time.sleep(delay)
    raise RuntimeError(f"Database not reachable after {attempts} attempts") from last_err


def create_app(store: FruitStore | None = None) -> FastAPI:
    """Create the FastAPI app. Accepts an optional store for testing."""
    if store is None:
        store = FruitStore()
        _init_with_retry(store)

    fastapi_app = FastAPI(title="FruitAPI", version="1.0.0")
    fastapi_app.include_router(build_router(store))
    return fastapi_app


__all__ = ["create_app"]
