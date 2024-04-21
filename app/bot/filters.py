import validators
from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils import prepare_url


class UrlFilter(BaseFilter):
    """Фильтр определяет является ли сообщение URL-адресом"""

    async def __call__(self, message: Message) -> bool:
        url = prepare_url(message.text)
        result = validators.url(url)
        return bool(result)
