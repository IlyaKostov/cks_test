import os
import re
import logging

from typing import Optional
import httpx

from common.parser.base import BaseParser

logger = logging.getLogger(__name__)


class MVideoParser(BaseParser):
    """Parser for extracting product information from MVideo website."""

    async def parse_product(self, url: str, client: httpx.AsyncClient) -> dict:
        """Parse product details from the specified MVideo URL."""

        product_id = self.extract_product_id(url)
        if not product_id:
            logger.error("Invalid MVideo URL provided.")
            raise ValueError("Invalid MVideo URL")

        api_url = f"https://www.mvideo.ru/bff/product-details?productId={product_id}"

        try:
            data = await self.fetch_data(api_url, client)
            return self.parse_product_response(product_id, data)
        except Exception as e:
            logger.exception("Failed to parse product data for URL: %s", url)
            raise e

    async def parse_price(self, product_id: int, client: httpx.AsyncClient) -> dict:
        """Parse price information for a given product ID from MVideo."""

        api_url = f'https://www.mvideo.ru/bff/products/prices?productIds={product_id}'

        try:
            data = await self.fetch_data(api_url, client)
            return self.parse_price_response(data)
        except Exception as e:
            logger.exception("Failed to parse price data for product ID: %d", product_id)
            raise e

    async def fetch_data(self, api_url: str, client: httpx.AsyncClient) -> dict:
        """Fetch data from the specified API URL."""

        try:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as http_error:
            logger.error("HTTP error occurred: %s", http_error)
            raise
        except Exception as e:
            logger.exception("An error occurred while fetching data from URL: %s", api_url)
            raise

    @staticmethod
    def extract_product_id(url: str) -> Optional[str]:
        """Extract the product ID from the given URL."""

        match_result = re.search(r'-(\d+)$', url)
        return match_result .group(1) if match_result else None

    @staticmethod
    def get_cookies() -> dict:
        """Get cookies required for the HTTP requests."""

        return {
            'MVID_CITY_ID': os.getenv('MVID_CITY_ID'),
            'MVID_REGION_ID': os.getenv('MVID_REGION_ID'),
            'MVID_TIMEZONE_OFFSET': os.getenv('MVID_TIMEZONE_OFFSET'),
            'MVID_REGION_SHOP': os.getenv('MVID_REGION_SHOP'),
        }

    @staticmethod
    def parse_product_response(product_id: str, data: dict) -> dict:
        """Parse product information from the API response."""
        try:
            product = data.get('body', {})
            response_product_id = product.get('productId')
            if response_product_id != product_id:
                logger.error(
                    "Product ID mismatch: expected %s, got %s",
                    product_id,
                    response_product_id
                )
                raise ValueError(f"Product ID does not match: expected {product_id}, got {response_product_id}")

            rating = product.get('rating', {})

            return {
                'id': product_id,
                'name': product.get('name', 'Unknown'),
                'description': product.get('description', ''),
                'rating': rating.get('star')
            }
        except Exception as e:
            logger.exception("An unexpected error occurred while parsing product data: %s", e)
            raise e

    @staticmethod
    def parse_price_response(data: dict) -> dict:
        """Parse price information from the API response."""

        product = data.get('body', {})
        price_data = product.get('materialPrices', [])
        final_price = None
        if price_data:
            price = price_data[0].get('price')
            final_price = price.get('salePrice') or price.get('basePrice')

        return {
            'price': final_price
        }
