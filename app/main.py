import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import core
from config import settings
from handlers import router
from middlewares import LanguageMiddleware

logger = logging.getLogger(__name__)


async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command="/start", description="About bot"),
    ]
    await bot.set_my_commands(commands)


async def on_startup(bot: Bot):
    """Инициализация при запуске бота"""
    logger.info("Starting...")
    await set_main_menu(bot)
    await core.init()


async def on_shutdown(bot: Bot):
    """Завершение при выключении бота"""
    logger.info("Shutdown...")
    await core.close()


async def main():
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    core.bot = bot
    # сохраняем имя бота - для ссылки
    info = await bot.get_me()
    bot_name = info.username
    core.bot_name = bot_name
    logger.info(f"starting Bot name: {bot_name}")

    dp = Dispatcher(storage=MemoryStorage())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.outer_middleware(LanguageMiddleware())

    dp.include_router(router)

    if settings.DROP_UPDATES_ON_START:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("drop_pending_updates")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    asyncio.run(main())
