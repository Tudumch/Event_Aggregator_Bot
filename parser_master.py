import config
import entities
import requests
import datetime

from bs4 import BeautifulSoup
import parser_KlinCity, parser_KlinPark 


def parse_urls_from_config():
    """
    Returns list of Events
    """

    urls_list = config.urls_for_parsing
    events_list = []

    for url in urls_list:
        response = requests.get(url)
        # !!! какая-то проблема с requests при парсинге klinCity

        if response.status_code != 200:
            print("!!! Неполадки при парсинге " + url)

        soup = BeautifulSoup(response.text, features="html.parser")

        if url == "http://www.klin-park.ru/afisha/":
            events_list.extend(parser_KlinPark.run(soup))
        if url == "https://www.klincity.ru/events/":
            events_list.extend(parser_KlinCity.run(soup))

    return events_list
