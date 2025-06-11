import logging
import os
from urllib.parse import urlparse

import httpx
from fake_useragent import UserAgent

from common.parser.mvideo import MVideoParser

logger = logging.getLogger(__name__)


class ParserService:
    """Service for parsing product information from various e-commerce websites."""

    _parsers = {
        'www.mvideo.ru': MVideoParser,
        'mvideo.ru': MVideoParser
    }

    async def parse_product(self, url: str) -> dict:
        """Parse product information from the given URL."""

        parser_class = self.get_parser_class(url)

        logger.info("Using parser: %s for URL: %s", parser_class.__name__, url)
        parser = parser_class()

        headers = {
            'User-Agent': UserAgent().random,
        }

        cookies = self.get_cookies()

        async with httpx.AsyncClient(follow_redirects=True, headers=headers, cookies=cookies) as client:
            try:
                product_data = await parser.parse_product(url, client)
                logger.info("Successfully parsed product data for URL: %s", url)
                return product_data
            except Exception as e:
                logger.exception("Failed to parse product data for URL: %s", url)
                raise e

    async def parse_price(self, product_id: int, url: str) -> dict:
        """Parse price information from the given product URL."""
        parser_class = self.get_parser_class(url)

        logger.info('Using parser: %s for URL: %s', parser_class.__name__, url)
        parser = parser_class()

        headers = {
            'User-Agent': UserAgent().random,
        }

        cookies = self.get_cookies()

        async with httpx.AsyncClient(follow_redirects=True, headers=headers, cookies=cookies) as client:
            try:
                product_data = await parser.parse_price(product_id, client)
                logger.info('Successfully parsed product data for URL: %s', url)
                return product_data
            except Exception as e:
                logger.exception('Failed to parse product data for URL: %s', url)
                raise e

    def get_parser_class(self, url: str):
        """Resolve parser class from URL domain."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f'Invalid URL passed: {url}')

        domain = parsed_url.netloc
        parser_class = self._parsers.get(domain)

        if parser_class is None:
            logger.error('No parser found for domain: %s', domain)
            raise ValueError(f'No parser available for domain: {domain}')

        return parser_class

    @staticmethod
    def get_cookies() -> dict:
        """Get cookies required for the HTTP requests."""

        return {
            'MVID_CITY_ID': os.getenv('MVID_CITY_ID'),
            'MVID_REGION_ID': os.getenv('MVID_REGION_ID'),
            'MVID_TIMEZONE_OFFSET': os.getenv('MVID_TIMEZONE_OFFSET'),
            'MVID_REGION_SHOP': os.getenv('MVID_REGION_SHOP'),
        }
