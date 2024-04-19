from enum import Enum


class Language(str, Enum):
    RU = "ru"
    EN = "en"

    def __str__(self):
        return self.value


class AppMessage(str, Enum):
    START = "start"
    STUB = "stub"
    RESULT = "result"
    ERROR = "error"
    UNKNOWN_URL = "unknown_url"
    DONT_KNOW = "dont_know"
    BTN_ADD_ME = "add_me"
    BTN_LANGUAGE_SELECT = "btn_language_select"
    LANGUAGE_SELECT = "language_select"
    LANGUAGE_CHANGED = "language_changed"
    BTN_REPEAT = "repeat"
    BTN_INFO = "info"
    BTN_RUS = "rus"
    BTN_EN = "en"
    DOMEN_NAME = "domain_name"
    REGISTRAR = "registrar"
    CREATION_DATE = "creation_date"
    EXPIRATION_DATE = "expiration_date"
    UPDATED_DATE = "updated_date"
    NAME_SERVERS = "name_servers"
    REGISTRANT_ORGANIZATION = "registrant_organization"
    STATISTIC = "statistic"


hello_text_ru = """
👋 Привет! Меня зовут *ImagerClone*.
Я - Бот для создания веб-скриншотов.
Чтобы получить скриншот - отправьте URL адрес сайта.
Например, wikipedia.org\n
• С помощью бота вы можете проверять подозрительные ссылки. (_Айпилоггеры, фишинговые веб-сайты, скримеры и т.п_)\n
• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи.\n
"""

hello_text_en = """
👋 Welcome! My name is ImagerClone.
I'm here for creating capture a website screenshot. To get a screenshot - submit the URL of the Website.
For example wikipedia.org\n
• With the help of the bot, you can check suspicious links. (_IPloggers, phishing websites, screamers, etc._)\n
• You can also add me to your chats so that I can check the links that the group chat members send.\n
"""

rus_text = {
    AppMessage.START: hello_text_ru,
    AppMessage.STUB: "⚡️***Запрос отправлен на сайт***",
    AppMessage.RESULT: (
        "<b>Заголовок страницы:</b> {0}\n" "<b>Веб-сайт:</b> {1}\n" "<b>Время обработки, сек:</b> {2:.4f}\n"
    ),
    AppMessage.ERROR: "***Произошла ошибка!***",
    AppMessage.BTN_ADD_ME: "Добавить меня в чат",
    AppMessage.LANGUAGE_SELECT: "👩🏼‍💻 Выберите язык",
    AppMessage.BTN_LANGUAGE_SELECT: "🇷🇺 Выбор языка",
    AppMessage.LANGUAGE_CHANGED: "Язык изменен на {0}",
    AppMessage.BTN_REPEAT: "🌀Обновить страницу",
    AppMessage.BTN_INFO: "🔬Подробнее",
    AppMessage.BTN_RUS: "🇷🇺 Русский",
    AppMessage.BTN_EN: "🇬🇧 English",
    AppMessage.DOMEN_NAME: "Домен",
    AppMessage.REGISTRAR: "Регистратор",
    AppMessage.CREATION_DATE: "Дата регистрации",
    AppMessage.EXPIRATION_DATE: "Окончание регистрации",
    AppMessage.UPDATED_DATE: "Обновлено",
    AppMessage.NAME_SERVERS: "NS сервера",
    AppMessage.REGISTRANT_ORGANIZATION: "Организация",
    AppMessage.UNKNOWN_URL: "Непонятный URL: {0}",
    AppMessage.DONT_KNOW: "Я не знаю что делать с этим...",
    AppMessage.STATISTIC: "*Запросов в день:* {0}\n*Запросов в месяц:* {1}",
}

en_text = {
    AppMessage.START: hello_text_en,
    AppMessage.STUB: "⚡️***Request sent to website***",
    AppMessage.RESULT: ("<b>Title:</b> {0}\n" "<b>Website:</b> {1}\n" "<b>Time of processing, sec:</b> {2:.4f}"),
    AppMessage.ERROR: "***Error occurred!***",
    AppMessage.BTN_ADD_ME: "Add me to chat",
    AppMessage.LANGUAGE_SELECT: "👩🏼‍💻 Choose your language",
    AppMessage.BTN_LANGUAGE_SELECT: "🇬🇧 Language selection",
    AppMessage.LANGUAGE_CHANGED: "Language changed to {0}",
    AppMessage.BTN_REPEAT: "🌀Refresh",
    AppMessage.BTN_INFO: "🔬More",
    AppMessage.BTN_RUS: "🇷🇺 Русский",
    AppMessage.BTN_EN: "🇬🇧 English",
    AppMessage.DOMEN_NAME: "Domain",
    AppMessage.REGISTRAR: "Registrar",
    AppMessage.CREATION_DATE: "Creation_date",
    AppMessage.EXPIRATION_DATE: "Expiration_date",
    AppMessage.UPDATED_DATE: "updated",
    AppMessage.NAME_SERVERS: "NS servers",
    AppMessage.REGISTRANT_ORGANIZATION: "Organization",
    AppMessage.UNKNOWN_URL: "Unknown URL: {0}",
    AppMessage.DONT_KNOW: "I don't know what this is...",
    AppMessage.STATISTIC: "*Requests per day:* {0}\n*Requests per month:* {1}",
}

text = {Language.RU: rus_text, Language.EN: en_text}


def _(key: AppMessage, lang: Language = Language.RU) -> str:
    if key in text[lang]:
        result = text[lang][key]

    elif key in text[Language.RU]:
        result = text[Language.RU][key]

    else:
        result = key.value

    return result
