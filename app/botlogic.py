from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

import core
import utils
import url_info
from app.keyboards import get_lang_keyboard, get_picture_keyboard, get_start_keyboard
from app.locales import AppMessage, Language, _


async def start_answer(msg: Message, lang: Language):
    text = _(AppMessage.START, lang)
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_start_keyboard(lang))


async def url_make_stub(msg: Message, lang: Language, inplace: bool = False) -> Message:
    """Создает в ответ сообщение-заглушку и возвращает это сообщение
    Если inplace = True - то редактирует существующее сообщение
    """
    text = _(AppMessage.STUB, lang)
    if inplace:
        new_msg = await msg.edit_media(
            media=InputMediaPhoto(media=core.empty_pic, caption=text, parse_mode=ParseMode.MARKDOWN)
        )
    else:

        new_msg = await msg.reply_photo(photo=core.empty_pic, caption=text, parse_mode=ParseMode.MARKDOWN)

    core.empty_pic = new_msg.photo[-1].file_id
    return new_msg


async def url_error_answer(msg: Message, result: dict, lang: Language):
    """Редактирует сообщение - сообщает об ошибке"""
    text = _(AppMessage.ERROR, lang)
    await msg.edit_media(
        media=InputMediaPhoto(caption=text, media=core.empty_pic, parse_mode=ParseMode.MARKDOWN),
        reply_markup=get_picture_keyboard(lang),
    )
    await core.write_db_error(msg.from_user, result["url_before"])


async def url_answer(msg: Message, result: dict, lang: Language):
    """Редактирует сообщение - сообщает об успешном обработке"""

    screenshot = FSInputFile(result["path"])
    text = _(AppMessage.RESULT, lang)
    new_text = text.format(result["title"], result["url_after"], result["time"])
    await msg.edit_media(
        media=InputMediaPhoto(caption=new_text, media=screenshot, parse_mode=ParseMode.HTML),
        reply_markup=get_picture_keyboard(lang),
    )
    await core.write_db_success(msg.from_user, result["url_before"], result['time'])


async def do_capture_url(msg: Message, url: str, lang: Language, inplace: bool = False):
    """Обрабатывает URL
    Если inplace = True - то редактирует существующее сообщение
    """
    new_msg = await url_make_stub(msg, lang, inplace)

    url = utils.prepare_url(url)
    result = await core.capture_screenshot(url=url, file_name=utils.get_image_name(msg.from_user.id, url))

    if result["error"]:
        await url_error_answer(new_msg, result, lang)
    else:
        await url_answer(new_msg, result, lang)


async def whois_callback_answer(callback: CallbackQuery, lang: Language):
    """Выводит сообщение  WHOIS"""
    url = utils.prepare_url(callback.message.reply_to_message.text)
    result_dict = await url_info.whois(url)

    # переводим название параметров и склеиваем в строку для отображения
    result = []
    for key, value in result_dict.items():
        result.append(f"{_(key, lang)}: {value}")

    text = "\n".join(result)

    await callback.answer(text=text, show_alert=True, parse_mode=ParseMode.MARKDOWN)


async def geoip_callback_answer(callback: CallbackQuery, lang: Language):
    """Выводит сообщение  GeoIP"""
    url = utils.prepare_url(callback.message.reply_to_message.text)
    result_dict = await url_info.geo_ip(url)

    # переводим название параметров и склеиваем в строку для отображения
    result = []
    for key, value in result_dict.items():
        result.append(f"{_(key, lang)}: {value}")

    text = "\n".join(result)

    await callback.answer(text=text, show_alert=True, parse_mode=ParseMode.MARKDOWN)


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
    text = _(AppMessage.UNKNOWN_URL, lang).format(msg.text)
    await msg.answer(text)


async def dont_know(msg: Message, lang: Language):
    text = _(AppMessage.DONT_KNOW, lang)
    await msg.answer(text)


async def stat_answer(msg: Message, lang: Language):
    text = _(AppMessage.STATISTIC, lang)
    requests_for_day, requests_for_month = await core.get_statistics()
    new_text = text.format(requests_for_day, requests_for_month)
    await msg.answer(new_text, parse_mode=ParseMode.MARKDOWN)
