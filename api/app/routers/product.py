from typing import Sequence

from fastapi import APIRouter
from starlette import status

from common.models import Product
from app.routers.dependencies import ProductServ, UOWDep
from app.schemas.product import ProductSchema, ProductWithPriceSchema

router = APIRouter()


@router.post(
    "/add_product",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_product(
        uow: UOWDep,
        service: ProductServ,
        url: str
) -> Product:
    """Adds a new product"""
    product: Product = await service.add_new_product(uow, url)
    return product


@router.delete(
    "/delete_product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    uow: UOWDep,
    service: ProductServ,
    product_id: int,
):
    """Deletes a product identified by its ID"""
    await service.delete_by_query(uow=uow, product_id=product_id)


@router.get(
    "/products_list",
    response_model=Sequence[ProductWithPriceSchema],
)
async def get_products_list(
    uow: UOWDep,
    service: ProductServ,
) -> Sequence[ProductWithPriceSchema]:
    """Retrieves a list of all products"""
    results: Sequence[ProductWithPriceSchema] = await service.get_all_products(uow)
    return results
