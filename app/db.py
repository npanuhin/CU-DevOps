"""Database engine factory and declarative base for FruitAPI."""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def make_database_url() -> str:
    """Build a SQLAlchemy URL from env vars. DATABASE_URL wins if set."""
    if url := os.getenv("DATABASE_URL"):
        return url
    user = os.getenv("DB_USER", "fruitapi")
    password = os.getenv("DB_PASSWORD", "fruitapi")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "fruitapi")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"


def make_engine(url: str | None = None) -> Engine:
    return create_engine(url or make_database_url(), pool_pre_ping=True, future=True)
