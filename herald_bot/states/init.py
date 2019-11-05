from herald_bot.handlers.core.state import BaseState as State
from herald_bot.schedule.group import check_group
from herald_bot.states.main import MainMenu


class BootStrapState(State):
    def on_trigger(self, trigger):
        try:
            trigger.create_user()
        except:
            trigger.get_user()
        return SelectLanguage()


class SelectLanguage(State):
    def __init__(self):
        self.buttons = ['🇷🇺Русский', '🇬🇧English']
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
        return EnterGroup()


"""
class SelectTypeEnterGroup(State):
    def __init__(self):
        self.buttons = ['Введу номер', 'Выберу из списка']
        self.text = 'Как хочешь выбрать свою группу?'

    def on_enter(self, trigger):
        trigger.send_keyboard(self.text, self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            return EnterGroup()
"""


class EnterGroup(State):
    def __init__(self):
        self.text = "Введите номер группы"
        self.buttons = ["✅Да", "❌Нет"]

    def on_enter(self, trigger):
        trigger.send_message(self.text)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            trigger.send_message("✅Группа выбрана\n💾Сохраняю вас")
            new_user = trigger.get_user()
            info = trigger.client.get_api().users.get(user_id=new_user.user_id)
            new_user.first_name = info[0]['first_name']
            new_user.second_name = info[0]['last_name']
            new_user.save()
            return MainMenu()
        elif trigger.text == self.buttons[1]:
            trigger.send_message("Попробуйте еще раз...")
            return EnterGroup()
        else:
            trigger.send_message("🕐Проверка номера группы может занять до 1 минуты\n🙃Пожалуйста подождите...")
            group = check_group(trigger.text)
            if group:
                trigger.send_keyboard(f"{group} - это ваша группа?", self.buttons)
                usr = trigger.get_user()
                usr.group = group
                usr.save()
            else:
                trigger.send_message("Не смог найти вашу группу ¯\_(ツ)_/¯\nПопробуйте еще раз")
                return EnterGroup()