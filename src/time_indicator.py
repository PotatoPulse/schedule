import tkinter as tk
from datetime import datetime
from schedule import Schedule

def update_time_indicator(time_canvas: tk.Canvas, sched: Schedule):
    """Moves the red line using fixed Y-coordinates for first and last row."""
    
    if not time_canvas.winfo_exists():
        print("WARNING: time_canvas does not exist yet. Skipping update.")
        return

    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute

    start_hour = sched.start_hour
    end_hour = sched.end_hour

    first_y = 82 #42
    last_y = 898

    if current_hour < start_hour:
        current_hour = start_hour
        current_minute = 0
    elif current_hour >= end_hour:
        current_hour = end_hour - 1
        current_minute = 59

    total_minutes = (current_hour * 60) + current_minute
    total_grid_height = last_y - first_y
    total_schedule_minutes = (end_hour - start_hour) * 60
    relative_position = (total_minutes - (start_hour * 60)) / total_schedule_minutes
    line_y_position = first_y + (relative_position * total_grid_height)

    time_canvas.place(relx=0, y=line_y_position, relwidth=1)

def update_day_indicator(day_canvas: tk.Canvas, sched: Schedule, block_width: int):
    """Places red background behind current day"""
    now = datetime.now()
    day = now.weekday()

    day_canvas.place(relx=0.072 + (day*1/7.54), rely=0.043, relwidth=1/7.55)