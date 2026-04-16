import asyncio
import logging
import sys

from app.bot import bot, dp
from app.database.models import async_main
from app.handlers.registration import router as reg_router
from app.handlers.admin import router as admin_router


async def main():
    await async_main()

    dp.include_router(admin_router)
    dp.include_router(reg_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
