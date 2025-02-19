import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Toplevel, Label, Entry, Button, colorchooser
from event import Event
from schedule import Schedule
from blocks.baseblock import BaseBlock

class EventBlock(BaseBlock):
    def __init__(self, parent, colors: dict, event: Event, block_width: int, start_hour: int, x: int, y: int, on_event_altered=None):
        """Creates an event block positioned exactly based on quarter blocks."""
        print(f"Creating EventBlock for {event.title} at ({x}, {y})")

        super().__init__(parent, width=block_width, height=1, bg=event.color, highlightthickness=0, bd=1, relief="solid", event=event, colors=colors, on_event_altered=on_event_altered)

        # calculate the amount of full hours passed, because we need to match padding
        num_pads = (event.datetime.minute + event.duration - 1) // 60
        
        self.num_blocks = max(1, event.duration // 15)
        event_height = self.num_blocks * 16

        self.display_event_info()

        self.place(x=x, y=y, width=block_width, height=event_height+num_pads*4)
        self.bind("<Double-Button-1>", self.open_add_event_window)
        self.bind("<Button-3>", self.edit_event)

    def display_event_info(self):
        """Displays event title, location, and note inside the block."""
        parent_bg = self.cget("bg")  
        text_frame = tk.Frame(self, bg=parent_bg)
        text_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        text_frame.bind("<Double-Button-1>", self.open_add_event_window)
        text_frame.bind("<Button-3>", self.edit_event)
        
        event_title = tk.Label(text_frame, text=self.event.title, bg=parent_bg, fg="white", font=("Arial", 9, "bold"))
        event_title.pack(anchor="n", pady=(2, 0))
        event_title.bind("<Double-Button-1>", self.open_add_event_window)
        event_title.bind("<Button-3>", self.edit_event)

        if self.event.location:
            event_location = tk.Label(text_frame, text="At: " + self.event.location, bg=parent_bg, fg="white", font=("Arial", 7))
            event_location.pack(anchor="w", padx=5, pady=(2, 0))
            event_title.bind("<Double-Button-1>", self.open_add_event_window)
            event_title.bind("<Button-3>", self.edit_event)

        if self.event.note:
            event_note = tk.Label(text_frame, text=self.event.note, bg=parent_bg, fg="white", font=("Arial", 7, "italic"))
            event_note.pack(anchor="w", padx=5, pady=(2, 0))
            event_title.bind("<Double-Button-1>", self.open_add_event_window)
            event_title.bind("<Button-3>", self.edit_event)
    
    def delete_event(self):
        if self.on_event_altered:
            self.on_event_altered(self.event, action="delete")
        self.event = None

    def edit_event(self, event):
        edit_options = tk.Menu(self, tearoff=0)

        edit_options.add_command(label="Edit event", command=lambda: self.open_add_event_window(None))
        edit_options.add_command(label="Delete event", command=lambda: self.delete_event())

        edit_options.post(event.x_root, event.y_root)