from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, Message

from app import core, utils
from app.keyboards import get_lang_keyboard, get_picture_keyboard, get_start_keyboard
from app.locales import AppMessage, Language, _

lang = Language.EN


async def start_answer(msg: Message):
    text = _(AppMessage.START, lang)
    await msg.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_start_keyboard(lang))


async def url_make_stub(msg: Message, inplace: bool = False) -> Message:
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


async def url_error_answer(msg: Message):
    """Редактирует сообщение - сообщает об ошибке"""
    text = _(AppMessage.ERROR, lang)
    await msg.edit_media(
        media=InputMediaPhoto(caption=text, media=core.empty_pic, parse_mode=ParseMode.MARKDOWN),
        reply_markup=get_picture_keyboard(lang),
    )


async def url_answer(msg: Message, result: dict):
    """Редактирует сообщение - сообщает об успешном обработке"""
    screenshot = FSInputFile(result["path"])
    text = _(AppMessage.RESULT, lang)
    new_text = text.format(result["title"], result["url"], result["time"])
    await msg.edit_media(
        media=InputMediaPhoto(caption=new_text, media=screenshot, parse_mode=ParseMode.HTML),
        reply_markup=get_picture_keyboard(lang),
    )


async def do_capture_url(msg: Message, url: str, inplace: bool = False):
    """Обрабатывает URL
    Если inplace = True - то редактирует существующее сообщение
    """
    new_msg = await url_make_stub(msg, inplace)

    url = utils.prepare_url(url)
    result = await core.capture_screenshot(url=url, file_name=utils.get_image_name(msg.from_user.id, url))

    if result["error"]:
        await url_error_answer(new_msg)
    else:
        await url_answer(new_msg, result)


async def whois_callback_answer(callback: CallbackQuery):
    """Редактирует сообщение - сообщает об успешном обработке"""
    url = utils.prepare_url(callback.message.reply_to_message.text)
    result_dict = await utils.whois(url)

    # переводим название параметров и склеиваем в строку для отображения
    result = []
    for key, value in result_dict.items():
        result.append(f"{_(key, lang)}: {value}")

    text = "\n".join(result)

    await callback.answer(text=text, show_alert=True)


async def lang_callback_answer(callback: CallbackQuery):
    """Сообщение с выбором языка"""
    text = _(AppMessage.LANGUAGE_SELECT, lang)
    await callback.message.edit_text(text, reply_markup=get_lang_keyboard(lang))


async def do_lang_change(callback: CallbackQuery):
    """Изменение языка"""
    global lang

    new_lang = callback.data.split(":")[1]

    lang = Language(new_lang)
    # set_language(user_id, new_lang)
    msg = await callback.message.edit_text("Язык изменен на {0}".format(new_lang))
    await start_answer(msg)


async def not_url(msg: Message):
    text = _(AppMessage.UNKNOWN_URL, lang).format(msg.text)
    await msg.answer(text)


async def dont_know(msg: Message):
    text = _(AppMessage.DONT_KNOW, lang)
    await msg.answer(text)
