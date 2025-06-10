from fastapi import APIRouter

from app.routers.product import router as product_router
from app.routers.price import router as price_router

router = APIRouter(prefix="/api")

router.include_router(
    product_router,
    prefix="/products",
    tags=["Products"],
)

router.include_router(
    price_router,
    prefix="/prices",
    tags=["Prices"],
)


@router.get("/health", tags=['health'], include_in_schema=False)
async def health_check():
    return {"status": "ok"}
