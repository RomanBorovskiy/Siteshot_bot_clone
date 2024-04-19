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
        logger.debug("Launch browser")
        self.connection = await async_playwright().start()
        self.browser = await self.connection.chromium.launch()
        #self.browser = await self.connection.firefox.launch()
        logger.debug("Browser launched version: {}".format(self.browser.version))

    async def close_browser(self):
        try:
            await self.browser.close()
            await asyncio.sleep(0.5)
            # TODO: починить Connection closed while reading from the driver
            await self.connection.stop()
        except Exception as e:
            logger.error(e)

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
            url_after = page.url

            await page.screenshot(path=path)
            logger.info("Screenshot saved to {0}".format(path))

        except Exception as e:
            logger.error(e)
            result = {"path": "", "url_before": url, "title": "", "time": "", "error": e}
            return result

        finally:
            await page.close()

        time_count = time.perf_counter() - start_time

        result = {"path": path, "url_before": url, "url_after": url, "title": title, "time": time_count, "error": None}
        return result
