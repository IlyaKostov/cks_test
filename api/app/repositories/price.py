from common.models import Price
from app.utils.base_repository import SQLAlchemyRepository


class PriceRepository(SQLAlchemyRepository):
    """repository for price class"""
    model = Price
