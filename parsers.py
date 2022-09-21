from abc import ABC, abstractmethod
import datetime
import re

from bs4 import BeautifulSoup
import urllib.request
import ssl

from entities import Event
from log_handler import logger

        
class MinorParser(ABC):
    """Interface for parser-classes."""

    def __init__(self):
        self._url = ""

    def _get_soup(self, url: str):
        scontext = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        scontext.check_hostname = False
        scontext.verify_mode = ssl.VerifyMode.CERT_NONE
        with urllib.request.urlopen(url = url, context=scontext) as f:
            response = f.read()

        return BeautifulSoup(response, features="html.parser")

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

            event = Event(0, event_title, event_date,
                                   datetime.date.today())
            events_list.append(event)

        if len(events_list) == 0:
            logger.warning("Not found any events at " + self._url + " ! " + 
                    "Perhaps need to change parser-template...")

        return events_list


class KlinCityParser(MinorParser):
    """
    Parse https://www.klincity.ru/events/
    """

    def __init__(self):
        self._url = "https://www.klincity.ru/events/"

    def _parse_url(self, soup: BeautifulSoup):
        events_list = []
        raw_events_list = soup.findAll('div',
                                       class_="shved-item")

        for raw_event in raw_events_list:
            event_title = raw_event.find('div',
                                         class_="head").text
            raw_preview_list = raw_event.find('div',
                                              class_="preview_text")

            # looking for any dates in raw_preview_list with REGEX:
            raw_event_date = re.findall(r"\d\d\.\d\d\.\d\d\d\d", 
                    str(raw_preview_list))[0].split(".")
            event_date = datetime.date(int(raw_event_date[2]),
                    int(raw_event_date[1]), int(raw_event_date[0]))
            
            event = Event(0, event_title, event_date, 
                    datetime.date.today())
            events_list.append(event)

        if len(events_list) == 0:
            logger.warning("Not found any events at " + self._url + " ! " + 
                    "Perhaps need to change parser-template...")

        return events_list


if __name__ == "__main__":
    parser1 = KlinParkParser()
    test_list1 = parser1.get_list_of_new_events()
    parser2 = KlinCityParser()
    test_list2 = parser2.get_list_of_new_events()
    print(test_list1 + test_list2)
