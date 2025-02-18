import tkinter as tk
from schedule import Schedule
from render import render_schedule
from time_indicator import update_time_indicator
from event import Event
from datetime import datetime, timedelta

colors = {
    "root_bg": "SystemButtonFace",
    "none_block": "lightblue",
    "time_line": "red",
    "day_bg": "#FF7074",
    "day_header_bg": "gray",
}

# Initialize application window
root = tk.Tk()
root.geometry("900x600")

sched = Schedule(12, 7, 8)
today = datetime.today()
start_day = today - timedelta(days=today.weekday())
block_width = 150

# Create container for the schedule grid
grid_container = tk.Frame(root)
grid_container.place(relx=0.5, rely=0.5, anchor="center")

def handle_event_altered(event: Event, action: str):
    if action == "put":
        sched.put_event(event)
        print(f"Event added: {event.title} at {event.location} on {event.datetime}")
    elif action == "delete":
        sched.delete_event(event)
        print(f"Event deleted: {event.title} at {event.location} on {event.datetime}")
    render_schedule(grid_container, sched, block_width, start_day, days_labels, hours_labels, handle_event_altered, colors)
    

days_labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
hours_labels = [f"{h}:00" for h in range(sched.start_hour, sched.end_hour)]

render_schedule(grid_container, sched, block_width, start_day, days_labels, hours_labels, handle_event_altered, colors)

root.mainloop()
