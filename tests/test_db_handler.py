import os
import datetime
from unittest import TestCase 


import sqlite3


from db_handler import DB_handler
from config import SQLite_db_path, use_SQLite
from entities import Event


test_db_name = "TestDB.db"
connection_info_dict = {"lite_db_name": test_db_name}
db_handler = DB_handler(con_dict=connection_info_dict)

# Test data:
list_of_test_events = [Event(432, "Doors Day", 
    datetime.date(2022, 3, 1), datetime.date(2022, 9, 5)), 
    Event(59, "Locks Day", datetime.date.today() + datetime.timedelta(days=2000), 
        datetime.date(2022, 9, 5)), 
    Event(923, "Windows Day", 
        datetime.date.today() + datetime.timedelta(days=6), 
        datetime.date(2022, 9, 5))]
another_list_of_test_events = list_of_test_events.copy()
another_list_of_test_events.append(Event(784, "Roofs Day", 
    datetime.date.today() + datetime.timedelta(days=2100), 
    datetime.date(2022, 9, 5)))


class DB_handlers_test(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        if os.path.isfile(test_db_name):
            os.remove(test_db_name)

    def test_connection_to_db(self):
        if use_SQLite == False:
            return 0
        cursor = db_handler.connect_to_db()
        if len(SQLite_db_path.split("/")) == 1:
            self.assertTrue(os.path.isfile("./" + SQLite_db_path))
        else:
            self.assertTrue(os.path.isfile(SQLite_db_path))
        self.assertIsInstance(cursor, sqlite3.Cursor)

    def test_query_execution_and_create_events_table(self):
        """
        Checks whether 'execute_query' and 'create_events_table' funcs
        works properly.
        """

        db_handler.create_events_table()
        cursor = db_handler.execute_query("""
                    SELECT name 
                    FROM sqlite_schema 
                    WHERE type ='table' AND name NOT LIKE 'sqlite_%';
                    """)
        records = cursor.fetchall()
        self.assertEqual(records[0][0], "events")

    def test_put_list_of_events_into_db(self):
        """
        Checks whether only new events that do not yet exist in the database 
        are inserted into it.
        """
        db_handler.create_events_table()
        inserted_events = db_handler.put_list_of_events(list_of_test_events)
        new_events = db_handler.put_list_of_events(another_list_of_test_events)
        self.assertEqual(["Locks Day", "Windows Day"], 
                [e.title for e in inserted_events])
        self.assertEqual(["Roofs Day"], 
                [e.title for e in new_events])

    def test_get_list_of_all_events_from_db(self):
        """
        Checks getting all events, stored into DB.
        """
        db_handler.create_events_table()
        db_handler.put_list_of_events(list_of_test_events)
        events_list = db_handler.get_list_of_events()
        self.assertEqual(["Windows Day", "Locks Day"], 
                [e.title for e in events_list])

    def test_get_list_of_events_sheduled_for_week(self):
        """
        Checks getting of events, which will happen in next 7 days.
        """
        db_handler.create_events_table()
        db_handler.put_list_of_events(list_of_test_events)
        events_list = db_handler.get_events_sheduled_for(7)
        self.assertEqual(["Windows Day"], 
                [e.title for e in events_list])

    def test_convert_str_to_datetime(self):
        string = "2022-12-23"
        date = db_handler._convert_str_to_date(string)
        self.assertEqual(type(date), datetime.date)
        
    def test_clear_overdues(self):
        """
        Checks are past events being deleted correctly.
        """

        db_handler.create_events_table()
        db_handler.execute_query("DELETE FROM events;")

        for event in list_of_test_events:
            db_handler.execute_query("INSERT INTO events(title, event_date) " + 
                    "VALUES('" + event.title + "', '" + str(event.event_date) + 
                    "');")

        events_list = db_handler.get_list_of_events()
        self.assertEqual(["Doors Day", "Windows Day", "Locks Day"], 
                [e.title for e in events_list])

        db_handler.clear_overdues()
        events_list = db_handler.get_list_of_events()
        self.assertEqual(["Windows Day", "Locks Day"], 
                [e.title for e in events_list])


