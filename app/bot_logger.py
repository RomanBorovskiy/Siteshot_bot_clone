import logging
from config import settings

log_level = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


def get_logger(name):
    return logging.getLogger(name)