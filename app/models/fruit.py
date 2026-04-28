from pydantic import BaseModel


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
