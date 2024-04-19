from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from core import get_user_language


class LanguageMiddleware(BaseMiddleware):
    """Middleware для определения языка пользователя"""

    async def __call__(self, handler: callable, event: TelegramObject, data: dict):
        user = data["event_from_user"]
        lang = await get_user_language(user)
        data["user_language"] = lang
        result = await handler(event, data)
        return result
