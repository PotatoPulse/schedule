import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Toplevel, Label, Entry, Button, colorchooser
from event import Event
from schedule import Schedule
from blocks.baseblock import BaseBlock
from blocks.selectblock import SelectBlock
from blocks.gridblock import GridBlock

class EventBlock(BaseBlock):
    def __init__(self, parent, colors: dict, event: Event, block_width: int, start_hour: int, x: int, y: int, on_event_altered=None):
        """Creates an event block positioned exactly based on quarter blocks."""
        print(f"Creating EventBlock for {event.title} at ({x}, {y})")

        super().__init__(parent, width=block_width, height=1, bg=event.color, highlightthickness=0, bd=1, relief="solid", event=event, colors=colors, on_event_altered=on_event_altered)
        self.parent = parent
        self.x=x
        self.y=y
        self.width = block_width
        self.select_box = None
        self.block_width = block_width
        self.grid_positions = [
            (widget, widget.winfo_x(), widget.winfo_y(), widget.winfo_width(), widget.winfo_height())
            for widget in self.parent.winfo_children() if isinstance(widget, GridBlock)
        ]
        self.nearest_gridblock = None

        # calculate the amount of full hours passed, because we need to match padding
        num_pads = (event.datetime.minute + event.duration - 1) // 60
        
        self.num_blocks = max(1, event.duration // 15)
        event_height = self.num_blocks * 16
        self.height = event_height+num_pads*4

        self.display_event_info()

        self.place(x=x, y=y, width=self.width, height=self.height)
        self.bind("<Double-Button-1>", self.open_add_event_window)
        self.bind("<Button-3>", self.edit_event)
        self.bind("<B1-Motion>", self.move)
        self.parent.bind_all("<ButtonRelease-1>", self.stop_move)
    
    def move(self, event):
        if not self.select_box:
            self.select_box = SelectBlock(self.parent, color=self.event.color, x=self.x, y=self.y, width=self.width, height=self.height)

        mouse_x = self.winfo_x() + event.x
        mouse_y = self.winfo_y() + event.y

        # make selection snap to gridblocks
        nearest_x, nearest_y = self.find_nearest_grid(mouse_x, mouse_y)

        if not (nearest_x, nearest_y) == (self.select_box.x, self.select_box.y):
            self.select_box.move_to(nearest_x, nearest_y)
    
    def find_nearest_grid(self, x, y):
        closest_x, closest_y = None, None
        nearest_gridblock = None
        min_distance = float("inf")

        for widget, grid_x, grid_y, grid_width, grid_height in self.grid_positions:
            center_x = grid_x + (grid_width // 2)
            center_y = grid_y + grid_height  # Center bottom edge

            distance = abs(center_x - x) + abs(center_y - y)
            if distance < min_distance:
                min_distance = distance
                closest_x, closest_y = grid_x, grid_y
                self.nearest_gridblock = widget

        return closest_x, closest_y

    def stop_move(self, event):
        if self.select_box:
            self.select_box.destroy()
            self.select_box = None

        if self.nearest_gridblock:
            grid = self.nearest_gridblock

            # Calculate correct datetime for new event
            new_date = self.start_day + timedelta(days=grid.col - 1)  # Adjust for the day
            new_time = grid.start_hour + ((grid.row - 2) // 4)  # Convert row to hour
            new_minutes = ((grid.row - 2) % 4) * 15  # Convert quarter rows to minutes
            
            new_datetime = new_date.replace(hour=new_time, minute=new_minutes, second=0, microsecond=0)

            # Create new event at the correct position
            new_event = Event(new_datetime, self.event.duration, self.event.title, self.event.location, self.event.note, self.event.color)

            # Update schedule: delete old event and put new event
            if self.on_event_altered:
                self.on_event_altered(self.event, action="delete")
                self.on_event_altered(new_event, action="put")

            # Destroy the current EventBlock
            self.destroy()


    def delete_event(self):
        if self.on_event_altered:
            self.on_event_altered(self.event, action="delete")
        self.event = None
        self.destroy()

    def edit_event(self, event):
        edit_options = tk.Menu(self, tearoff=0)

        edit_options.add_command(label="Edit event", command=lambda: self.open_add_event_window(None))
        edit_options.add_command(label="Delete event", command=lambda: self.delete_event())

        edit_options.post(event.x_root, event.y_root)

    def display_event_info(self):
        """Displays event title, location, and note inside the block."""
        parent_bg = self.cget("bg")  
        text_frame = tk.Frame(self, bg=parent_bg)
        text_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        text_frame.bind("<Double-Button-1>", self.open_add_event_window)
        text_frame.bind("<Button-3>", self.edit_event)
        text_frame.bind("<B1-Motion>", self.move)
        
        event_title = tk.Label(text_frame, text=self.event.title, bg=parent_bg, fg="white", font=("Arial", 9, "bold"))
        event_title.pack(anchor="n", pady=(2, 0))
        event_title.bind("<Double-Button-1>", self.open_add_event_window)
        event_title.bind("<Button-3>", self.edit_event)
        event_title.bind("<B1-Motion>", self.move)

        if self.event.location:
            event_location = tk.Label(text_frame, text="At: " + self.event.location, bg=parent_bg, fg="white", font=("Arial", 7))
            event_location.pack(anchor="w", padx=5, pady=(2, 0))
            event_location.bind("<Double-Button-1>", self.open_add_event_window)
            event_location.bind("<Button-3>", self.edit_event)
            event_location.bind("<B1-Motion>", self.move)

        if self.event.note:
            event_note = tk.Label(text_frame, text=self.event.note, bg=parent_bg, fg="white", font=("Arial", 7, "italic"))
            event_note.pack(anchor="w", padx=5, pady=(2, 0))
            event_note.bind("<Double-Button-1>", self.open_add_event_window)
            event_note.bind("<Button-3>", self.edit_event)
            event_note.bind("<B1-Motion>", self.move)