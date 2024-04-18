import logging

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message

import botlogic
from filters import UrlFilter

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def start_handler(msg: Message):
    """Обработка команды /start"""
    logger.debug("Start command from {0}".format(msg.from_user.username))
    await botlogic.start_answer(msg)


@router.message(F.text, UrlFilter())
async def url_handler(msg: Message):
    """Обработка сообщения с URL"""
    logger.debug("url {1} from {0}".format(msg.from_user.username, msg.text))
    await botlogic.do_capture_url(msg, msg.text, inplace=False)


@router.message(F.text, F.chat.type == "private")
async def message_handler(msg: Message):
    """Обработка непонятных текстовых сообщений"""
    logger.debug("text {1} from {0}".format(msg.from_user.username, msg.text))
    await botlogic.not_url(msg)


@router.message(F.chat.type == "private")
async def end_handler(msg: Message):
    """Обработчик - заглушка всего остального"""
    logger.debug("message not text from {0}".format(msg.from_user.username))
    await botlogic.dont_know(msg)


@router.callback_query(F.data.startswith("info"))
async def info_handler(callback: types.CallbackQuery):
    """Обработка кнопки Подробнее - WHOIS"""
    logger.debug("callback INFO data:{1} from {0}".format(callback.from_user.username, callback.data))
    await botlogic.whois_callback_answer(callback)


@router.callback_query(F.data.startswith("repeat"))
async def repeat_handler(callback: types.CallbackQuery):
    """Обработка кнопки Повторить"""
    # обрабатываем нажатие на кнопку
    logger.debug("callback REPEAT data:{1} from {0}".format(callback.from_user.username, callback.data))
    await callback.answer()

    # запускаем обработку повторно
    url = callback.message.reply_to_message.text
    await botlogic.do_capture_url(callback.message, url, inplace=True)


@router.callback_query(F.data.startswith("change_lang"))
async def change_lang_handler(callback: types.CallbackQuery):
    """Обработка кнопки Выбор языка"""
    # обрабатываем нажатие на кнопку
    logger.debug("callback LANG_CHANGE data:{1} from {0}".format(callback.from_user.username, callback.data))
    await callback.answer()
    await botlogic.lang_callback_answer(callback)


@router.callback_query(F.data.startswith("lang"))
async def lang_handler(callback: types.CallbackQuery):
    """Обработка кнопки English/Russian"""
    # обрабатываем нажатие на кнопку
    logger.debug("callback LANG data:{1} from {0}".format(callback.from_user.username, callback.data))
    await callback.answer()
    await botlogic.do_lang_change(callback)
