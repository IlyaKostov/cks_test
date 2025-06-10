from sqlalchemy import select
from common.models import Price
from common.database.db import async_session_maker


class PriceRepository:
    @staticmethod
    async def get_last_price(product_id: int) -> float | None:
        """Retrieves the last price for the specified product."""
        async with async_session_maker() as session:
            stmt = (
                select(Price.price)
                .filter_by(product_id=product_id)
                .order_by(Price.created_at.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @staticmethod
    async def save_price(product_id: int, price: float) -> None:
        """Saves a new price for the specified product."""
        async with async_session_maker() as session:
            async with session.begin():
                price_record = Price(product_id=product_id, price=price)
                session.add(price_record)
                await session.commit()
