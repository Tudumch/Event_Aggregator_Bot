import datetime


from unittest import TestCase
from bot_master import BotMaster 
from entities import Event
from db_handler import DB_handler


# Test-DB config:
test_db_name = "TestDB.db"
connection_info_dict = {"lite_db_name": test_db_name}

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
        self.db_handler = DB_handler(con_dict=connection_info_dict)
        self.bot_master = BotMaster(self.db_handler)
        self.db_handler.create_events_table()
        self.db_handler.put_list_of_events(list_of_test_events)

    def test_get_message_with_new_events(self):
        correct_str = ("Doors Day\n2022-03-01\n\nLocks Day\n" +
                str(datetime.date.today() + datetime.timedelta(days=2000)) +
                "\n\n" + 
                "Windows Day\n" + 
                str(datetime.date.today() + datetime.timedelta(days=6)) + 
                "\n\n")
        result_str = self.bot_master.get_message_with_new_events(
                list_of_test_events)
        self.assertEqual(result_str, correct_str)

    def test_get_message_with_weekly_events(self):
        correct_str = ("Windows Day\n" + 
                str(datetime.date.today() + datetime.timedelta(days=6)) + 
                "\n\n")
        result_str = self.bot_master.get_message_with_weekly_events()
        self.assertEqual(result_str, correct_str)


