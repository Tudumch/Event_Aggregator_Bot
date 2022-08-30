import datetime

class Event:

    def __init__(self, event_id: int, title: str, event_date: datetime.date, 
            date_added: datetime.date):
        self.event_id = event_id
        self.title = title
        self.event_date = event_date # when event happen
        self.date_added = date_added # when event added to DB

    def get_event_id(self):
        return self.event_id
    def get_title(self):
        return self.title
    def get_event_date(self):
        return self.event_date
    def get_date_added(self):
        return self.date_added
    
    def set_event_id(self, event_id: int):
        self.event_id = event_id
    def set_title(self, title: str):
        self.title = title
    def set_event_date(self, date: datetime.date):
        self.event_date = date
    def set_date_added(self, date: datetime.date):
        self.date_added = date
