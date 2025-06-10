from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.models import Product
from app.utils.base_repository import SQLAlchemyRepository


class ProductRepository(SQLAlchemyRepository):
    """repository for product class"""
    model = Product

    async def get_products_with_price(self) -> Sequence[Product]:
        """
        Request for data on the latest trading dates
        """

        query = (
            select(self.model)
            .options(selectinload(self.model.prices))
            .order_by(self.model.created_at.desc())
            )
        result = await self.session.execute(query)
        return result.scalars().all()
