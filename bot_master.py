from db_handlers import DB_handler

from parsers import KlinParkParser as KPP


list_of_new_events = []
greetings_message = ("Привет!\n"
"Я буду присылать тебе уведомления обо всех новых мероприятиях, которые "
"найду на клинских сайтах новостей.\n"
"А по команде '/week' я могу показать список всех городских мероприятий, "
"которые пройдут в ближайшие 7 дней.")
weekly_events_not_found_message = """
        На следующие 7 дней я не смог найти запланированных мероприятий.
        """


def refresh_db():
    """
    Create 'events'-table into DB if it already not exists, gets new parsed 
    events from parsers and puts only newly, none-deplicated events into DB.
    Returns list of events ADDED into DB.
    """

    global list_of_new_events

    db_handler = DB_handler()
    db_handler.create_events_table()

    KlinParkParser = KPP()
    list_of_parsed_events = KlinParkParser.get_list_of_new_events() # update DB
    list_of_new_events = db_handler.put_list_of_events(list_of_parsed_events)

    return db_handler


class BotMaster():
    """
    Class through which bot-instances centrally receive various information 
    about events.
    """

    def __init__(self):
        self.db_handler = refresh_db()
        self.greetings_message = greetings_message
        self.weekly_events_not_found_message = weekly_events_not_found_message

    def make_message_from_events(self, list_of_events: list):
        """
        Concatinates event titile and event_date attrs of every Event in 
        one string message for future sending into messages.
        """

        list_of_stringed_events = ""
        for event in list_of_events:
            list_of_stringed_events += (event.title + "\n" +
                    str(event.event_date) + "\n\n")
        return list_of_stringed_events

    def get_weekly_list(self):
        "Returns string of events that will happen in next 7 days."
        return self.make_message_from_events(
                self.db_handler.get_events_sheduled_for(7))

    def get_new_events(self):
        """
        Gets newly added events from var in main-function and returns them as a 
        text for bots.
        """
        return self.make_message_from_events(list_of_new_events)


# One Bot_Master-instance for all different platforms bot-instances access:
Bot_Master_Parent = BotMaster()


if __name__ == "__main__":
    bot_master = BotMaster()

