import config
import entities
import requests
import datetime

from bs4 import BeautifulSoup

def parse_events(urls_list: list):
    """
    Returns list of Events
    """
    events_list = []

    for url in urls_list:
        response = requests.get(url)
# !!! какая-то проблема с requests

        soup = BeautifulSoup(response.text) 

        # Klin-Park parser:
        if url == "http://www.klin-park.ru/afisha/":
            raw_events_list = soup.findAll('div', 
                    class_="entry shved clearfix")

            for raw_event in raw_events_list:
                event_title = raw_event.find('div', 
                        class_="entry-title").text

                raw_event_date = raw_event.find('ul', 
                        class_="entry-meta clearfix").text.strip().split(' ')
                event_date = datetime.date(int(raw_event_date[2]),
                        int(raw_event_date[1]), int(raw_event_date[0]))

                event = entities.Event(0, event_title, event_date, 
                        datetime.date.today())

                events_list.append(event)

        # KlinCity parser:
        if url == "1https://www.klincity.ru/events/":
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

parse_events(config.urls_for_parsing)

