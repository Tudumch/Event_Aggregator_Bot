import requests
import datetime
from bs4 import BeautifulSoup

from .. import entities

def run(soup: BeautifulSoup):
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
