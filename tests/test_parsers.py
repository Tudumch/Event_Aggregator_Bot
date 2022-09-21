from unittest import TestCase, main
from parsers import KlinParkParser, KlinCityParser
from entities import Event


class parsersTest(TestCase):

    def setUp(self):
        self.KlinParkParser = KlinParkParser()
        self.KlinCityParser = KlinCityParser()
        self.KlinPark_events_list = self.KlinParkParser.get_list_of_new_events()
        self.KlinCity_events_list = self.KlinParkParser.get_list_of_new_events()
    
    def test_returns_list(self):
        self.assertEqual(type(self.KlinPark_events_list), list)
        self.assertEqual(type(self.KlinCity_events_list), list)

    def test_content_type_in_lists(self):
        for event in self.KlinPark_events_list:
            self.assertIsInstance(event, Event)
        for event in self.KlinCity_events_list:
            self.assertIsInstance(event, Event)
  


if __name__ == "__main__":
	main()
