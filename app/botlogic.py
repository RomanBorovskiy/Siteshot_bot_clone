from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.markdown import hide_link

import core
from config import settings
from services import url_info
import utils
from bot.keyboards import get_lang_keyboard, get_picture_keyboard, get_start_keyboard
from locales import AppMessage, Language, _


async def start_answer(msg: Message, lang: Language):
    """Возвращает ответ на /start"""
    text = _(AppMessage.START_MSG, lang)
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_start_keyboard(lang))


async def url_make_stub(msg: Message, lang: Language, inplace: bool = False) -> Message:
    """Создает в ответ сообщение-заглушку и возвращает это сообщение
    Если inplace = True - то редактирует существующее сообщение
    """
    text = _(AppMessage.STUB_MSG, lang)
    if inplace:
        new_msg = await msg.edit_text(text=text)
    else:
        new_msg = await msg.reply(text=text)

    return new_msg


async def url_error_answer(chat_id: int, message_id: int, user_id: int, result: dict, lang: Language):
    """Редактирует сообщение - сообщает об ошибке"""
    text = _(AppMessage.ERROR_MSG, lang)
    await core.bot.edit_message_text(text, chat_id, message_id, reply_markup=get_picture_keyboard(lang))
    await core.write_db_error(user_id, result["url_before"])


async def url_answer(chat_id: int, message_id: int, user_id: int, result: dict, lang: Language):
    """Редактирует сообщение - сообщает об успешном обработке"""
    text = _(AppMessage.RESULT_MSG, lang)
    new_text = text.format(result["title"], result["url_after"], result["time"])

    link = result["link"]
    if link:
        link_text = hide_link(result["link"])
        new_text = link_text + new_text
    else:
        # на случай, если не удалось загрузить картинку на телеграф, отправим ее следом
        await core.bot.send_photo(chat_id, FSInputFile(result["image"]))

    await core.bot.edit_message_text(new_text, chat_id, message_id, reply_markup=get_picture_keyboard(lang),
                                     parse_mode=ParseMode.HTML)
    await core.write_db_success(user_id, result["url_before"], result["time"])


async def do_url_answer(chat_id: int, message_id: int, user_id: int, url: str, lang: Language):
    result = await core.capture_screenshot(url=url, file_name=utils.get_image_name(user_id, url))

    if result["error"]:
        await url_error_answer(chat_id, message_id, user_id, result, lang)
    else:
        link = await utils.get_image_link(result["image"], core.bot.session)
        result["link"] = link
        await url_answer(chat_id, message_id, user_id, result, lang)


async def do_capture_url(msg: Message, url: str, lang: Language, inplace: bool = False):
    """Обрабатывает URL
    Если inplace = True - то редактирует существующее сообщение
    """
    new_msg = await url_make_stub(msg, lang, inplace)
    url = utils.prepare_url(url)

    if settings.WORKER_USED:
        await core.queue.get_image(chat_id=new_msg.chat.id,
                                   message_id=new_msg.message_id,
                                   user_id=msg.from_user.id,
                                   url=url,
                                   language=lang)
    else:
        await do_url_answer(new_msg.chat.id, new_msg.message_id, msg.from_user.id, url, lang)


async def whois_callback_answer(callback: CallbackQuery, lang: Language):
    """Выводит сообщение  WHOIS"""
    url = utils.prepare_url(callback.message.reply_to_message.text)
    result_dict = await url_info.whois(url)

    # переводим название параметров и склеиваем в строку для отображения
    result = []
    for key, value in result_dict.items():
        result.append(f"{_(key, lang)}: {value}")

    text = "\n".join(result)

    await callback.answer(text=text, show_alert=True)


async def geoip_callback_answer(callback: CallbackQuery, lang: Language):
    """Выводит сообщение  GeoIP"""
    url = utils.prepare_url(callback.message.reply_to_message.text)
    result_dict = await url_info.geo_ip(url)

    # переводим название параметров и склеиваем в строку для отображения
    result = []
    for key, value in result_dict.items():
        result.append(f"{_(key, lang)}: {value}")

    text = "\n".join(result)

    await callback.answer(text=text, show_alert=True)


async def lang_callback_answer(callback: CallbackQuery, lang: Language):
    """Сообщение с выбором языка"""
    text = _(AppMessage.LANGUAGE_SELECT, lang)
    await callback.message.edit_text(text, reply_markup=get_lang_keyboard(lang))


async def do_lang_change(callback: CallbackQuery):
    """Изменение языка"""

    new_lang = callback.data.split(":")[1]
    user = callback.from_user
    lang = Language(new_lang)
    await core.set_user_language(user, lang)

    msg = await callback.message.edit_text(_(AppMessage.LANGUAGE_CHANGED, lang).format(lang))
    await start_answer(msg, lang)


async def not_url(msg: Message, lang: Language):
    """Отвечает на текстовое сообщение - не URL"""
    text = _(AppMessage.UNKNOWN_URL_MSG, lang).format(msg.text)
    await msg.answer(text)


async def dont_know(msg: Message, lang: Language):
    """Отвечает на не текстовое сообщение"""
    text = _(AppMessage.DONT_KNOW_MSG, lang)
    await msg.answer(text)


async def stat_answer(msg: Message, lang: Language):
    """Обработка /stat  - выводит статистику"""
    text = _(AppMessage.STATISTIC, lang)
    requests_for_day, requests_for_month = await core.get_statistics()
    new_text = text.format(requests_for_day, requests_for_month)
    await msg.answer(new_text)
