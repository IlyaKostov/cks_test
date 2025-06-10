import asyncio
import logging

from aiogram import Dispatcher, Bot

from common.config import settings
from bot_app.handlers import router

logging.basicConfig(level=logging.INFO,
                    filename="py_log.log",
                    format="%(asctime)s %(levelname)s %(message)s",
                    encoding="utf-8")
logger = logging.getLogger(__name__)
bot = Bot(token=settings.TG_BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Polling stopped by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Stopping polling...")
