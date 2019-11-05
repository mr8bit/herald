from herald_bot.handlers.core.state import BaseState as State
from herald_bot.states import settings
from herald_bot.schedule.main import get_next_day, get_by_date
import re


class MainMenu(State):
    def __init__(self):
        self.buttons = [
            '🔜Расписание на завтра',
            '🗓️Расписание по дате',
            '👨‍✈️Расписание преподавателя',
            '⚙Настройки',
            '💁Помощь'
        ]

    def on_enter(self, trigger):
        trigger.send_keyboard("Главное меню", self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            group = trigger.get_user().group
            trigger.send_message("🤔Выполняю запрос")
            lessons = get_next_day(group)
            if lessons:
                trigger.send_message("🙌Держи")
                trigger.send_message(lessons)
            else:
                trigger.send_message("🥳Завтра нету пар!")
            return MainMenu()
        elif trigger.text == self.buttons[1]:
            return GetScheduleByDate()
        elif trigger.text == self.buttons[2]:
            trigger.send_message("Тут еще ничего нет")
            return MainMenu()
        elif trigger.text == self.buttons[3]:
            return settings.Settings()
        else:
            trigger.send_keyboard("Не понял вас ¯\_(ツ)_/¯\nВыберите один из пунктов", self.buttons)


class GetScheduleByDate(State):
    def __init__(self):
        self.text = '🗓️Напиши в дату в формате дд.мм\nПример: 05.11'
        self.buttons = ["🔙Назад"]

    def on_enter(self, trigger):
        trigger.send_keyboard(self.text, self.buttons)

    def on_trigger(self, trigger):
        if trigger.text == self.buttons[0]:
            return MainMenu()
        group = trigger.get_user().group
        if re.fullmatch(r'\d{1,2}(\.\d{1,2}){0,4}', trigger.text):
            lessons = get_by_date(group, trigger.text)
            if lessons:
                trigger.send_message(lessons)
            else:
                trigger.send_message("😮При поиске расписания произшла ошибка, поробуйте другую дату")
        else:
            trigger.send_message("🤦‍♀️Не правильно введена дата")
        return GetScheduleByDate()