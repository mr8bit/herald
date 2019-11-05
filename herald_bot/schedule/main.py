import re
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen
import datetime
import pytz
from django.core.cache import cache


def get_by_date(group, date):
    msc = pytz.timezone('Europe/Moscow')
    today = datetime.datetime.now(msc).date()
    if re.fullmatch(r'\d{1,2}(\.\d{1,2}){0,4}', date):
        date = convert_date(date, today)
        if not date:
            return False
        schedule = get_schedule(group)
        lessons = search_for_date(date.strftime('%d.%m.%Y'), schedule)
        if lessons:
            output = ""
            for lesson in lessons:
                output+=prepare_message(lesson)
            return output
        else:
            return "🎉Занятия на этот день не найдены🥳"
    else:
        return False


def get_next_day(group):
    """
        Расписание на следующий день
    :param group:
    :return:
    """
    msc = pytz.timezone('Europe/Moscow')
    today = datetime.datetime.now(msc).date()
    next_day = datetime.timedelta(days=1) + today
    schedule = get_schedule(group)
    lessons = search_for_date(next_day.strftime('%d.%m.%Y'), schedule)
    output = ""
    for lesson in lessons:
        output += prepare_message(lesson)
    return output


def search_for_date(date, schedule):
    """
        Получаем расписание по датам
    :param date: Дата datetime
    :param schedule: Расписание list
    :return:
    """
    lessons = [lesson for lesson in schedule if lesson['date'] == date]
    lessons.sort(key=lambda lesson: int(lesson['start_time'].split(':')[0]))
    return lessons


def get_schedule(group):
    """
        Получить все расписание по номеру группы
    :param group: string representing student's group
    :return schedule: list of dicts <3
    """
    marks = ['date', 'dow', 'start_time', 'end_time', 'title', 'lecturer', 'place', 'type']
    group = quote(group)
    schedule = cache.get(group)
    if not schedule:
        url = f"https://mai.ru/education/schedule/data/{group}.txt"
        response = urlopen(url)
        response = response.read()
        schedule = response.decode('utf-8-sig')
        schedule = list(set(schedule.split('\n')))
        schedule = [data.split('\t') for data in schedule]
        schedule = [dict(zip(marks, lesson)) for lesson in schedule]
        cache.set(group, schedule)  # записыаем в кэш списки групп
    return schedule


def convert_date(date, today):
    """
        Конвертор даты в datetime
    :param date:
    :param today:
    :return:
    """
    date_parts = list(map(int, date.split('.')))

    if len(date_parts) >= 3 and date_parts[2] < 2000:
        date_parts[2] += 2000

    keys = ['day', 'month', 'year']
    kwargs = dict(zip(keys, date_parts))

    try:
        date = today.replace(**kwargs)
    except ValueError:
        return False

    return date


def prepare_message(lesson) -> str:
    """
        Оформление расписания
    :param lesson:
    :return:
    """
    incorrect_inputs = ['NONAME NONAME ', '', ' ']
    tag_groups = [
        ['start_time', 'end_time'],
        ['title', 'type'],
        ['lecturer'],
        ['place']
    ]
    formatters = (
        "⌚ {0} -- {1}",
        "📝 {0}, {1}",
        "👤 {0}",
        "📍 {0}\n"
    )
    lesson_data = []

    for tag_group in tag_groups:
        lesson_data_line = []
        for tag in tag_group:
            if not lesson[tag] in incorrect_inputs:
                lesson_data_line.append(lesson[tag])
        lesson_data.append(lesson_data_line)

    couples = zip(formatters, lesson_data)
    message = [couple[0].format(*couple[1]) for couple in couples if couple[1]]
    message = '\n'.join(message) + '\n\n'

    return message


if __name__ == '__main__':
    print(get_by_date("3О-501С-15", '06.11'))