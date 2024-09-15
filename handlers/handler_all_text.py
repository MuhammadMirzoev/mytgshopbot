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

    def pressed_btn_bonuses(self, message):
        """
        Обработка события нажатия на кнопку 'Настройки'
        """
        self.bot.send_message(message.chat.id, MESSAGES['bonuses'])

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

    def pressed_btn_my_orders(self, message):
        """
        Обработка события нажатия на кнопку 'Связаться с нами'
        """
        self.bot.send_message(message.chat.id, '''Логика еще не продуманна''')

    def pressed_btn_back(self, message):
        """
        Обработка события нажатия на кнопку 'Назад'
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точне
        это выбор товара из категории
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              config.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(
                                  config.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())

    def pressed_btn_order(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Заказ'.
        """
        # обнуляем данные шага
        self.step = 0
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество в каждой позиции товара в заказе
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        """
        Отправляет ответ пользователю при выполнении различных действий
        """
        self.bot.send_message(message.chat.id,MESSAGES['order_number'].format(
            self.step+1), parse_mode="HTML")
        self.bot.send_message(message.chat.id,
                              MESSAGES['order'].
                              format(self.BD.select_single_product_name(
                                  product_id),
                                     self.BD.select_single_product_title(
                                         product_id),
                                     self.BD.select_single_product_price(
                                         product_id),
                                     self.BD.select_order_quantity(
                                         product_id)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.orders_menu(
                                  self.step, quantity))

    def pressed_btn_up(self, message):
        """
        Обработка нажатия кнопки увеличения
        количества определенного товара в заказе
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар есть
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_douwn(self, message):
        """
        Обработка нажатия кнопки уменьшения
        количества определенного товара в заказе
        """
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем количество конкретной позиции в заказе
        quantity_order = self.BD.select_order_quantity(count[self.step])
        # получаем количество конкретной позиции в пролуктов
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        # если товар в заказе есть
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            # вносим изменения в БД orders
            self.BD.update_order_value(count[self.step],
                                       'quantity', quantity_order)
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        """
        Обработка нажатия кнопки удаления
        товарной позиции заказа
        """
        # получаем список всех product_id заказа
        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:
            # получаем количество конкретной позиции в заказе
            quantity_order = self.BD.select_order_quantity(count[self.step])
            # получаем количество товара к конкретной
            # позиции заказа для возврата в product
            quantity_product = self.BD.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            # вносим изменения в БД orders
            self.BD.delete_order(count[self.step])
            # вносим изменения в БД product
            self.BD.update_product_value(count[self.step],
                                         'quantity', quantity_product)
            # уменьшаем шаг
            self.step -= 1

        count = self.BD.select_all_product_id()
        # если список не пуст
        if count.__len__() > 0:

            quantity_order = self.BD.select_order_quantity(count[self.step])
            # отправляем пользователю сообщение
            self.send_message_order(count[self.step], quantity_order, message)

        else:
            # если товара нет в заказе отправляем сообщение
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.category_menu())

    def pressed_btn_back_step(self, message):
        """
        Обработка нажатия кнопки перемещения
        к более ранним товарным позициям заказа
        """
        # уменьшаем шаг пока шаг не будет равет "0"
        if self.step > 0:
            self.step -= 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        """
        Обработка нажатия кнопки перемещения
        к более поздним товарным позициям заказа
        """
        # увеличиваем шаг пока шаг не будет равет количеству строк
        # полей заказа с расчетом цены деления начиная с "0"
        if self.step < self.BD.count_rows_order() - 1:
            self.step += 1
        # получаем список всех товаров в заказе
        count = self.BD.select_all_product_id()
        # получаем еоличество конкретного товара в соответствие с шагом выборки
        quantity = self.BD.select_order_quantity(count[self.step])

        # отправляем ответ пользователю
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apllay(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Оформить заказ'.
        """
        # отправляем ответ пользователю
        self.bot.send_message(message.chat.id,
                              MESSAGES['applay'].format(
                                  utility.get_total_coas(self.BD),

                                  utility.get_total_quantity(self.BD)),
                              parse_mode="HTML",
                              reply_markup=self.keybords.category_menu())
        # отчищаем данные с заказа
        self.BD.delete_all_order()

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие текстовые сообщения от нажатия кнопок.
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            # ********** меню ********** #

            if message.text == config.KEYBOARD['ABOUT_US']:
                self.pressed_btn_about_us(message)

            elif message.text == config.KEYBOARD['CATALOG']:
                self.pressed_btn_catalog(message)

            elif message.text == config.KEYBOARD['MY_ORDERS']:
                self.pressed_btn_my_orders(message)

            elif message.text == config.KEYBOARD['BONUSES']:
                self.pressed_btn_bonuses(message)

            elif message.text == config.KEYBOARD['FAQ']:
                self.pressed_btn_faq(message)

            elif message.text == config.KEYBOARD['TECH_SUPPORT']:
                self.pressed_btn_tech_support(message)

            elif message.text == config.KEYBOARD['<<']:
                self.pressed_btn_back(message)

            elif message.text == config.KEYBOARD['ORDER']:
                # если есть заказ
                if self.BD.count_rows_order() > 0:
                    self.pressed_btn_order(message)
                else:
                    self.bot.send_message(message.chat.id,
                                          MESSAGES['no_orders'],
                                          parse_mode="HTML",
                                          reply_markup=self.keybords.
                                          category_menu())

            # ********** меню (категории товара, ПФ, Бакалея, Мороженое)******
            elif message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.pressed_btn_product(message, 'SEMIPRODUCT')

            elif message.text == config.KEYBOARD['GROCERY']:
                self.pressed_btn_product(message, 'GROCERY')

            elif message.text == config.KEYBOARD['ICE_CREAM']:
                self.pressed_btn_product(message, 'ICE_CREAM')

            # ********** меню (Заказа)**********

            elif message.text == config.KEYBOARD['UP']:
                self.pressed_btn_up(message)

            elif message.text == config.KEYBOARD['DOUWN']:
                self.pressed_btn_douwn(message)

            elif message.text == config.KEYBOARD['X']:
                self.pressed_btn_x(message)

            elif message.text == config.KEYBOARD['BACK_STEP']:
                self.pressed_btn_back_step(message)

            elif message.text == config.KEYBOARD['NEXT_STEP']:
                self.pressed_btn_next_step(message)

            elif message.text == config.KEYBOARD['APPLAY']:
                self.pressed_btn_apllay(message)
            # иные нажатия и ввод данных пользователем
            else:
                self.bot.send_message(message.chat.id, message.text)