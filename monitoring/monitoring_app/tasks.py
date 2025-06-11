import logging
import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from common.config import settings
from .monitor import PriceMonitor

logger = logging.getLogger(__name__)

rabbitmq_broker = RabbitmqBroker(url=settings.RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)


price_monitor = PriceMonitor()
price_scheduler = price_monitor.scheduler


@dramatiq.actor
def schedule_monitoring(product_id: int, url: str):
    logger.info(f'Scheduling monitoring for product {product_id}')
    price_scheduler.add_product_monitoring(product_id, url)


@dramatiq.actor
def delete_product(product_id: int):
    logger.info(f'Remove product {product_id} from monitoring')
    price_scheduler.remove_product_monitoring(product_id)
