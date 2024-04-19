from datetime import datetime
from urllib.parse import urlparse


def get_image_name(user_id: int, url: str):
    """Функция для генерации имени файла
    формат: дата_время_пользователь_домен.png
    """
    now_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    netloc = urlparse(url).netloc
    filename = f"{now_datetime}_{user_id}_{netloc}.png"
    return filename


def prepare_url(message: str):
    """Функция для предобработки строки с url
    обрезает пробелы и добавляет http:// в начало, если нет схемы"""

    if not message:
        return None

    message.strip()
    if not message.startswith("http://") and not message.startswith("https://"):
        url = "https://" + message
    else:
        url = message
    return url

