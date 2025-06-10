import dramatiq

from dramatiq.brokers.rabbitmq import RabbitmqBroker

from common.config import settings

rabbitmq_broker = RabbitmqBroker(url=settings.RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)


@dramatiq.actor
def schedule_monitoring(product_id: int, url: str):
    print(f'Send to monitor_service: {product_id}, {url}')


@dramatiq.actor
def delete_product(product_id: int):
    print(f'Deleting product {product_id}')
