from abc import ABC, abstractmethod

from common.database.db import async_session_maker
from app.repositories.product import ProductRepository
from app.repositories.price import PriceRepository


class AbstractUnitOfWork(ABC):
    product: ProductRepository
    price: PriceRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions"""

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.product = ProductRepository(self.session)
        self.price = PriceRepository(self.session)

    async def __aexit__(self, exc_type, *args):
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
