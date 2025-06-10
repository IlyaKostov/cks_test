import asyncio
import logging
import signal
from monitoring_app.monitor import PriceMonitor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

monitor = PriceMonitor()


async def shutdown():
    logging.info("Shutting down...")
    await monitor.shutdown()


async def main():
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    def signal_handler():
        logging.info('Received termination signal, initiating shutdown...')
        stop_event.set()

    if loop.is_running():
        for signame in ('SIGINT', 'SIGTERM'):
            try:
                loop.add_signal_handler(getattr(signal, signame), signal_handler)
            except NotImplementedError:
                logging.warning(f'Signal handling for {signame} is not supported on this platform.')

    try:
        await monitor.start()
        await stop_event.wait()
    finally:
        await shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Program interrupted by user.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        raise e
    finally:
        logging.info('Program termination.')
