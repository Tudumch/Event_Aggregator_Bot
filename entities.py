import datetime

class Event:

    def __init__(self, event_id: int, title: str, event_date: datetime.date, 
            date_added: datetime.date):
        self.__event_id = event_id
        self.__title = title
        self.__event_date = event_date # when event happen
        self.__date_added = date_added # when event added to DB

    @property
    def event_id(self):
        return self.__event_id
    @event_id.setter
    def event_id(self, event_id: int):
        if type(event_id) != int:
            raise ValueError(".event_id type must be int!")
        self.__event_id = event_id

    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, title: str):
        if type(title) != str:
            raise ValueError(".title type must be str!")
        self.__title = title

    @property
    def event_date(self):
        return self.__event_date
    @event_date.setter
    def event_date(self, date: datetime.date):
        if type(date) != datetime.date:
            raise ValueError(".event_date type must be datetime.date!")
        self.__event_date = date

    @property
    def date_added(self):
        return self.__date_added
    @date_added.setter
    def date_added(self, date: datetime.date):
        if type(date) != datetime.date:
            raise ValueError(".event_date type must be datetime.date!")
        self.__date_added = date


if __name__ == "__main__":
    event = Event(32, "Test Event", datetime.date.today(),
            datetime.date.today())
    event.event_date = datetime.date(2021, 11, 1)
    # event.event_date = "2300, 12, 1"
    print(type(event.event_date))

