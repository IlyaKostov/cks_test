from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from common.config import settings


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = tuple()

    metadata = MetaData(
        naming_convention=settings.naming_convention,
    )

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
