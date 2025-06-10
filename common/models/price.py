from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from common.models.base import BaseModel


class Price(BaseModel):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='CASCADE'),
    )
    price: Mapped[Optional[float]]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    product: Mapped['Product'] = relationship('Product', back_populates='prices')
