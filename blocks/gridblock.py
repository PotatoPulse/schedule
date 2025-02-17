import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Toplevel, Label, Entry, Button, colorchooser
from event import Event
from schedule import Schedule
from blocks.baseblock import BaseBlock


class GridBlock(BaseBlock):
    def __init__(self, parent, colors: dict, width=100, height=16, color="blue", row=0, col=0, event=None, on_event_altered=None, start_day=None, start_hour=8):
        super().__init__(parent, width=width, height=height, bg=color, borderwidth=1, event=event, colors=colors)
        self.grid(row=row, column=col, padx=2, pady=(0, 0))
        self.row = row
        self.col = col
        self.start_day = start_day or datetime.today()
        self.start_hour = start_hour  
        self.on_event_altered = on_event_altered  
        
        self.bind("<Double-Button-1>", self.open_add_event_window)