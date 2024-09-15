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

    def our_choice_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки
        """
        print(f'Кнопка нажата. Код: {code}')
        self.bot.answer_callback_query(call.id, 'еще сюда ниче не добавили')

    def handle(self):
        """
        Регистрация обработчиков callback-запросов
        """
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
            self.our_choice_btn(call, code)
