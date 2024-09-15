# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# импортируем настройки и утилиты
from settings import config
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """
    # инициализация разметки

    def __init__(self):
        self.markup = None
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """

        if name == "AMOUNT_ORDERS":
            config.KEYBOARD["AMOUNT_ORDERS"] = "{} {} {}".format(step + 1,
                                                                 ' из ', str(
                    self.BD.count_rows_order()))

        if name == "AMOUNT_PRODUCT":
            config.KEYBOARD["AMOUNT_PRODUCT"] = "{}".format(quantity)

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Создает разметку кнопок в основном меню и возвращает разметку
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('ABOUT_US')
        itm_btn_2 = self.set_btn('CATALOG')
        itm_btn_3 = self.set_btn('MY_ORDERS')
        itm_btn_4 = self.set_btn('BONUSES')
        itm_btn_5 = self.set_btn('FAQ')
        itm_btn_6 = self.set_btn('TECH_SUPPORT')
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6)
        return self.markup

    def about_us_menu(self):
        """
        Создает разметку кнопок в меню 'О бренде'
        """
        self.markup = InlineKeyboardMarkup()
        itm_btn_1 = self.set_inline_btn(('Документы', 'documents_callback'))
        self.markup.row(itm_btn_1)
        return self.markup

    def tech_support_menu(self):
        """
        Создает разметку кнопок в меню 'Связаться с нами'
        """
        self.markup = InlineKeyboardMarkup()
        itm_btn_1 = self.set_inline_btn(('Документы', 'documents_callback'))
        itm_btn_2 = self.set_inline_btn(('Ссылка на менеджера', 'manager_callback'))
        self.markup.row(itm_btn_1, itm_btn_2)
        return self.markup

    @staticmethod
    def remove_menu():
        """
        Удаляет кнопки
        """
        return ReplyKeyboardRemove()

    def catalog_menu(self):
        """
        Создает разметку кнопок в меню каталога товаров
        """
        print('sf')
        self.markup = InlineKeyboardMarkup()
        itm_btn_1 = self.set_inline_btn(('Наш выбор', 'our_choice_callback'))
        itm_btn_2 = self.set_inline_btn(('Тело', 'body_callback'))
        itm_btn_3 = self.set_inline_btn(('Лицо', 'face_callback'))
        itm_btn_4 = self.set_inline_btn(('Дом', 'home_callback'))
        itm_btn_5 = self.set_inline_btn(('Наборы', 'kits_callback'))

        self.markup.row(itm_btn_1)
        self.markup.row(itm_btn_2, itm_btn_3)
        self.markup.row(itm_btn_4, itm_btn_5)

        return self.markup

    @staticmethod
    def set_inline_btn(name):
        """
        Создает и возвращает инлайн кнопку по входным параметрам
        """
        if type(name) == tuple:
            return InlineKeyboardButton(name[0],
                                    callback_data=name[1])
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создает разметку инлайн-кнопок в
        выбранной категории товара и возвращает разметку
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # загружаем в название инлайн кнопок данные
        # с БД в соответствие с категорией товара
        for itm in self.BD.select_all_products_category(category):
            self.markup.add(self.set_inline_btn(itm))

        return self.markup

    def orders_menu(self, step, quantity):
        """
        Создает разметку кнопок в заказе товара и возвращает разметку
        """

        self.markup = ReplyKeyboardMarkup(True, True)
        itm_btn_1 = self.set_btn('X', step, quantity)
        itm_btn_2 = self.set_btn('DOUWN', step, quantity)
        itm_btn_3 = self.set_btn('AMOUNT_PRODUCT', step, quantity)
        itm_btn_4 = self.set_btn('UP', step, quantity)

        itm_btn_5 = self.set_btn('BACK_STEP', step, quantity)
        itm_btn_6 = self.set_btn('AMOUNT_ORDERS', step, quantity)
        itm_btn_7 = self.set_btn('NEXT_STEP', step, quantity)
        itm_btn_8 = self.set_btn('APPLAY', step, quantity)
        itm_btn_9 = self.set_btn('<<', step, quantity)
        # рассположение кнопок в меню
        self.markup.row(itm_btn_1, itm_btn_2, itm_btn_3, itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6, itm_btn_7)
        self.markup.row(itm_btn_9, itm_btn_8)

        return self.markup
