from abc import ABC, abstractmethod
import datetime
import requests
from bs4 import BeautifulSoup
import requests


import entities


class MinorParser(ABC):
    "Interface for parser-classes."

    @abstractmethod
    def get_soup(self, url: str):
        pass

    @abstractmethod
    def parse_url(self, soup: BeautifulSoup):
        pass

    @abstractmethod
    def get_list_of_new_events():
        return list


class KlinParkParser(MinorParser):
    """Parse http://www.klin-park.ru/afisha/."""

    __url = "http://www.klin-park.ru/afisha/"

    def get_soup(self, url: str):
        response = requests.get(url)

        if response.status_code != 200:
            print("!!! Parsing error for " + url)

        return BeautifulSoup(response.text, features="html.parser")


    def parse_url(self, soup: BeautifulSoup):
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

    
    def get_list_of_new_events(self):
        "Returns list of Events."
        return self.parse_url(self.get_soup(self.__url))



# !!! TODO: need to rewrite:
class KlinCityParser(MinorParser):
    "Parse https://www.klincity.ru/events/"

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
