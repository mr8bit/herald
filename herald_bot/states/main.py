from herald_bot.handlers.core.state import BaseState as State
from .utils import DEFAULT, POSITIVE

class MainMenu(State):
    def __init__(self):
        self.buttons = [
            'Расписание на завтра',
            'Расписание по дате',
            'Настройки'
        ]

    def on_enter(self, trigger):
        trigger.send_keyboard("Главное меню", self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            trigger.send_message("Тут еще ничего нет")
            return MainMenu()
        if trigger.text == self.buttons[1]:
            trigger.send_message("Тут еще ничего нет")
            return MainMenu()
        if trigger.text == self.buttons[2]:
            trigger.send_message("Тут еще ничего нет")
            return MainMenu()