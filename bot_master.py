from db_handlers import DB_handler

from parsers import KlinParkParser, KlinCityParser 
from log_handler import logger


greetings_message = ("Привет!\n"
"Я буду присылать тебе уведомления обо всех новых мероприятиях, которые "
"найду на клинских сайтах новостей.\n"
"А по команде '/week' я могу показать список всех городских мероприятий, "
"которые пройдут в ближайшие 7 дней.")
weekly_events_not_found_message = """
        На следующие 7 дней я не смог найти запланированных мероприятий.
        """


class BotMaster():
    """
    Class through which bot-instances centrally receive various information 
    about events from DB.
    """

    def __init__(self, db_handler: DB_handler):
        self.db_handler = db_handler
        self.greetings_message = greetings_message
        self.weekly_events_not_found_message = weekly_events_not_found_message
        self.list_of_new_events = []

    def refresh_db(self):
        """
        Create 'events'-table into DB if it not exists already, gets new parsed 
        events from parsers and puts only newly, none-duplicated events into DB.
        Updates self.list_of_new_events var.
        """
        self.db_handler.create_events_table()

        KPP = KlinParkParser()
        KCP = KlinCityParser()
        list_of_parsed_events = (KPP.get_list_of_new_events() + 
                KCP.get_list_of_new_events())

        self.list_of_new_events = self.db_handler.put_list_of_events(
                list_of_parsed_events)
        self.db_handler.clear_overdues()

    def get_message_with_new_events(self, list_of_events=[]):
        """
        Concatinates event title and event_date attrs of every Event in list 
        into one string message for future sending into messengers.
        """

        if len(list_of_events) == 0:
            list_of_events = self.list_of_new_events

        list_of_stringed_events = ""

        for event in list_of_events:
            list_of_stringed_events += (event.title + "\n" +
                    str(event.event_date) + "\n\n")
        return list_of_stringed_events

    def get_message_with_weekly_events(self):
        "Returns string of events that will happen in next 7 days."
        message = self.get_message_with_new_events(self.db_handler.get_events_sheduled_for(7))
        if message == "":
            return "На следующие 7 дней мероприятий не запланированно."
        else:
            return message


# One Bot_Master-instance for all different platforms bot-instances access:

logger.info("Creating BotMaster...")
Bot_Master_Parent = BotMaster(DB_handler())
Bot_Master_Parent.refresh_db()
logger.info("BotMaster successfuly created.")


if __name__ == "__main__":
    bot_master = BotMaster(DB_handler())

