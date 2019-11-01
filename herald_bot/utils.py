import difflib
import requests
from bs4 import BeautifulSoup


def check_group(group):
    page = requests.get('https://mai.ru/education/schedule/')
    soup = BeautifulSoup(page.text, "html.parser")
    link_group = soup.findAll("a", {"class": "sc-group-item"})
    groups = []
    for item in link_group:
        groups.append(item.text.strip())
    match = difflib.get_close_matches(group, groups)
    return match[0]