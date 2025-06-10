from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    rating: Mapped[Optional[float]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    prices: Mapped[list['Price']] = relationship(back_populates='product', cascade='all, delete-orphan')
