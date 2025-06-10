import logging

import httpx

from common.config import settings

logger = logging.getLogger(__name__)


async def add_product_api(url: str) -> dict:
    """Adds a product to the API using the provided URL."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f'{settings.API_BASE_URL}/api/products/add_product',
                json={'url': url},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f'HTTP error adding product: {e}')
            return {'error': f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f'Error adding product: {e}')
            return {'error': str(e)}


async def delete_product_api(product_id: int) -> bool:
    """Deletes a product from the API using the specified product ID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f'{settings.API_BASE_URL}/api/products/delete_product/{product_id}',
                timeout=10.0
            )
            return response.status_code in (200, 204)
        except httpx.HTTPStatusError as e:
            logger.error(f'HTTP error deleting product: {e.response.status_code}')
            return False
        except httpx.RequestError as e:
            logger.error(f'Request error deleting product: {e}')
            return False
        except Exception as e:
            logger.error(f'Unexpected error deleting product: {e}')
            return False


async def get_products_list_api() -> list:
    """Retrieves a list of products from the API."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{settings.API_BASE_URL}/api/products/products_list',
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f'Error getting products list: {e}')
            return []


async def get_price_history_api(product_id: int) -> list:
    """ Retrieves the price history of a specific product using its ID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{settings.API_BASE_URL}/api/prices/{product_id}',
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f'Error getting price history: {e}')
            return []
