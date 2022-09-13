import requests


from unittest import TestCase, main
from parsers import KlinParkParser


class parsersTest(TestCase):

    def setUp(self):
        self.KlinParkParser = KlinParkParser()
    

    def test_urls_availability(self):
        response_KlinPark = requests.get(self.KlinParkParser._url).status_code
        self.assertEqual(response_KlinPark, 200)


    def test_returns_list(self):
        list_of_events = self.KlinParkParser.get_list_of_new_events()
        self.assertEqual(type(list_of_events), list)
  


if __name__ == "__main__":
	main()
