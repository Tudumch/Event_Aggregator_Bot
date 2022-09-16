import os
from unittest import TestCase


import sqlite3


from db_handlers import DB_handler
from config import SQLite_db_path 


test_db_name = "TestDB.db"
db_handler = DB_handler()


class DB_handlers_test(TestCase):

    def setUp(self):
        sqlite3.connect(test_db_name)   # create test DB

    def tearDown(self):
        os.remove(test_db_name)


    def test_sqlite_db_creation(self):
        """
        Checks can sqlite3 create DB or not.
        """

        con = sqlite3.connect("temp_" + test_db_name) 
        con.close()
        self.assertTrue(os.path.isfile("temp_" + test_db_name))
        os.remove("temp_" + test_db_name)
    
    def test_sqlite_connection_to_db(self):
        cursor = db_handler.connect_to_db()
        if len(SQLite_db_path.split("/")) == 1:
            self.assertTrue(os.path.isfile("../" + SQLite_db_path))
        else:
            self.assertTrue(os.path.isfile(SQLite_db_path))
        self.assertIsInstance(cursor, sqlite3.Cursor)



if __name__ == "__main__":
    db_handlers_test = DB_handlers_test()
    db_handlers_test.setUp()

    db_handlers_test.test_sqlite_db_creation()
    db_handlers_test.test_sqlite_connection_to_db()

    db_handlers_test.tearDown()
