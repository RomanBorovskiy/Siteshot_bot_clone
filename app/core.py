from pathlib import Path

from aiogram import types

from app.config import EMPTY_PIC, PICS_DIR, settings
from imager import UrlImager

imager: UrlImager
bot_name: str
empty_pic = types.FSInputFile(EMPTY_PIC)


async def init():
    global imager
    imager = UrlImager(PICS_DIR, timeout=settings.PAGE_TIMEOUT)
    await imager.launch_browser()


async def close():
    global imager
    await imager.close_browser()


async def capture_screenshot(url: str, file_name: Path):
    global imager
    return await imager.capture_screenshot(url=url, file_name=file_name)
