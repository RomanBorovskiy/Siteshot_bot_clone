import logging

import aioredis

logger = logging.getLogger(__name__)


class RedisCacheService:
    """Класс для работы с кэшем Redis"""

    # ключ для хранения языка пользователя
    key_lang = "lang:{}"

    def __init__(self, redis_uri: str):
        self.redis_uri = redis_uri
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(str(self.redis_uri), decode_responses=True)

    async def close(self):
        await self.redis.close()  # noqa

    async def set_lang(self, user_id: int, lang: str):
        try:
            await self.redis.set(self.key_lang.format(user_id), lang)  # noqa
        except aioredis.RedisError as e:
            logger.error(e)

    async def get_lang(self, user_id: int) -> str | None:
        try:
            return await self.redis.get(self.key_lang.format(user_id))  # noqa
        except aioredis.RedisError as e:
            logger.error(e)
            return None
