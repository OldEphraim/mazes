class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False  # Track if this cell has been visited
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        if self.has_left_wall:
            self._win._canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="black", width=2)
        else:
            self._win._canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="#d9d9d9", width=2)

        if self.has_top_wall:
            self._win._canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="black", width=2)
        else:
            self._win._canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="#d9d9d9", width=2)

        if self.has_right_wall:
            self._win._canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="black", width=2)
        else:
            self._win._canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="#d9d9d9", width=2)

        if self.has_bottom_wall:
            self._win._canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="black", width=2)
        else:
            self._win._canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="#d9d9d9", width=2)

    def draw_move(self, to_cell, undo=False):
        # Determine the fill color based on the undo flag
        color = "red" if not undo else "gray"
    
        # Calculate the center points of the current cell and the destination cell
        x1 = (self._x1 + self._x2) // 2
        y1 = (self._y1 + self._y2) // 2
        x2 = (to_cell._x1 + to_cell._x2) // 2
        y2 = (to_cell._y1 + to_cell._y2) // 2
    
        # Draw the line from the center of the current cell to the center of the destination cell
        self._win._canvas.create_line(x1, y1, x2, y2, fill=color, width=2)