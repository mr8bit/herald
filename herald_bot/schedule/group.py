import difflib
import requests
from bs4 import BeautifulSoup
from django.core.cache import cache


def check_group(group):
    """
        Валидатор номера группы
    :str group: Номер группы
    :return str or none: Номер группы или ничего
    """
    groups = cache.get('list_group')  # если ничего нет, то кэш вернет None
    if not groups:  # Если None (not False), то обновляем БД
        page = requests.get('https://mai.ru/education/schedule/')  # Берем страицу со всеми группами
        soup = BeautifulSoup(page.text, "html.parser")  # Парсим страницу
        link_group = soup.findAll("a", {"class": "sc-group-item"})  # Собираем только группы
        groups = []
        for item in link_group:
            groups.append(item.text.strip())  # Берем только текст
        cache.set('list_group', groups)  # записыаем в кэш списки групп
    match = difflib.get_close_matches(group, groups)  # Ищем наиболее похожую группу на ту что ввел пользователь
    try:
        return match[0]  # возвращаем первую похожую группу
    except:
        return None  # ничего не получилось найти
