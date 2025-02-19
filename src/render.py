import tkinter as tk
from blocks.gridblock import GridBlock
from blocks.eventblock import EventBlock
from schedule import Schedule
from time_indicator import update_time_indicator, update_day_indicator
from datetime import datetime, timedelta

def render_schedule(
    grid_container: tk.Frame, 
    sched: Schedule,
    block_width: int,
    start_day: datetime, 
    days_labels: list, 
    hours_labels: list, 
    handle_event_altered,
    colors: dict,
):
    """Rebuilds the schedule UI based on current events."""
    
    # Recreate headers
    tk.Label(grid_container, text="", width=8, height=2).grid(row=0, column=0, padx=2, pady=2)

    # Current day backdrop
    day_canvas = tk.Canvas(grid_container, width=1, height=1000, bg=colors["day_bg"], highlightthickness=0)
    update_day_indicator(day_canvas, sched, block_width)

    # Day headers
    for c, day in enumerate(days_labels, start=1):
        current_date = start_day + timedelta(days=c-1)
        date_str = current_date.strftime("%d-%m-%Y")
        tk.Label(grid_container, text=date_str, bg=colors["root_bg"], fg="black", width=int(block_width/8.4), height=2, font=("Arial", 10, "bold"), anchor="s").grid(row=0, column=c, padx=2)
        tk.Label(grid_container, text=day, bg=colors["day_header_bg"], fg="white", width=int(block_width/8.4), height=2, font=("Arial", 10, "bold")).grid(row=1, column=c, padx=2, pady=2)

    start_row = 2  # Row where time labels start

    # Hours (show only full-hour labels, but keep 15-min rows)
    for r in range(start_row, sched.hours * 4 + start_row):
          if (r - start_row) % 4 == 0:  # Show label only for full hours
            hour_index = (r - start_row) // 4
            hour_text = hours_labels[hour_index]  # Use only full hours
            canvas = tk.Canvas(grid_container, width=50, height=14, bg=colors["root_bg"], highlightthickness=0)
            canvas.create_text(25, 7, text=hour_text, font=("Arial", 9, "bold"), fill="black", anchor="center")
            canvas.grid(row=r, column=0, padx=2, sticky="n")
            tk.Frame(grid_container, height=2, width=80, bg="black").grid(row=r, column=0, sticky="n", padx=2)

    for r in range(start_row, sched.quarters + start_row):
        for c in range(1, len(days_labels) + 1):
            block_padding = (4, 0) if (r - start_row) % 4 == 0 else (0, 0) # block padding for each hour
            block = GridBlock(grid_container, colors, width=block_width, height=16, color=colors["none_block"], row=r, col=c, 
                  on_event_altered=handle_event_altered, start_day=start_day, start_hour=sched.start_hour).grid(padx=2, pady=block_padding)

    weekly_events = sched.get_weekly_events(start_day)
    
    for event in weekly_events:
        col = (event.datetime.date() - start_day.date()).days + 1  # +1 to match grid column index
        row = ((event.datetime.hour - sched.start_hour) * 4) + (event.datetime.minute // 15) + start_row  # Match quarter-hour grid

        blocks_at_pos = grid_container.grid_slaves(row=row, column=col)  # Returns a list of widgets
        print("blocks at pos: ", blocks_at_pos)

        if blocks_at_pos:
            block = blocks_at_pos[1]  # Get the first block (should be only one per cell)
            x, y = block.winfo_x(), block.winfo_y()  # Fetch real-time widget position
            EventBlock(grid_container, colors, event, block_width, sched.start_hour, x=x, y=y, on_event_altered=handle_event_altered)
        else:
            print(f"Warning: No block found at row {row}, col {col} for event {event.title}")

    # Current time line
    time_canvas = tk.Canvas(grid_container, width=900, height=3, bg=colors["time_line"], highlightthickness=0)
    update_time_indicator(time_canvas, sched)
