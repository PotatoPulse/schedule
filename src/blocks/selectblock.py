import tkinter as tk

class SelectBlock:
    def __init__(self, parent, color: str, x: int, y: int, width: int, height: int):
        self.width = width
        self.height = height
        self.color = color
        
        dash_pattern = (4, 2)  # 4px dash, 2px gap
        line_width = 2  # Thickness of the outline

        # Top border
        self.top = tk.Canvas(parent, width=width, height=line_width, highlightthickness=0, bg=parent["bg"])
        self.top.create_line(0, 0, width, 0, fill=color, dash=dash_pattern, width=line_width)
        self.top.place(x=x, y=y)

        # Bottom border
        self.bottom = tk.Canvas(parent, width=width, height=line_width, highlightthickness=0, bg=parent["bg"])
        self.bottom.create_line(0, 0, width, 0, fill=color, dash=dash_pattern, width=line_width)
        self.bottom.place(x=x, y=y + height - line_width)

        # Left border
        self.left = tk.Canvas(parent, width=line_width, height=height, highlightthickness=0, bg=parent["bg"])
        self.left.create_line(0, 0, 0, height, fill=color, dash=dash_pattern, width=line_width)
        self.left.place(x=x, y=y)

        # Right border
        self.right = tk.Canvas(parent, width=line_width, height=height, highlightthickness=0, bg=parent["bg"])
        self.right.create_line(0, 0, 0, height, fill=color, dash=dash_pattern, width=line_width)
        self.right.place(x=x + width - line_width, y=y)
    
    def move_to(self, x, y):
        """Move the selection block to new coordinates."""
        self.top.delete("all")
        self.bottom.delete("all")
        self.left.delete("all")
        self.right.delete("all")

        dash_pattern = (4, 2)  # 4px dash, 2px gap
        line_width = 2  # Thickness of the outline

        self.top.create_line(0, 0, self.width, 0, fill=self.color, dash=dash_pattern, width=line_width)
        self.bottom.create_line(0, 0, self.width, 0, fill=self.color, dash=dash_pattern, width=line_width)
        self.left.create_line(0, 0, 0, self.height, fill=self.color, dash=dash_pattern, width=line_width)
        self.right.create_line(0, 0, 0, self.height, fill=self.color, dash=dash_pattern, width=line_width)

        self.top.place(x=x, y=y)
        self.bottom.place(x=x, y=y + self.height - 2)
        self.left.place(x=x, y=y)
        self.right.place(x=x + self.width - 2, y=y)