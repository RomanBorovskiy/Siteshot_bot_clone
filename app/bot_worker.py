import asyncio
import json
import logging
from signal import SIGINT, SIGTERM

import aio_pika
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import bot_logger  # noqa: F401
import botlogic
import core
from config import settings

logger = logging.getLogger(__name__)


async def process_message(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process(ignore_processed=True):
        body = message.body.decode()
        data = json.loads(body)
        logger.info(f"Received message: {data}")
        await botlogic.do_url_answer(
            data["chat_id"], data["message_id"], data["user_id"], data["url"], data["language"]
        )
        await message.ack()


def set_signals():
    """Настройка обработчиков сигналов
    Необходимо для нормального завершения воркера по сигналам
    """
    main_task = asyncio.current_task()
    loop = asyncio.get_event_loop()
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, main_task.cancel)


async def main() -> None:
    # выходим если не включен режим работы воркером
    if not settings.WORKER_USED:
        logger.error("Worker not used! set WORKER_USED=True in config")
        return

    set_signals()

    logger.info("Starting bot worker...")
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    core.bot = bot

    logger.info("Init connections...")
    await core.init()

    # Подписываемся на очередь
    logger.info("consuming queue...")
    await core.queue.consume(process_message, max_tasks=settings.MAX_TASKS)

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info("Shutdown bot worker...")
        await core.close()
        logger.info("Bot worker stopped")


if __name__ == "__main__":
    asyncio.run(main())
