from functools import lru_cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import core
from app.locales import AppMessage, Language, _


@lru_cache
def get_start_keyboard(lang: Language = Language.RU):
    btn_add_to_chat = InlineKeyboardButton(
        text=_(AppMessage.BTN_ADD_ME, lang), url=f"https://t.me/{core.bot_name}?startgroup=true"
    )
    btn_lang_choice = InlineKeyboardButton(text=_(AppMessage.BTN_LANGUAGE_SELECT, lang), callback_data="change_lang")

    start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn_add_to_chat], [btn_lang_choice]])
    return start_keyboard


@lru_cache
def get_picture_keyboard(lang: Language = Language.RU):
    btn_repeat = InlineKeyboardButton(text=_(AppMessage.BTN_REPEAT, lang), callback_data="repeat")
    btn_info = InlineKeyboardButton(text=_(AppMessage.BTN_INFO, lang), callback_data="info")
    geoip_btn = InlineKeyboardButton(text='🌎 GeoIP ', callback_data="geoip")

    picture_keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn_repeat], [btn_info, geoip_btn]])

    return picture_keyboard


@lru_cache
def get_lang_keyboard(lang: Language = Language.RU):
    btn_ru = InlineKeyboardButton(text=_(AppMessage.BTN_RUS, lang), callback_data=f"lang:{Language.RU.value}")

    btn_en = InlineKeyboardButton(text=_(AppMessage.BTN_EN, lang), callback_data=f"lang:{Language.EN.value}")

    lang_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[btn_ru, btn_en]])
    return lang_keyboard
