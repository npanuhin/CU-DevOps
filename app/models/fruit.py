from pydantic import BaseModel
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class FruitCreate(BaseModel):
    name: str
    price: float = 0.0
    in_season: bool = True


class FruitUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    in_season: bool | None = None


class Fruit(BaseModel):
    id: int
    name: str
    price: float = 0.0
    in_season: bool = True


class FruitORM(Base):
    __tablename__ = "fruits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    in_season: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


def fruit_response(fruit_id: int, data: dict) -> dict:
    """Build the canonical fruit JSON: id + the data fields."""
    return {"id": fruit_id, **data}
