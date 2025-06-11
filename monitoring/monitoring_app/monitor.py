import logging
from monitoring_app.scheduler import PriceScheduler

logger = logging.getLogger(__name__)


class PriceMonitor:
    """
    A class for monitoring price changes of products using a scheduled task.

    This class manages a PriceScheduler to periodically check for price changes
    and log the results. It handles the starting and shutdown process of the monitoring.
    """
    def __init__(self):
        """
        Initializes the PriceMonitor with a PriceScheduler instance.
        """
        self.scheduler = PriceScheduler()

    async def start(self):
        """Starts the price monitoring process."""
        self.scheduler.start()
        logger.info("Price Monitor started")

    async def shutdown(self):
        """Shuts down the price monitoring service."""
        logger.info("Shutting down Price Monitor...")
        self.scheduler.shutdown()
