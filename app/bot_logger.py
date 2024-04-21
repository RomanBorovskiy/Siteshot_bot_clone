import logging

from loguru import logger

from config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = logging.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level: str | int = "DEBUG"):
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.getLevelName(level))


log_level = logging.DEBUG if settings.DEBUG else logging.INFO
setup_logger(log_level)
