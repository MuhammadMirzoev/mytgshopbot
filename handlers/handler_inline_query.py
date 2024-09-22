# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю
from settings.message import MESSAGES, order_msg


class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие запросы на нажатие инлайн-кнопок
    """

    def __init__(self, bot):
        super().__init__(bot)
        # Инициализация обработчиков

    def show_product_msg(self, call, category_id, subcategory_id=3, num=0):
        products = self.BD.select_products(category_id, subcategory_id)
        num = num % len(products)
        self.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text=f'{products[num].name}', reply_markup=self.keybords.products_menu(category_id, subcategory_id, num))

    def order_product_msg(self, call, category_id, product_id, num, quantity=1, subcategory_id=3, delivery=0):
        product = self.BD.get_product(product_id)

        self.bot.edit_message_text(chat_id=call.message.chat.id,
                                   message_id=call.message.message_id,
                                   text=f'{product.name}',
                                   reply_markup=self.keybords.make_order_menu(category_id, subcategory_id, product_id, num, quantity, delivery))

    def make_order(self, call, product_id, quantity, delivery):
        self.BD.set_order(quantity, product_id, call.from_user.id)
        self.bot.send_message(call.from_user.id, 'Вы сделали заказ !')

    def handle(self):
        """
        Регистрация обработчиков callback-запросов
        """
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            categories = [str(i) for i in self.BD.select_all_categories()]
            if code.isdigit():
                code = int(code)

            if code.startswith('delivery'):
                args = code.split('_')
                print(args[6])
                self.order_product_msg(call, category_id=args[1], subcategory_id=args[2], product_id=args[3], num=args[4], quantity=int(args[5]), delivery=int(args[6]))
            elif code.startswith('+'):
                args = code.split('_')
                self.order_product_msg(call, category_id=args[1], subcategory_id=args[2], product_id=args[3], num=args[4], quantity=int(args[5]) + 1, delivery=int(args[6]))
            elif code.startswith('-'):
                args = code.split('_')
                self.order_product_msg(call, category_id=args[1], subcategory_id=args[2], product_id=args[3],
                                       num=args[4], quantity=int(args[5]) - 1 if int(args[5]) > 1 else 1, delivery=int(args[6]))
            elif code.startswith('<'):
                args = code.split('_')
                self.show_product_msg(call, args[1], args[2], num=int(args[3]) - 1)
            elif code.startswith('>'):
                args = code.split('_')
                self.show_product_msg(call, args[1], args[2], num=int(args[3]) + 1)
            elif code[:-9] in categories:
                is_subcategory = True if len(self.BD.select_subcategories(code[:-9])) > 0 else False
                if is_subcategory:
                    self.bot.send_message(call.from_user.id, MESSAGES[code[:-9] + '_message'], reply_markup=self.keybords.subcategory_menu(code[:-9]))
                else:
                    category_id = self.BD.get_category_id_from_name(code[:-9])
                    self.show_product_msg(call, category_id)
            elif code.startswith('subs'):
                args = code.split('_')
                self.show_product_msg(call, args[1], args[2])
            elif code.startswith('order'):
                args = code.split('_')
                self.order_product_msg(call, category_id=args[2], subcategory_id=args[3], product_id=args[1], quantity=1, num=args[4])
            elif code.startswith('make_order'):
                args = code.split('_')
                self.make_order(call, product_id=args[2], quantity=args[3], delivery=args[4])
            else:
                self.bot.answer_callback_query(call.id, 'еще сюда ниче не добавили')

