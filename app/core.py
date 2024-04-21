import datetime
from pathlib import Path

from aiogram import Bot, types

from services.cache_service import RedisCacheService
from config import PICS_DIR, settings
from db import database
from services.imager import UrlImager
from locales import Language

# глобальные переменные
bot_name = "BOT_NAME"
bot: Bot
imager = UrlImager(PICS_DIR, timeout=settings.PAGE_TIMEOUT)
cache_service = RedisCacheService(settings.REDIS_URI)


async def init():
    """Инициализация ресурсов"""
    await database.setup()
    await cache_service.connect()
    await imager.launch_browser()


async def close():
    """Освобождение ресурсов"""
    await imager.close_browser()
    await database.close()
    await cache_service.close()


async def capture_screenshot(url: str, file_name: Path):
    """Функция для получения скриншота с сайта"""
    return await imager.capture_screenshot(url=url, file_name=file_name)


async def get_user_language(user: types.User) -> Language:
    """Возвращает язык пользователя
    Если пользователь не зарегистрирован - возвращает ru
    """
    cached_language = await cache_service.get_lang(user.id)
    if cached_language:
        return Language(cached_language)

    lang = await database.get_user_language(user.id)

    if lang:
        language = Language(lang)
    else:
        language = Language.RU

    await cache_service.set_lang(user.id, lang)
    return language


async def set_user_language(user: types.User, language: Language):
    """Устанавливает язык пользователя
    Если пользователь не зарегистрирован - создает его
    """
    await database.set_user_language(user.id, user.username, user.full_name, str(language))
    await cache_service.set_lang(user.id, str(language))


async def write_db_success(user: types.User, url: str, time: int):
    """Логирует в БД успешный запрос"""
    await database.write_success(user.id, url, time)


async def write_db_error(user: types.User, url: str):
    """Логирует в БД неудачный запрос"""
    await database.write_error(user.id, url)


async def get_statistics():
    """Немного статистики :)
    Возвращаем кол-во запросов за день и месяц (календарный)
    """
    now = datetime.datetime.now()
    today_request_count = database.get_statistic_per_day(now)
    month_request_count = database.get_statistic_per_month(now)
    return today_request_count, month_request_count
