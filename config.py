# ---------------------------------------------------------------------- 
# GLOBAL VARIABLES SETUP SECTION
# Sections with exclamations (!!!) are must be redifine with your own data!
# ---------------------------------------------------------------------- 

# !!!
# path to file in which placed your token for doscord-bot
# (see https://docs.pycord.dev/en/v2.0.0/discord.html#discord-intro 
# to know how to get one):
discord_bot_token_filePath = "discord_token"

# !!!
# provide ID of channel of your discord-server which will be used for 
# notifications about new events
# (see https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
discord_bot_channel_id = 1010249090010988586

# urls which will be parsed by parser:
urls_for_parsing = ["http://www.klin-park.ru/afisha/"] 
# !!! какая-то проблема при парсиге https://www.klincity.ru/events/

# refresh db every .. seconds (43200s == 12h):
refresh_time = 43200            


# ---------------------------------------------------------------------- 
# DATABASE SETUP SECTION
# If you don't know about databases - leave below sections by default.
# ---------------------------------------------------------------------- 

# SQLite
use_SQLite = True  # set True if you want use SQLite as Data Base
SQLite_db_path = "EventsDataBase.db"  

# PostgreSQL 
use_postgreSQL = False # set True if you want use postgreSQL as Data Base
pSQL_adress = "127.0.0.1"
pSQL_username = "postgres"
pSQL_password = ""
pSQL_db_name = "Event_Aggregator"

#use_SQLite, use_postgreSQL = use_postgreSQL, use_SQLite # TODO: delete this line!

def readTokenFromFile(filePath):
    """Bot-tokens should be saved in external file for security reasons."""

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
    datetime.date(2022, 3, 1), datetime.date(2022, 9, 5)), 
    Event(59, "День замков", 
        datetime.date(2022, 6, 1), datetime.date(2022, 9, 5)), 
    Event(923, "День окон", 
        datetime.date(2022, 12, 28), datetime.date(2022, 9, 5))]

list_of_another_test_events = list_of_test_events.copy()
list_of_another_test_events.append(Event(784, "День крыш", 
    datetime.date(2022, 6, 17),
    datetime.date(2022, 9, 5)))
