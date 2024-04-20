import asyncio
import logging.config
import os

import backoff
from asyncpg import connect, PostgresError
from aioredis import Redis, RedisError

#PG_URI = 'postgres://app:123qwe@localhost:5432/siteshot_bot'
#REDIS_URI = 'redis://default:123qwe@localhost:6379/0'

PG_URI = os.getenv("DB_BOT_DSN")
REDIS_URI = os.getenv("REDIS_BOT_DSN")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": logging.DEBUG,
        "formatter": "default",
        "handlers": ["default"],
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def on_error(details: dict):
    logger.error("Wait error")
    exit(1)


@backoff.on_predicate(backoff.expo, logger=logger, max_time=300, on_giveup=on_error, max_value=5)
async def check_postgres(pg_uri: str) -> bool:
    conn = None
    try:
        conn = await connect(pg_uri)
        await conn.execute("SELECT 1")
        await conn.close()
        logger.info("Postgres OK")
        return True
    except PostgresError:
        return False
    finally:
        if conn:
            await conn.close()


@backoff.on_predicate(backoff.expo, logger=logger, max_time=300, on_giveup=on_error, max_value=5)
async def check_redis(redis_client: Redis) -> bool:
    try:
        ping = await redis_client.ping()
        if ping:
            logger.info("Redis OK")

        return ping

    except RedisError:
        return False


async def wait():
    redis_client = Redis.from_url(REDIS_URI)
    await check_redis(redis_client)
    await check_postgres(PG_URI)

if __name__ == "__main__":
    asyncio.run(wait(), debug=True)
