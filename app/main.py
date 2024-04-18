import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import core
from app.config import settings
from handlers import router

logger = logging.getLogger(__name__)


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="/start", description="About bot"),
    ]
    await bot.set_my_commands(commands)


async def on_startup(bot: Bot):
    logger.info("Starting...")
    await set_main_menu(bot)
    await core.init()


async def on_shutdown(bot: Bot):
    logger.info("Shutdown...")
    await core.close()


async def main():
    bot = Bot(token=settings.BOT_TOKEN.get_secret_value())

    # сохраняем имя бота - для ссылки
    info = await bot.get_me()
    bot_name = info.username
    core.bot_name = bot_name
    logger.info(f"starting Bot name: {bot_name}")

    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(router)

    if settings.DROP_UPDATES_ON_START:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("drop_pending_updates")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
