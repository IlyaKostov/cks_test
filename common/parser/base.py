import abc
import httpx


class BaseParser(abc.ABC):
    @abc.abstractmethod
    async def parse_product(self, url: str, client: httpx.AsyncClient) -> dict:
        """Parse product data from URL"""
        pass
