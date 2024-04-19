import asyncio
from datetime import datetime
from urllib.parse import urlparse
import logging

import aiogram.client.session.aiohttp
import aiohttp

from config import settings

logger = logging.getLogger(__name__)


def get_image_name(user_id: int, url: str):
    """Функция для генерации имени файла
    формат: дата_время_пользователь_домен.png
    """
    now_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    netloc = urlparse(url).netloc
    filename = f"{now_datetime}_{user_id}_{netloc}.png"
    return filename


def prepare_url(message: str):
    """Функция для предобработки строки с url
    обрезает пробелы и добавляет http:// в начало, если нет схемы"""

    if not message:
        return None

    message.strip()
    if not message.startswith("http://") and not message.startswith("https://"):
        url = "https://" + message
    else:
        url = message
    return url


async def get_image_link(stream: bytes, bot_session: aiogram.client.session.aiohttp.AiohttpSession):
    """Записывает на telegraph изображение и возвращает ссылку на него"""
    session = await bot_session.create_session()

    try:
        async with session.post("https://telegra.ph/upload",
                                data={"file": stream}, timeout=settings.TELEGRAPH_TIMEOUT) as response:
            data = await response.json()

    except asyncio.TimeoutError:
        logger.error("Timeout error while uploading image to telegraph")
        return None

    except aiohttp.ClientError as e:
        logger.error(f"Client error:{e}")
        return None

    return "https://telegra.ph" + data[0]["src"]
