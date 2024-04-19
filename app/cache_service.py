import logging

import aioredis

from config import settings

redis: aioredis.Redis
key_lang = "lang:{}"

logger = logging.getLogger(__name__)


async def setup():
    global redis
    redis = await aioredis.from_url(str(settings.REDIS_URI), decode_responses=True)


async def close():
    await redis.close() # noqa


async def set_lang(user_id: int, lang: str):
    try:
        await redis.set(key_lang.format(user_id), lang) # noqa
    except aioredis.RedisError as e:
        logger.error(e)


async def get_lang(user_id: int) -> str | None:
    try:
        return await redis.get(key_lang.format(user_id)) # noqa
    except aioredis.RedisError as e:
        logger.error(e)
        return None
