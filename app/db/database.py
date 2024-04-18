from tortoise import Tortoise

from app.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": str(settings.DB_URI)
    },
    "apps": {
        "models": {
            "models": ["db.models"],
            "default_connection": "default",
        },
    },
}


async def setup():
    await Tortoise.init(TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()
