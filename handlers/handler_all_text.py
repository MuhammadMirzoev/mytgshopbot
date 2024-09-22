# импортируем ответ пользователю
from settings.message import MESSAGES
from settings import config, utility
# импортируем класс родитель
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопоки
    """

    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_catalog(self, message):
        """
        Обработка события нажатия на кнопку 'Каталог'. А точне
        это выбор категории товаров
        """
        self.bot.send_message(message.chat.id, MESSAGES['catalog'],
                              reply_markup=self.keybords.catalog_menu())


    def pressed_btn_about_us(self, message):
        """
        Обработка события нажатия на кнопку 'О бренде'
        """
        self.bot.send_photo(message.chat.id, photo=open('img/img.png', 'rb'), caption=MESSAGES['about_us'],
                              reply_markup=self.keybords.about_us_menu())

    def pressed_btn_bukket(self, message):
        """
        Обработка события нажатия на кнопку 'Корзина'
        """
        self.bot.send_message(message.chat.id, MESSAGES['bukket'])
        orders = self.BD.get_orders_by_user_id(message.from_user.id)
        if len(orders) > 0:
            self.bot.send_message(message.chat.id, f'Ваши заказы')
            for i in orders:
                product = self.BD.get_product(i.product_id)
                self.bot.send_message(message.chat.id, f'{product.name} {product.price} {i.quantity}')
        else:
            self.bot.send_message(message.chat.id, 'Вы еще не сделали ни одного заказа')

    def pressed_btn_faq(self, message):
        """
        Обработка события нажатия на кнопку 'Частые вопросы'
        """
        self.bot.send_message(message.chat.id, MESSAGES['faq'], reply_markup=self.keybords.about_us_menu())

    def pressed_btn_tech_support(self, message):
        """
        Обработка события нажатия на кнопку 'Связаться с нами'
        """
        self.bot.send_message(message.chat.id, MESSAGES['tech_support'], reply_markup=self.keybords.tech_support_menu())

    def pressed_btn_order(self, message):
        """
        Обработка события нажатия на кнопку 'Связаться с нами'
        """
        self.bot.send_message(message.chat.id, MESSAGES['order'])


    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['ABOUT_US']:
                self.pressed_btn_about_us(message)

            elif message.text == config.KEYBOARD['CATALOG']:
                self.pressed_btn_catalog(message)

            elif message.text == config.KEYBOARD['BUKKET']:
                self.pressed_btn_bukket(message)

            elif message.text == config.KEYBOARD['ORDER']:
                self.pressed_btn_order(message)

            elif message.text == config.KEYBOARD['FAQ']:
                self.pressed_btn_faq(message)

            elif message.text == config.KEYBOARD['TECH_SUPPORT']:
                self.pressed_btn_tech_support(message)
