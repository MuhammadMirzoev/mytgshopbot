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

    def toxines_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Токсины"
        """
        self.bot.send_message(call.from_user.id, 'Токсины', reply_markup=self.keybords.toxines_menu())

    def fillers_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Филлеры"
        """
        self.bot.send_message(call.from_user.id, 'Филлеры', reply_markup=self.keybords.fillers_menu())

    def lipolitiks_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Липолитики"
        """
        pass

    def pillings_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Пиллинги"
        """
        pass

    def anestetiks_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Анестетики"
        """
        pass

    def cons_btn(self, call, code):
        """
        Обрабатывает входящие запросы на нажатие кнопки "Расходники"
        """
        pass


    def handle(self):
        """
        Регистрация обработчиков callback-запросов
        """
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
            if code == 'toxines_callback':
                self.toxines_btn(call, code)
            elif code == 'fillers_callback':
                self.fillers_btn(call, code)
            # elif code == 'lipolitiks_callback':
            #    self.lipolitiks_btn(call, code)
            # elif code == 'pillings_callback':
            #    self.pillings_btn(call, code)
            # elif code == 'anestetiks_callback':
            #    self.anestetiks_btn(call, code)
            #elif code == 'cons_callback':
            #    self.cons_btn(call, code)
            else:
                self.bot.answer_callback_query(call.id, 'еще сюда ниче не добавили')
