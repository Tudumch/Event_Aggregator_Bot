import config

if config.use_postgreSQL: 
    import handler_postgreSQL as sql_handler
else: 
    import handler_SQLite as sql_handler

greetings_message = ("Привет\n"
"Я буду присылать тебе уведомления обо всех новых мероприятиях, которые "
"найду на клинских сайтах новостей.\n"
"А по команде '\\week' я могу показать список всех городских мероприятий, "
"которые пройдут в ближайшие 7 дней.")


def get_weekly_list():
    list_of_events = sql_handler.get_events_sheduled_for(180)
    list_of_stringed_events = ""
    for event in list_of_events:
        list_of_stringed_events += (event.title.rstrip() + "\n" +
                str(event.event_date) + "\n\n")

    return list_of_stringed_events



