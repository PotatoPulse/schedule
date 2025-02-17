import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Toplevel, Label, Entry, Button, colorchooser
from event import Event
from schedule import Schedule
from blocks.baseblock import BaseBlock

class EventBlock(BaseBlock):
    def __init__(self, parent, colors: dict, event, block_width: int, start_hour: int, x: int, y: int):
        """Creates an event block positioned exactly based on quarter blocks."""
        print(f"Creating EventBlock for {event.title} at ({x}, {y})")

        super().__init__(parent, width=block_width, height=1, bg=event.color, highlightthickness=1, bd=1, relief="solid", event=event, colors=colors)

        self.num_blocks = max(1, event.duration // 15)
        event_height = self.num_blocks * 16  

        self.display_event_info()

        self.place(x=x, y=y, width=block_width, height=event_height)

    def display_event_info(self):
        """Displays event title, location, and note inside the block."""
        parent_bg = self.cget("bg")  
        text_frame = tk.Frame(self, bg=parent_bg)
        text_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        event_title = tk.Label(text_frame, text=self.event.title, bg=parent_bg, fg="white", font=("Arial", 9, "bold"))
        event_title.pack(anchor="n", pady=(2, 0))

        if self.event.location:
            event_location = tk.Label(text_frame, text="At: " + self.event.location, bg=parent_bg, fg="white", font=("Arial", 7))
            event_location.pack(anchor="w", padx=5, pady=(2, 0))

        if self.event.note:
            event_note = tk.Label(text_frame, text=self.event.note, bg=parent_bg, fg="white", font=("Arial", 7, "italic"))
            event_note.pack(anchor="w", padx=5, pady=(2, 0))