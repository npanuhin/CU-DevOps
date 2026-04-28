from sqlalchemy import func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import Base, make_engine
from app.models.fruit import FruitCreate, FruitORM, FruitUpdate, fruit_response


class FruitStore:
    """SQLAlchemy-backed store for fruits."""

    def __init__(self, engine: Engine | None = None) -> None:
        self._engine = engine if engine is not None else make_engine()
        self._Session = sessionmaker(bind=self._engine, expire_on_commit=False)

    @property
    def engine(self) -> Engine:
        return self._engine

    def init_schema(self) -> None:
        Base.metadata.create_all(self._engine)

    def reset(self) -> None:
        """Drop and recreate the schema. Used by tests."""
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

    def seed_defaults(self) -> None:
        """Replace contents with the default catalog."""
        with self._Session() as s:
            s.query(FruitORM).delete()
            s.add_all(self._default_rows())
            s.commit()

    def seed_defaults_if_empty(self) -> None:
        """Insert defaults only if the table is empty (safe at startup)."""
        with self._Session() as s:
            count = s.scalar(select(func.count()).select_from(FruitORM))
            if count == 0:
                s.add_all(self._default_rows())
                s.commit()

    @staticmethod
    def _default_rows() -> list[FruitORM]:
        return [
            FruitORM(name="Apple", price=1.20, in_season=True),
            FruitORM(name="Banana", price=0.80, in_season=True),
            FruitORM(name="Orange", price=1.00, in_season=False),
        ]

    def list(self, in_season: bool | None = None) -> list[dict]:
        with self._Session() as s:
            stmt = select(FruitORM).order_by(FruitORM.id.asc())
            if in_season is not None:
                stmt = stmt.where(FruitORM.in_season == in_season)
            return [self._to_dict(f) for f in s.scalars(stmt).all()]

    def get(self, fruit_id: int) -> dict | None:
        with self._Session() as s:
            f = s.get(FruitORM, fruit_id)
            return None if f is None else self._to_dict(f)

    def create(self, body: FruitCreate) -> dict:
        with self._Session() as s:
            f = FruitORM(name=body.name, price=body.price, in_season=body.in_season)
            s.add(f)
            s.commit()
            s.refresh(f)
            return self._to_dict(f)

    def update(self, fruit_id: int, body: FruitUpdate) -> dict | None:
        with self._Session() as s:
            f = s.get(FruitORM, fruit_id)
            if f is None:
                return None
            if body.name is not None:
                f.name = body.name
            if body.price is not None:
                f.price = body.price
            if body.in_season is not None:
                f.in_season = body.in_season
            s.commit()
            s.refresh(f)
            return self._to_dict(f)

    def delete(self, fruit_id: int) -> bool:
        with self._Session() as s:
            f = s.get(FruitORM, fruit_id)
            if f is None:
                return False
            s.delete(f)
            s.commit()
            return True

    def cheapest(self) -> dict | None:
        with self._Session() as s:
            stmt = select(FruitORM).order_by(FruitORM.price.asc(), FruitORM.id.asc()).limit(1)
            f = s.scalars(stmt).first()
            return None if f is None else self._to_dict(f)

    def __len__(self) -> int:
        with self._Session() as s:
            return int(s.scalar(select(func.count()).select_from(FruitORM)) or 0)

    @staticmethod
    def _to_dict(f: FruitORM) -> dict:
        return fruit_response(
            f.id, {"name": f.name, "price": f.price, "in_season": f.in_season}
        )
