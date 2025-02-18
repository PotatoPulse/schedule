from datetime import datetime, timedelta

class Event():
    def __init__(self, datetime_obj: datetime, duration: int, title: str, location: str, note: str, color: str):
        self.datetime = datetime_obj  # Use built-in datetime
        self.duration = duration #event duration in minutes
        self.title = title
        self.location = location
        self.note = note
        self.color = color

    def get_tuple(self):
        return (self.datetime.year, self.datetime.month, self.datetime.day, self.datetime.hour)