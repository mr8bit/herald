from herald_bot.handlers.core.state import BaseState as State
from herald_bot.utils import check_group


class BootStrapState(State):
    def on_trigger(self, trigger):
        try:
            trigger.get_user()
        except:
            trigger.create_user()
        return SelectLanguage()


class SelectLanguage(State):
    def __init__(self):
        self.buttons = ['Русский', 'English']
        self.text = 'Приветсвую, для начала выбери язык'

    def on_enter(self, trigger):
        trigger.send_keyboard(self.text, self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            usr = trigger.get_user()
            usr.language = 0
        if trigger.text == self.buttons[1]:
            usr = trigger.get_user()
            usr.language = 1
        return SelectTypeEnterGroup()


class SelectTypeEnterGroup(State):
    def __init__(self):
        self.buttons = ['Введу номер', 'Выберу из списка']
        self.text = 'Как хочешь выбрать свою группу?'


    def on_enter(self, trigger):
        trigger.send_keyboard(self.text, self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            return EnterGroup()


class EnterGroup(State):
    def __init__(self):
        self.text = "Введите номер группы"
        self.buttons = ["Да", "Нет"]

    def on_enter(self, trigger):
        trigger.send_message(self.text)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0] and not trigger.get_user().group:
            print("Выбрана группа")
        if trigger.text == self.buttons[1] and not trigger.get_user().group:
            trigger.send_message("Попробуйте еще раз...")
            return EnterGroup()
        else:
            trigger.send_message("Проверка номера группы.\nПодождите...")
            trigger.send_keyboard("Это ваша группа?", self.buttons)
