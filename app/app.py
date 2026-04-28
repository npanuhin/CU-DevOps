from fastapi import FastAPI

from app.handlers.handlers import router
from app.store.store import store


def create_app() -> FastAPI:
    """FastAPI application factory."""
    fastapi_app = FastAPI(title="FruitAPI", version="1.0.0")
    fastapi_app.include_router(router)
    return fastapi_app


__all__ = ["create_app", "store"]
