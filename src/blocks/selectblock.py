import tkinter as tk

class SelectBlock:
    def __init__(self, parent, color: str, x: int, y: int, width: int, height: int):
        self.parent = parent
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        
        self.top = None
        self.bottom = None
        self.right = None
        self.left = None

        self.move_to(x, y)
    
    def move_to(self, x, y):
        """Move the selection block to new coordinates."""
        self.destroy()  # Destroy old canvases

        dash_pattern = (4, 2)  # 4px dash, 2px gap
        line_width = 3  # Border thickness

        # Recreate the canvases
        self.top = tk.Canvas(self.parent, width=self.width, height=line_width, highlightthickness=0, bg="SystemButtonFace")
        self.bottom = tk.Canvas(self.parent, width=self.width, height=line_width, highlightthickness=0, bg="SystemButtonFace")
        self.left = tk.Canvas(self.parent, width=line_width, height=self.height, highlightthickness=0, bg="SystemButtonFace")
        self.right = tk.Canvas(self.parent, width=line_width, height=self.height, highlightthickness=0, bg="SystemButtonFace")

        # Redraw dashed lines
        self.top.create_line(0, 0, self.width, 0, fill=self.color, dash=dash_pattern, width=line_width)
        self.bottom.create_line(0, 0, self.width, 0, fill=self.color, dash=dash_pattern, width=line_width)
        self.left.create_line(0, 0, 0, self.height, fill=self.color, dash=dash_pattern, width=line_width)
        self.right.create_line(0, 0, 0, self.height, fill=self.color, dash=dash_pattern, width=line_width)

        # Place the canvases at new coordinates
        self.top.place(x=x, y=y)
        self.bottom.place(x=x, y=y + self.height - 2)
        self.left.place(x=x, y=y)
        self.right.place(x=x + self.width - 2, y=y)
        
    def destroy(self):
        """Completely remove all canvases from the UI."""
        if self.top:
            self.top.destroy()
        if self.bottom:
            self.bottom.destroy()
        if self.left:
            self.left.destroy()
        if self.right:
            self.right.destroy()

        self.top = self.bottom = self.left = self.right = None
