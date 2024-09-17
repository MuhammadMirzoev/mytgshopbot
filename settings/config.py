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
    'ORDER': emojize('⚡ Оформить заказ'),
    'BUKKET': emojize('🛒 Корзина'),
    'FAQ': emojize('❓ Частые вопросы'),
    'TECH_SUPPORT': emojize('💬 Связаться с нами'),
}