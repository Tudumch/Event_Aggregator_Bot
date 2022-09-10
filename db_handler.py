"""
This module contains functions for work with
SQLite and postgreSQL databases.
"""

import datetime


import sqlite3
import psycopg2


import config
from entities import Event
from config import (use_SQLite, use_postgreSQL, pSQL_adress, pSQL_db_name, 
        pSQL_password, pSQL_username, list_of_test_events, 
        list_of_another_test_events, lSQL_db_path)


list_of_new_events = []


def create_events_table():
    """
    Connect to DB and check is there 'events'-table.
    If there is none - create new one.
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
        cursor = None
        raise ValueError("Didn't set prefered DB in config-file!")

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


#---------------------------------------------------------------------- 
# DEBUG
#---------------------------------------------------------------------- 
# Check for create_events_table():
use_postgreSQL = False
use_SQLite = True
create_events_table()
