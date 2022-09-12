"""
This module contains functions for work with SQLite and postgreSQL databases.
"""

import datetime


import sqlite3
import psycopg2


from entities import Event
from config import (use_SQLite, use_postgreSQL, pSQL_adress, pSQL_db_name, 
        pSQL_password, pSQL_username, SQLite_db_path, list_of_test_events)


list_of_new_events = [] 


def connect_to_db():
    """
    Check variables from config-file and creates connection to database.
    Returns Cursor-object.
    """

    if use_SQLite:
        with sqlite3.connect(SQLite_db_path) as con: 
            cursor = con.cursor()

    elif use_postgreSQL:
        with psycopg2.connect(host=pSQL_adress, database=pSQL_db_name,
                user=pSQL_username, password=pSQL_password) as con:
            con.autocommit = True 
            cursor = con.cursor() 
    else:
        raise ValueError("Didn't set prefered DB in config-file!")

    print("Successful connection to Database.\n")
    return cursor



def create_events_table():
    """
    Connects to DB and checks is there 'events'-table.
    If there is none - create new one.
    """

    # SQLite and postgres have different types of values for id-row
    if use_SQLite:
        id_row = "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
    else:
        id_row = "id SERIAL PRIMARY KEY,"

    query = (" CREATE TABLE IF NOT EXISTS events(" + 
            id_row + """
            title VARCHAR(200) DEFAULT 'NO_TITLE',
            event_date DATE, 
            date_added DATE DEFAULT CURRENT_TIMESTAMP
            );
            """)

    execute_query(query)

    print("'events' table successfuly created!")


def convert_str_to_date(string: str):
    """
    This func converts date-string from DB to datetime.data(), because 
    SQLite3 does not do it automaticaly.

    Returns datetime.date() object.
    """
    
    date_list = list(map(int, string[0:10].split("-")))
    return datetime.date(date_list[0], date_list[1], date_list[2])


def execute_query(query: str):
    """
    Connects to DB and executes SQL-query.
    Returns cursor-object with result.
    """

    if use_SQLite:
        with sqlite3.connect(SQLite_db_path) as con: 
            cursor = con.cursor()
            cursor.execute(query)
    else:
        cursor = connect_to_db()
        cursor.execute(query)

    return cursor


def get_list_of_events(): 
    "Returns list of Events stored in DB."

    events_list = []
    query = "SELECT * FROM events ORDER BY event_date"
    raw_data = execute_query(query).fetchall()

    for record in raw_data:
        event_id = record[0]
        event_title = record[1]
        event_date = record[2]
        event_added = record[3]
        if use_SQLite:
            event_date = convert_str_to_date(record[2])
            event_added = convert_str_to_date(record[3])

        events_list.append(Event(event_id, event_title, event_date, event_added))

    print("Events from DB received!")
    return events_list


def put_list_of_events(list_of_events: list):
    """
    Checks are the same events from list already in DB. 
    If not - puts them into DB.

    Returns list of events, which were added into DB.
    """

    global list_of_new_events
    today = datetime.date.today()
    db_list_of_events = get_list_of_events()


    def check_for_outdates(list_of_events: list):
        filtered_list = []

        for event in list_of_events:
            if event.event_date >= today: 
                filtered_list.append(event)

        return filtered_list


    def check_for_duplicates(list_of_events: list):
        filtered_list = list_of_events.copy()

        for db_event in db_list_of_events:
            if len(filtered_list) == 0: break
            
            for event in list_of_events:
                if (event.title == db_event.title 
                        and event.event_date == db_event.event_date):
                    filtered_list.remove(event)
                    break

        return filtered_list


    # Put filtered list of events in DB
    list_of_events = check_for_outdates(list_of_events)
    list_of_events = check_for_duplicates(list_of_events)
    for event in list_of_events:
        execute_query("INSERT INTO events(title, event_date) " + 
                "VALUES('" + event.title + "', '" + str(event.event_date) + 
                "');")

    print("Data has wrote into DB successfuly!")
    list_of_new_events = list_of_events
    return list_of_new_events 


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


create_events_table()


#---------------------------------------------------------------------- 
# DEBUG
#---------------------------------------------------------------------- 
if __name__ == "__main__":
    put_list_of_events(list_of_test_events)
    execute_query("""INSERT INTO events(title, event_date)
VALUES('sfdsdsfsdf', '2022-09-03')""")
    print("GLOBAL list_of_new_events:", [i.title for i in list_of_new_events])

