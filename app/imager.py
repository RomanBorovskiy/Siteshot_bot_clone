import asyncio
import logging
import time
from pathlib import Path

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


class UrlImager:
    """Класс для создания скриншотов веб-страниц
    для начала работы необходимо вызвать метод launch_browser()
    для закрытия - close_browser()

    для создания скриншота - capture_screenshot(url, file_name)
    url - адрес веб-страницы
    file_name - имя файла для сохранения

    """

    def __init__(self, pics_dir: Path, timeout=10 * 1000):
        self.connection = None
        self.browser = None
        self.timeout = timeout
        self.pics_dir = pics_dir

    async def launch_browser(self):
        self.connection = await async_playwright().start()
        self.browser = await self.connection.chromium.launch()

    async def close_browser(self):
        await self.browser.close()
        await asyncio.sleep(0.1)

        # TODO: починить Connection closed while reading from the driver
        await self.connection.stop()
        await asyncio.sleep(0.1)

    async def capture_screenshot(
        self, url: str, file_name: Path, viewport_width: int = 1024, viewport_height: int = 768
    ) -> dict:

        start_time = time.perf_counter()
        path = self.pics_dir / file_name

        page = await self.browser.new_page()

        try:
            await page.set_viewport_size({"width": viewport_width, "height": viewport_height})

            await page.goto(url=url, timeout=self.timeout)

            title = await page.title()
            url = page.url

            await page.screenshot(path=path)
            logger.info("Screenshot saved to {0}".format(path))

        except Exception as e:
            logger.error(e)
            result = {"path": "", "url": url, "title": "", "time": "", "error": e}
            return result

        finally:
            await page.close()

        end_time = time.perf_counter() - start_time

        result = {"path": path, "url": url, "title": title, "time": end_time, "error": None}
        return result
