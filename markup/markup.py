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
        itm_btn_3 = self.set_btn('ORDER')
        itm_btn_4 = self.set_btn('BUKKET')
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
        self.markup = InlineKeyboardMarkup()
        categories = self.BD.select_all_categories()
        print(categories)
        itm_btn_1 = self.set_inline_btn((str(categories[0]), f'{categories[0]}_callback'))
        itm_btn_2 = self.set_inline_btn((str(categories[1]), f'{categories[1]}_callback'))
        itm_btn_3 = self.set_inline_btn((str(categories[2]), f'{categories[2]}_callback'))
        itm_btn_4 = self.set_inline_btn((str(categories[3]), f'{categories[3]}_callback'))
        itm_btn_5 = self.set_inline_btn((str(categories[4]), f'{categories[4]}_callback'))
        itm_btn_6 = self.set_inline_btn((str(categories[5]), f'{categories[5]}_callback'))
        itm_btn_7 = self.set_inline_btn((str(categories[6]), f'{categories[6]}_callback'))
        itm_btn_8 = self.set_inline_btn((str(categories[7]), f'{categories[7]}_callback'))

        self.markup.row(itm_btn_1, itm_btn_2)
        self.markup.row(itm_btn_3)
        self.markup.row(itm_btn_4)
        self.markup.row(itm_btn_5, itm_btn_6)
        self.markup.row(itm_btn_7, itm_btn_8)

        return self.markup

    def subcategory_menu(self, category):
        self.markup = InlineKeyboardMarkup()
        subs = self.BD.select_subcategories(category)
        category_id = self.BD.get_category_id_from_name(category)
        for i in range(len(subs)):
            itm_btn = self.set_inline_btn((str(subs[i]), f'subs_{category_id}_{subs[i].id}_callback'))
            self.markup.row(itm_btn)

        return self.markup

    def products_menu(self, category, subcategory=3, num=0):
        self.markup = InlineKeyboardMarkup()
        products = self.BD.select_products(category, subcategory)
        num = num % len(products)
        itm_btn_1 = self.set_inline_btn((f'Купить | {products[num].price} руб', f'order_{products[num].id}_callback'))
        itm_btn_2 = self.set_inline_btn(('<', f'<_{category}_{subcategory}_{num}_callback'))
        itm_btn_3 = self.set_inline_btn((f'{num + 1}/{len(products)}', f'order_{products[num].id}_callback'))
        itm_btn_4 = self.set_inline_btn(('>', f'>_{category}_{subcategory}_{num}_callback'))

        self.markup.add(itm_btn_1)
        self.markup.add(itm_btn_2, itm_btn_3, itm_btn_4)

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

