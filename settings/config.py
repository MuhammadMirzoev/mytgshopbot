import os
from dotenv import load_dotenv
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize


load_dotenv()  # Загрузка переменных из файла .env

# токен выдается при регистрации приложения
TOKEN = os.getenv('TOKEN')

# DEBUG = True

# название БД
NAME_DB = os.getenv('NAME_DB')

# версия приложения
VERSION = os.getenv('VERSION')

# автор приложния
AUTHOR = os.getenv('AUTHOR')

# родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CATALOG': emojize('📙 Каталог'),
    'ABOUT_US': emojize('✨ О бренде'),
    'MY_ORDERS': emojize('🛒 Мои заказы'),
    'BONUSES': emojize('⚡ Бонусы за покупки'),
    'FAQ': emojize('❓ Частые вопросы'),
    'TECH_SUPPORT': emojize('💬 Связаться с нами'),

    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}
