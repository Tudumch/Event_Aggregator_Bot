import sqlite3
import datetime

import config
from entities import Event


db_path = config.lSQL_db_path
list_of_new_events = []


with sqlite3.connect(db_path) as con: 
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS events(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title VARCHAR(100) DEFAULT 'NO_TITLE', 
                    event_date DATE, 
                    date_added DATE DEFAULT CURRENT_TIMESTAMP);""")


def convert_str_to_date(string: str):
    """
    This func converts date-string from DB to datetime.data, because 
    SQLite3 does not do it automaticaly.
    Returns datetime.date() object
    """
    
    date_list = list(map(int, string[0:10].split("-")))
    return datetime.date(date_list[0], date_list[1], date_list[2])


def execute_query(query: str):
    """
    Connects to DB and returns cursor-object.
    """
    with sqlite3.connect(db_path) as con: 
        cursor = con.cursor()
        cursor.execute(query)
        return cursor


def get_list_of_events_all():
    "Returns list of Events"

    events_list = []
    query = "SELECT * FROM events"
    data_list = execute_query(query).fetchall()

    for record in data_list:
        event_date = convert_str_to_date(record[2])
        date_added = convert_str_to_date(record[3])
        events_list.append(Event(int(record[0]), record[1], 
            event_date, date_added))

    return events_list


def put_list_of_events(list_of_events: list):
    """
    Checks are the same events from list already in DB. 
    If not - puts them into DB

    Returns list of events, which were added into DB.
    """

    global list_of_new_events
    list_of_events_from_db = get_list_of_events_all()

    # Check for duplicates in DB
    for db_event in list_of_events_from_db:
        if len(list_of_events) == 0:
            break

        for event in list_of_events:
            if (event.title == db_event.title 
                    and event.event_date == db_event.event_date):
                list_of_events.remove(event)
                break

    # Put remaining events in DB
    for event in list_of_events:
        execute_query("INSERT INTO events(title, event_date) " + 
                "VALUES('" + event.title + "', '" + str(event.event_date) + 
                "');")

    list_of_new_events = list_of_events
    return list_of_events


def get_events_sheduled_for(number_of_days: int):
    "Returns events from DB, which will happen in next number_of_days"

    today_date = datetime.date.today()
    number_of_days = datetime.timedelta(days=number_of_days)
    zero_day = datetime.timedelta(days=0)

    list_of_events_from_db = get_list_of_events_all()
    filtered_list = []

    for event in list_of_events_from_db:
        if (zero_day <= (event.event_date - today_date) <= number_of_days):
            filtered_list.append(event)

    return filtered_list


def clear_overdues():
    "Deletes all events whose dates have already passed"
    
    execute_query("""
            DELETE FROM events
            WHERE event_date < CURRENT_DATE;
            """)


