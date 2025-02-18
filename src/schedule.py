from datetime import datetime, timedelta
from event import Event

class Schedule():
    def __init__(self, hours, days, start_hour):
        self.start_hour = start_hour
        self.end_hour = start_hour + hours
        self.hours = hours
        self.quarters = hours * 4
        self.days = days
        self.all_events = {}

    def put_event(self, event: Event):
        self.all_events[event.datetime] = event  # Use the actual datetime object

    def delete_event(self, event: Event):
        if event.datetime in self.all_events:
            del self.all_events[event.datetime]

    def get_weekly_events(self, start_day: datetime):
        end_day = start_day + timedelta(days=7)

        return [
            event
            for dt, event in self.all_events.items()
            if start_day.date() <= dt.date() < end_day.date()  # Compare only dates
        ]