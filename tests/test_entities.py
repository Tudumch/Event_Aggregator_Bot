import datetime
from unittest import TestCase


from entities import Event


Event = Event(23, "My Test Event", 
        datetime.date.today() + datetime.timedelta(days=6), 
        datetime.date.today())


class Entities_Test(TestCase):

    def test_event_id_setter(self):
        with self.assertRaises(ValueError) as e:
            Event.event_id = "431"

    def test_title_setter(self):
        with self.assertRaises(ValueError) as e:
            Event.title = int(2023)

    def test_event_date_setter(self):
        with self.assertRaises(ValueError) as e:
            Event.event_date = 2023, 12, 3

    def test_date_added_setter(self):
        with self.assertRaises(ValueError) as e:
            Event.date_added = 2023, 12, 3
