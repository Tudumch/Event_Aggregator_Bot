discord_bot_token_filePath = "discord_token"

urls_for_parsing = ["http://www.klin-park.ru/afisha/"] 
# !!! какая-то проблема при парсиге https://www.klincity.ru/events/

# PostgreSQL 
use_postgreSQL = True
pSQL_adress = "127.0.0.1"
pSQL_username = "postgres"
pSQL_password = ""
pSQL_db_name = "Event_Aggregator"


def readTokenFromFile(filePath):
    """Bot-tokens should be saved in external file for security reasons, 
    not in code."""

    with open(filePath, "r") as file:
        return file.read().rstrip()
        breakpoint()

token_discord = readTokenFromFile(discord_bot_token_filePath)


# ---------------------------------------------------------------------- 
# DEBUG SECTION
# ---------------------------------------------------------------------- 
from entities import Event
import datetime
list_of_test_events = [Event(432, "День дверей", 
    datetime.date(2022, 3, 21), datetime.date(2022, 9, 5)), 
    Event(59, "День замков", 
        datetime.date(2022, 6, 1), datetime.date(2022, 9, 5)), 
    Event(923, "День окон", 
        datetime.date(2022, 12, 28), datetime.date(2022, 9, 5))]

list_of_another_test_events = list_of_test_events.copy()

list_of_another_test_events.append(Event(784, "День крыш", 
    datetime.date(2022, 6, 17),
    datetime.date(2022, 9, 5)))
