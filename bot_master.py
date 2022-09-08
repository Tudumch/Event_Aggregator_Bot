"""
This module implements all custum functions accessible for bots.
"""

import config
if config.use_postgreSQL: import handler_postgreSQL as sql_handler
else: import handler_SQLite as sql_handler


greetings_message = ("Привет!\n"
"Я буду присылать тебе уведомления обо всех новых мероприятиях, которые "
"найду на клинских сайтах новостей.\n"
"А по команде '/week' я могу показать список всех городских мероприятий, "
"которые пройдут в ближайшие 7 дней.")

def make_message_from_events(list_of_events: list):
    """
    Concatinates event titile and event_date attrs of every Event in 
    one string message for future sending into messages.
    """

    list_of_stringed_events = ""
    for event in list_of_events:
        list_of_stringed_events += (event.title + "\n" +
                str(event.event_date) + "\n\n")
    return list_of_stringed_events




def get_weekly_list():
    "Returns string of events that will happen in next 7 days."
    return make_message_from_events(sql_handler.get_events_sheduled_for(7))


def get_new_events():
    """
    Gets newly added events from var in main-function and returns them as a 
    text for bots.
    """
    return make_message_from_events(sql_handler.list_of_new_events)




