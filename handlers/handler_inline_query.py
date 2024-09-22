# импортируем класс родитель
from handlers.handler import Handler
# импортируем сообщения пользователю
from settings.message import MESSAGES

class HandlerInlineQuery(Handler):
    """
    Класс обрабатывает входящие запросы на нажатие инлайн-кнопок
    """

    def __init__(self, bot):
        super().__init__(bot)
        # Инициализация обработчиков

    def show_product_msg(self, call, category_id, subcategory_id=3, num=0):
        products = self.BD.select_products(category_id, subcategory_id)
        self.bot.send_message(call.from_user.id, f'{products[num].name}', reply_markup=self.keybords.products_menu(category_id, subcategory_id, num))

    def handle(self):
        """
        Регистрация обработчиков callback-запросов
        """
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
            if code.startswith('<'):
                args = code.split('_')
                print(args)
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                self.show_product_msg(call, args[1], args[2], num=int(args[3]) - 1)
                return
            elif code.startswith('>'):
                args = code.split('_')
                self.bot.delete_message(call.message.chat.id, call.message.message_id)
                self.show_product_msg(call, args[1], args[2], num=int(args[3]) + 1)
                return
            categories = [str(i) for i in self.BD.select_all_categories()]
            if code[:-9] in categories:
                is_subcategory = True if len(self.BD.select_subcategories(code[:-9])) > 0 else False
                if is_subcategory:
                    self.bot.send_message(call.from_user.id, MESSAGES[code[:-9] + '_message'], reply_markup=self.keybords.subcategory_menu(code[:-9]))
                else:
                    category_id = self.BD.get_category_id_from_name(code[:-9])
                    self.show_product_msg(call, category_id)
            if code.startswith('subs'):
                args = code.split('_')
                self.show_product_msg(call, args[1], args[2])
            else:
                self.bot.answer_callback_query(call.id, 'еще сюда ниче не добавили')
