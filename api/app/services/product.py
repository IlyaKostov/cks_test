from fastapi import HTTPException
from sqlalchemy import Sequence

from common.models import Product
from app.services.base import BaseService
from app.utils.unit_of_work import AbstractUnitOfWork
from app.utils.tasks import schedule_monitoring, delete_product
from common.parser.parser_service import ParserService


class ProductService(BaseService):
    """Service class for managing product-related operations."""
    base_repository = 'product'

    async def add_new_product(self, uow: AbstractUnitOfWork, url: str) -> Product:
        """Adds a new product"""
        parser = ParserService()
        try:
            parser_data = await parser.parse_product(url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")

        product_id = int(parser_data.get('id'))

        async with uow:
            if await self.product_exists(uow, product_id):
                raise HTTPException(status_code=400, detail=f"Product with id {product_id} already exists")

            data = {
                'id': product_id,
                'url': url,
                'name': parser_data.get('name'),
                'description': parser_data.get('description'),
                'rating': round(parser_data.get('rating'), 2),
            }
            new_product = await uow.product.add_one_and_get_obj(**data)

            schedule_monitoring.send(new_product.id, new_product.url)
        return new_product

    async def get_all_products(self, uow: AbstractUnitOfWork) -> Sequence[Product]:
        """Retrieves all product"""
        async with uow:
            products = await uow.product.get_products_with_price()
            for product in products:
                if product.prices:
                    last_price = max(product.prices, key=lambda p: p.created_at)
                    product.price = last_price.price
                else:
                    product.price = None
            return products

    async def delete_product(self, uow: AbstractUnitOfWork, product_id: int) -> None:
        """Deletes a product from the system by its ID."""
        async with uow:
            await uow.product.delete_by_query(product_id=product_id)
            delete_product.send(product_id)

    @staticmethod
    async def product_exists(uow: AbstractUnitOfWork, product_id: int) -> bool:
        """Checks if a product exists in the system by its ID."""
        existing_product = await uow.product.get_by_query_one_or_none(id=product_id)
        return existing_product
