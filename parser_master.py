"""
Calls minor parsers and gather theirs outputs to one list of events.
"""


import requests
from bs4 import BeautifulSoup


import parser_minors
from config  import urls_for_parsing


class ParserMaster():

    def parse_urls_from_config(self):
        """
        Returns list of Events
        """

        events_list = []
        KlinParkParser = parser_minors.KlinParkParser()
        KlinCityParser = parser_minors.KlinCityParser()

        for url in urls_for_parsing:
            response = requests.get(url)
            # !!! какая-то проблема с requests при парсинге klinCity

            if response.status_code != 200:
                print("!!! Parsing error for " + url)

            soup = BeautifulSoup(response.text, features="html.parser")

            if url == "http://www.klin-park.ru/afisha/":
                events_list.extend(KlinParkParser.run(soup))
            if url == "https://www.klincity.ru/events/":
                events_list.extend(KlinCityParser.run(soup))

        return events_list
