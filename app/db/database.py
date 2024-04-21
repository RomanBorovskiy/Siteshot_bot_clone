from datetime import datetime

from tortoise import Tortoise

from config import settings

from .models import Request, User

TORTOISE_ORM = {
    "connections": {"default": str(settings.DB_URI)},
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


async def get_user_language(user_id: int) -> str | None:
    query = await User.filter(user_id=user_id).first().values_list("language")
    if query:
        return query[0]
    else:
        return None


async def set_user_language(user_id: int, username: str, full_name: str, language: str):
    await User.update_or_create(
        user_id=user_id, defaults={"username": username, "full_name": full_name, "language": language}
    )


async def write_success(user_id: int, url: str, time: int):
    await Request.create(user_id=user_id, url=url, duration=int(time * 1000))


async def write_error(user_id: int, url: str):
    await Request.create(user_id=user_id, url=url, duration=None)


async def get_statistic_per_day(date: datetime):
    today_request_count = await Request.filter(created_at__gte=date).count()
    return today_request_count


async def get_statistic_per_month(date: datetime):
    month_first_day = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_request_count = await Request.filter(created_at__gte=month_first_day).count()
    return month_request_count
