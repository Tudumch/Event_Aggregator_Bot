"""
This module contains functions for work with SQLite and postgreSQL databases.
"""

import datetime


import sqlite3
import psycopg2


import config
from entities import Event
from config import (use_SQLite, use_postgreSQL, pSQL_adress, pSQL_db_name, 
        pSQL_password, pSQL_username, list_of_test_events, 
        list_of_another_test_events, lSQL_db_path)


list_of_new_events = [] # TODO: проверить можно ли обойтись без этой переменной


def connect_to_db():
    """
    Check variables from config-file and makes connection to database.
    Returns cursor-object.
    """

    if use_SQLite:
        with sqlite3.connect(lSQL_db_path) as con: 
            cursor = con.cursor()
    elif use_postgreSQL:
        with psycopg2.connect(host=pSQL_adress, database=pSQL_db_name,
                user=pSQL_username, password=pSQL_password) as con:
            con.autocommit = True 
            cursor = con.cursor() 
    else:
        raise ValueError("Didn't set prefered DB in config-file!")

    return cursor



def create_events_table(cursor):
    """
    Connects to DB and checks is there 'events'-table.
    If there is none - create new one.
    """

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS events(
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) DEFAULT 'NO_TITLE',
            event_date DATE, 
            date_added DATE DEFAULT CURRENT_TIMESTAMP
            );
            """)

    print("Successful connection to Database.")


def convert_str_to_date(string: str):
    """
    This func converts date-string from DB to datetime.data(), because 
    SQLite3 does not do it automaticaly.
    Returns datetime.date() object
    """
    
    date_list = list(map(int, string[0:10].split("-")))
    return datetime.date(date_list[0], date_list[1], date_list[2])


def execute_query(query: str):
    """
    Connects to DB and executes SQL-query.
    Returns cursor-object with result.
    """

    cursor = connect_to_db()
    cursor.execute(query)
    return cursor


def get_list_of_events(): # TODO: rename to get_list_of_events
    "Returns list of Events"

    events_list = []
    query = "SELECT * FROM events"
    raw_data = execute_query(query).fetchall()

    for record in raw_data:
        events_list.append(Event(record[0], record[1], record[2], record[3]))

    return events_list


def put_list_of_events(list_of_events: list):
    """
    Checks are the same events from list already in DB. 
    If not - puts them into DB

    Returns list of events, which were added into DB.
    """

    global list_of_new_events
    db_list_of_events = get_list_of_events()

    def check_for_duplicates():
        for db_event in db_list_of_events:
            for event in list_of_events:
                if (event.title == db_event.title 
                        and event.event_date == db_event.event_date):
                    list_of_events.remove(event)
                    break
                
            if len(list_of_events) == 0: break

    # Put non-duplicated events in DB
    check_for_duplicates()
    for event in list_of_events:
        execute_query("INSERT INTO events(title, event_date) " + 
                "VALUES('" + event.title + "', '" + str(event.event_date) + 
                "');")

    list_of_new_events = list_of_events
    return list_of_events


def get_events_sheduled_for(number_of_days):
    "Returns list of events from DB, which will happen in next number_of_days"

    filtered_list = []

    today = datetime.date.today()
    number_of_days = datetime.timedelta(days=number_of_days)
    zero_day = datetime.timedelta(days=0)

    db_list_of_events = get_list_of_events()

    for event in db_list_of_events:
        if (zero_day <= (event.event_date - today) <= number_of_days):
            filtered_list.append(event)

    return filtered_list


def clear_overdues():
    "Deletes all events whose dates have already passed."
    
    execute_query("""
            DELETE FROM events
            WHERE event_date < CURRENT_DATE;
            """)


#---------------------------------------------------------------------- 
# DEBUG
#---------------------------------------------------------------------- 
# Check create_events_table():
use_postgreSQL = False
use_SQLite = True
create_events_table(connect_to_db)
