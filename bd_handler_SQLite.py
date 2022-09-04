import sqlite3
import datetime

import config
from entities import Event

db_path = "EventsDataBase.db"

with sqlite3.connect(db_path) as con: 
    cursor = con.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS events(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title VARCHAR(100) DEFAULT 'NO_TITLE', 
                    event_date DATE, 
                    date_added DATE DEFAULT CURRENT_TIMESTAMP);""")

def execute_query(DB_path: str, query: str):
    with sqlite3.connect(DB_path) as con: 
        cursor = con.cursor()
        cursor.execute(query)
        return cursor

def get_events_all():
    "Returns list of Events"

    events_list = []
    query = "SELECT * FROM events"
    data_list = execute_query(db_path, query).fetchall()

    for record in data_list:
        print(record)
        # !!! Надо как-то конвертировать timestamp в нормальную дату
        event_date = datetime.datetime(record[3])

get_events_all()
