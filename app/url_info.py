import asyncio
import logging
import socket
from urllib.parse import urlparse

import aiogeoip
import asyncwhois

from app.locales import AppMessage

logger = logging.getLogger(__name__)


async def whois(url):
    netloc = urlparse(url).netloc
    result = {}

    try:
        _, parsed_dict = await asyncwhois.aio_whois(netloc)

    except asyncwhois.errors.WhoIsError as e:
        logger.error(e)
        result[AppMessage.ERROR] = str(e)
        return result

    # список параметров для вывода
    show_keys = [
        ("domain_name", AppMessage.DOMEN_NAME),
        ("registrar", AppMessage.REGISTRAR),
        ("creation_date", AppMessage.CREATION_DATE),
        ("expiration_date", AppMessage.EXPIRATION_DATE),
        ("updated_date", AppMessage.UPDATED_DATE),
        ("name_servers", AppMessage.NAME_SERVERS),
        ("registrant_organization", AppMessage.ORGANIZATION),
    ]

    # формируем словарь из выбранных параметров
    for key, name in show_keys:
        if key in parsed_dict:
            value = parsed_dict[key]
            # ограничиваем длину списка для вывода
            if isinstance(value, list):
                if len(value) > 2:
                    value = ", ".join(value[:2]) + "..."
                else:
                    value = ", ".join(value)

            result[name] = value

    return result


async def geo_ip(url):
    def get_ip(domen_name):
        try:
            domen_ip = socket.gethostbyname(domen_name)
        except socket.gaierror as e:
            logger.error(e)
            return None
        return domen_ip

    result = {}
    netloc = urlparse(url).netloc
    # получаем ip по домену в потоке, так как это не асинхронная функция
    ip = await asyncio.to_thread(get_ip, netloc)

    if not ip:
        error = "Domain {} not found".format(netloc)
        logger.error(error)
        result[AppMessage.ERROR] = error
        return result

    geo = await aiogeoip.geoip(ip)
    if not geo:
        error = "IP {} not found in GeoIP database".format(ip)
        logger.error(error)
        result[AppMessage.ERROR] = error
        return result

    result[AppMessage.IP] = ip
    result[AppMessage.COUNTRY] = geo.country
    result[AppMessage.CITY] = geo.city
    result[AppMessage.PROVIDER] = geo.isp
    result[AppMessage.ORGANIZATION] = geo.org

    return result
