import config
import entities
import requests
import datetime

from bs4 import BeautifulSoup
import parser_KlinCity, parser_KlinPark 


def parse_events(urls_list: list):
    """
    Returns list of Events
    """

    events_list = []

    for url in urls_list:
        response = requests.get(url)
        # !!! какая-то проблема с requests

        soup = BeautifulSoup(response.text)

        if url == "http://www.klin-park.ru/afisha/":
            events_list.extend(parser_KlinPark.run(soup))
        if url == "https://www.klincity.ru/events/":
            pass
            events_list.extend(parser_KlinCity.run(soup))

    return events_list

parse_events(config.urls_for_parsing)