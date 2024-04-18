import logging
from datetime import datetime
from urllib.parse import urlparse

import asyncwhois

from locales import AppMessage

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
        url = "http://" + message
    else:
        url = message
    return url


async def whois(url):
    netloc = urlparse(url).netloc

    try:
        _, parsed_dict = await asyncwhois.aio_whois(netloc)

    except asyncwhois.errors.WhoIsError as e:
        logger.error(e)
        return "Error: " + str(e)

    # список параметров для вывода
    show_keys = [
        ("domain_name", AppMessage.DOMEN_NAME),
        ("registrar", AppMessage.REGISTRAR),
        ("creation_date", AppMessage.CREATION_DATE),
        ("expiration_date", AppMessage.EXPIRATION_DATE),
        ("updated_date", AppMessage.UPDATED_DATE),
        ("name_servers", AppMessage.NAME_SERVERS),
        ("registrant_organization", AppMessage.REGISTRANT_ORGANIZATION),
    ]

    result = {}
    # формируем словарь из выбранных параметров
    for key, name in show_keys:
        if key in parsed_dict:
            value = parsed_dict[key]
            if isinstance(value, list):
                value = ", ".join(value)
            result[name] = value

    return result
