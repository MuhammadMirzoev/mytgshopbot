# импортируем класс родитель
from handlers.handler import Handler
from settings.message import MESSAGES


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start и /help и т.п.
    """
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_start(self, message):
        """
        обрабатывает входящие /start команды
        """
        self.bot.send_message(message.chat.id, MESSAGES['start'].format(message.from_user.first_name),
                              reply_markup=self.keybords.start_menu())
        self.bot.send_message(message.chat.id, '⚡')
        self.bot.send_message(message.chat.id, 'В честь открытия Nuage Orange мы дарим тебе скидку 20% на первый заказ. Чтобы предновогодние покупки были еще приятнее.')

    def handle(self):
        # обработчик(декоратор) сообщений,
        # который обрабатывает входящие /start команды.
        @self.bot.message_handler(commands=['start'])
        def handle(message):
            print(type(message))
            if message.text == '/start':
                self.pressed_btn_start(message)
