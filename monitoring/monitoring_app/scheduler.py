import logging
import asyncio
from typing import Dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.job import Job

from common.parser.parser_service import ParserService
from monitoring_app.price_repository import PriceRepository

logger = logging.getLogger(__name__)


class PriceScheduler:
    """A class for managing product price monitoring."""
    def __init__(self):
        """
        Initializes PriceScheduler with an asynchronous scheduler,
        price repository, and parsing service.
        """
        self.scheduler = AsyncIOScheduler()
        self.price_repo = PriceRepository()
        self.parser_service = ParserService()
        self.jobs: Dict[int, Job] = {}

    def start(self) -> None:
        """Starts the APScheduler to begin monitoring tasks."""
        self.scheduler.start()
        logger.info('APScheduler started')

    def shutdown(self) -> None:
        """Stops the APScheduler."""
        self.scheduler.shutdown()
        logger.info('APScheduler stopped')

    def add_product_monitoring(self, product_id: int, url: str) -> None:
        """Adds a product to the monitoring list."""
        self.remove_product_monitoring(product_id)
        job = self.scheduler.add_job(
            self.check_product_price,
            trigger=CronTrigger(minute=0),
            args=(product_id, url),
            id=f'price_check_{product_id}',
            name=f'Price monitoring for product {product_id}',
            replace_existing=True,
        )
        self.jobs[product_id] = job
        logger.info(f'Added monitoring job for product {product_id}')
        asyncio.create_task(self.check_product_price(product_id, url))

    def remove_product_monitoring(self, product_id: int) -> None:
        """Removes a product from the monitoring list."""
        job_id = f'price_check_{product_id}'
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
            logger.info(f'Removed monitoring job for product {product_id}')
        self.jobs.pop(product_id, None)

    async def check_product_price(self, product_id: int, url: str) -> None:
        """Checks the current price of the specified product."""
        logger.info(f'Checking price for product {product_id}')
        try:
            current_price = await self.parser_service.parse_price(product_id, url)
            price = current_price.get('price')
            logger.debug(f'Current price: {price}')
            last_price = await self.price_repo.get_last_price(product_id)
            if last_price is None or price != last_price:
                await self.price_repo.save_price(product_id, price)
                logger.info(f'Price changed for product {product_id}: {price}')
            else:
                logger.info(f'Price unchanged for product {product_id}')
        except Exception as e:
            logger.error(f'Error: {str(e)}')
            await asyncio.sleep(600)
            await self.check_product_price(product_id, url)
