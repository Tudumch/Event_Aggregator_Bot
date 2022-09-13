from unittest import TestCase, main
import parsers

class Parser_Minors_test(TestCase):

    def setUp(self):
        self.KlinParkParser = parser_minors.KlinParkParser()
        self.KlinCityParser = parser_minors.KlinCityParser()
    
    def test_returns_not_empty_list(self):
  
        self.assertEqual(type(self.KlinParkParser.run()), type(list))


if __name__ == "__main__":
	main()
