from typing import Sequence

from common.models import Price
from app.services.base import BaseService
from app.utils.unit_of_work import AbstractUnitOfWork


class PriceService(BaseService):
    """Service class for handling price-related operations."""
    base_repository = 'price'

    async def get_prices_for_product(self, uow: AbstractUnitOfWork, product_id: int):
        """Retrieves all prices for a specific product identified by its ID."""
        async with uow:
            results: Sequence[Price] = await uow.price.get_by_query_all(product_id=product_id)
            return results
