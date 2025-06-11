from typing import Sequence

from fastapi import APIRouter

from app.routers.dependencies import UOWDep, PriceServ
from app.schemas.price import PriceSchema

router = APIRouter()


@router.get(
    "/{product_id}",
    response_model=Sequence[PriceSchema],
)
async def get_price_history(
    uow: UOWDep,
    service: PriceServ,
    product_id: int,
) -> Sequence[PriceSchema]:
    """Retrieves the price history for a specific product identified by its ID."""
    results: Sequence[PriceSchema] = await service.get_prices_for_product(uow, product_id)
    return results
