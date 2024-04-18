from pathlib import Path

from aiogram import types

from config import EMPTY_PIC, PICS_DIR, settings
from imager import UrlImager
from db import database
from db.models import User

from locales import Language

# глобальные переменные
bot_name = 'BOT_NAME'
imager = UrlImager(PICS_DIR, timeout=settings.PAGE_TIMEOUT)
empty_pic = types.FSInputFile(EMPTY_PIC)


async def init():
    await database.setup()
    await imager.launch_browser()


async def close():
    await imager.close_browser()
    await database.close()


async def capture_screenshot(url: str, file_name: Path):
    return await imager.capture_screenshot(url=url, file_name=file_name)


async def get_user_language(user: types.User) -> Language:
    """ Возвращает язык пользователя
        Если пользователь не зарегистрирован - возвращает ru
    """
    query = await User.filter(user_id=user.id).first().values_list("language")
    if query:
        return Language(query[0])
    else:
        return Language.RU


async def set_user_language(user: types.User, language: Language):
    """
        Устанавливает язык пользователя
        Если пользователь не зарегистрирован - создает его
    """
    await User.update_or_create(user_id=user.id, defaults={"username": user.username,
                                                                   "full_name": user.full_name,
                                                                   "language": str(language)})
