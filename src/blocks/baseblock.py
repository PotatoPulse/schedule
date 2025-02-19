import tkinter as tk
from datetime import datetime, timedelta
from tkinter import Toplevel, Label, Entry, Button, colorchooser
from event import Event
from schedule import Schedule


class BaseBlock(tk.Frame):
    """Parent class for Block and EventBlock to share common methods like event editing."""
    
    def __init__(self, parent, width=100, height=16, bg="blue", borderwidth=1, event=None, colors=None, on_event_altered=None, start_day=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, borderwidth=borderwidth, **kwargs)
        self.event = event
        self.colors = colors or {}
        self.start_day = start_day if start_day else datetime.today() - timedelta(days=datetime.today().weekday())
        self.on_event_altered = on_event_altered

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def open_add_event_window(self, event=None):
        """Opens a popup to add/edit an event when a block is double-clicked."""
        self.config(highlightthickness=2)
        self.unbind("<Enter>")
        self.unbind("<Leave>")

        popup = Toplevel(self)
        popup.title("Edit Event" if self.event else "Add Event")
        popup.geometry("+{}+{}".format(self.winfo_rootx() + 120, self.winfo_rooty()))  # Position near block

        def on_popup_close():
            self.bind("<Enter>", self.on_hover)
            self.bind("<Leave>", self.on_leave)
            self.config(highlightthickness=0)
            popup.destroy()

        popup.protocol("WM_DELETE_WINDOW", on_popup_close)

        event_title = self.event.title if self.event else ""
        event_location = self.event.location if self.event else ""
        event_note = self.event.note if self.event else ""
        event_color = self.event.color if self.event else self.colors.get("none_block", "gray")
        event_duration = self.event.duration if self.event else 60

        row = 1
        Label(popup, text="Title:").grid(row=row, column=0, padx=5, pady=5)
        title_entry = Entry(popup)
        title_entry.insert(0, event_title)
        title_entry.grid(row=row, column=1, padx=5, pady=5)

        row += 1
        Label(popup, text="Duration:").grid(row=row, column=0, padx=5, pady=5)
        hour_entry = Entry(popup)
        hour_entry.insert(0, int(event_duration / 60))
        hour_entry.grid(row=row, column=1, padx=5, pady=5)
        minute_entry = Entry(popup)
        minute_entry.insert(0, event_duration % 60)
        minute_entry.grid(row=row, column=2, padx=5, pady=5)

        row += 1
        Label(popup, text="Location:").grid(row=row, column=0, padx=5, pady=5)
        location_entry = Entry(popup)
        location_entry.insert(0, event_location)
        location_entry.grid(row=row, column=1, padx=5, pady=5)

        row += 1
        Label(popup, text="Note:").grid(row=row, column=0, padx=5, pady=5)
        note_entry = Entry(popup)
        note_entry.insert(0, event_note)
        note_entry.grid(row=row, column=1, padx=5, pady=5)

        # Color Selection
        selected_color = [event_color]  

        def choose_color():
            try:
                root_window = self.winfo_toplevel()
                color = colorchooser.askcolor(title="Choose Event Color", parent=root_window)
                if color[1]:  
                    selected_color[0] = color[1]
                    color_button.config(bg=color[1])  
                    popup.lift()  
            except Exception as e:
                print(f"Error choosing color: {e}")  

        row += 1
        Label(popup, text="Color:").grid(row=row, column=0, padx=5, pady=5)
        color_button = Button(popup, text="Pick Color", command=choose_color, bg=event_color)
        color_button.grid(row=row, column=1, padx=5, pady=5)

        warning_label = Label(popup, text="", fg="red", font=("Arial", 10))
        warning_label.grid(row=0, column=1, columnspan=2)

        def save_event():
            title = title_entry.get().strip()
            hour_duration = hour_entry.get().strip()
            minute_duration = minute_entry.get().strip()
            location = location_entry.get().strip()
            note = note_entry.get().strip()
            color = selected_color[0]  # Event color

            if not title:
                warning_label.config(text="Title is required!", fg="red")  
                return

            if self.event:
                event_datetime = self.event.datetime
            else:
                event_datetime = self.start_day + timedelta(days=self.col - 1)  # Adjust date correctly
                event_datetime = event_datetime.replace(
                    hour=self.start_hour + int((self.row - 2) / 4),
                    minute=((self.row-2)%4)*15,
                    second=0,
                    microsecond=0
                )

            try:
                duration = int(hour_duration) * 60 + int(minute_duration)
            except ValueError:
                duration = 60

            new_event = Event(event_datetime, duration, title, location, note, color)

            popup.destroy()

            if hasattr(self, "on_event_altered") and self.on_event_altered:
                self.on_event_altered(new_event, action="put")
            
            self.config(highlightthickness=0)
        row += 1
        save_button = Button(popup, text="Save", command=save_event)
        save_button.grid(row=row, column=0, columnspan=2, pady=10)

    def on_hover(self, event):
        self.config(highlightbackground="black", highlightthickness=1)
    
    def on_leave(self, event):
        self.config(highlightthickness=0)
