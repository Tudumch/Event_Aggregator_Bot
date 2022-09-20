from abc import ABC, abstractmethod
import datetime
import requests
from bs4 import BeautifulSoup
import requests

import entities
from log_handler import logger


class MinorParser(ABC):
    """Interface for parser-classes."""

    def __init__(self):
        self._url = ""

    def _get_soup(self, url: str):
        response = requests.get(url)

        if response.status_code != 200:
            print("!!! Parsing error for " + url)
            logger.error("parsers.py: couldn't parse " + url)

        return BeautifulSoup(response.text, features="html.parser")

    @abstractmethod
    def _parse_url(self, soup: BeautifulSoup):
        pass

    def get_list_of_new_events(self):
        """Returns list of Events."""
        return self._parse_url(self._get_soup(self._url))


class KlinParkParser(MinorParser):
    """
    Parser for http://www.klin-park.ru/afisha/
    """

    def __init__(self):
        self._url = "http://www.klin-park.ru/afisha/"

    def _parse_url(self, soup: BeautifulSoup):
        "Returns list of Events."

        events_list = []
        raw_events_list = soup.findAll('div',
                                       class_="entry shved clearfix")

        for raw_event in raw_events_list:
            event_title = raw_event.find('div',
                                         class_="entry-title").text.strip('\n').strip()

            raw_event_date = raw_event.find('ul',
                                            class_="entry-meta clearfix").text.strip().split(' ')

            event_date = datetime.date(int(raw_event_date[2]),
                                       int(raw_event_date[1]), int(raw_event_date[0]))

            event = entities.Event(0, event_title, event_date,
                                   datetime.date.today())
            events_list.append(event)

        return events_list


# !!! TODO: need to rewrite:
class KlinCityParser(MinorParser):
    """Parse https://www.klincity.ru/events/"""

    _url = "https://www.klincity.ru/events/"

    def get_soup(self):
        pass

    def parse_url(self):
        pass

    def get_list_of_new_events(self):
        pass

    def run(self, soup: BeautifulSoup):
        events_list = []
        raw_events_list = soup.findAll('div',
                                       class_="shved-item")

        for raw_event in raw_events_list:
            event_title = raw_event.find('div',
                                         class_="head").text

            raw_preview_list = raw_event.find('div',
                                              class_="preview_text")
            print(raw_preview_list)

            """
            event_date = datetime.date(int(raw_event_date[2]),
                    int(raw_event_date[1]), int(raw_event_date[0]))

            event = entities.Event(0, event_title, event_date, 
                    datetime.date.today())

            events_list.append(event)
            """
        return events_list


if __name__ == "__main__":
    parser1 = KlinParkParser()
    test_list = parser1.get_list_of_new_events()
    print(test_list)
