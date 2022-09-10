import psycopg2
import datetime

from entities import Event
from config import (pSQL_adress, pSQL_db_name, pSQL_password, pSQL_username, 
        list_of_test_events, list_of_another_test_events)


list_of_new_events = []


# Connection to postgreSQL server and create table if not exists:
with psycopg2.connect(host=pSQL_adress, database=pSQL_db_name,
        user=pSQL_username, password=pSQL_password) as connection:
    connection.autocommit = True 
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT version();
                """)
        print("Server version: " + str(cursor.fetchone()))

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS events(
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) DEFAULT 'NO_TITLE',
                event_date DATE, 
                date_added DATE DEFAULT CURRENT_TIMESTAMP
                );
                """)

def execute_query(query: str):
    with psycopg2.connect(host=pSQL_adress, database=pSQL_db_name,
            user=pSQL_username, password=pSQL_password) as connection:
        connection.autocommit = True 

        cursor = connection.cursor() 
        cursor.execute(query)
        return cursor


def get_list_of_events():
    "Returns list of Events"

    events_list = []
    query = "SELECT * FROM events"
    data_list = execute_query(query).fetchall()

    for record in data_list:
        events_list.append(Event(record[0], record[1], record[2], record[3]))

    return events_list


def put_list_of_events(list_of_events: list):
    """
    Checks are the same events from list already in DB. 
    If not - puts them into DB

    Returns list of events, which were added into DB.
    """


    global list_of_new_events
    list_of_events_from_db = get_list_of_events()

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

    list_of_events_from_db = get_list_of_events()
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


