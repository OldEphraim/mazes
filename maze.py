import time
import random
import cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)

        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)  # Start breaking walls from the top-left cell

    def _create_cells(self):
        self._cells = [[cell.Cell(self._x1 + j * self._cell_size_x, self._y1 + i * self._cell_size_y, 
                             self._x1 + (j + 1) * self._cell_size_x, 
                             self._y1 + (i + 1) * self._cell_size_y, self._win) 
                        for j in range(self._num_cols)] for i in range(self._num_rows)]
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True  # Mark the current cell as visited
        directions = []  # To hold possible directions

        # Check adjacent cells (up, down, left, right)
        if i > 0 and not self._cells[i - 1][j].visited:  # Up
            directions.append((i - 1, j))
        if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:  # Down
            directions.append((i + 1, j))
        if j > 0 and not self._cells[i][j - 1].visited:  # Left
            directions.append((i, j - 1))
        if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:  # Right
            directions.append((i, j + 1))

        # If there are no directions, draw the cell and return
        if not directions:
            self._draw_cell(i, j)
            return

        # Pick a random direction and break the wall
        next_cell = random.choice(directions)
        ni, nj = next_cell

        # Break the wall between current cell and next cell
        if ni < i:  # Moving up
            self._cells[i][j].has_top_wall = False
            self._cells[ni][nj].has_bottom_wall = False
        elif ni > i:  # Moving down
            self._cells[i][j].has_bottom_wall = False
            self._cells[ni][nj].has_top_wall = False
        elif nj < j:  # Moving left
            self._cells[i][j].has_left_wall = False
            self._cells[ni][nj].has_right_wall = False
        elif nj > j:  # Moving right
            self._cells[i][j].has_right_wall = False
            self._cells[ni][nj].has_left_wall = False

        # Recursively call for the next cell
        self._break_walls_r(ni, nj)

        self._reset_cells_visited()  # Reset visited status after breaking walls

    def _draw_cell(self, i, j):
        # Calculate the x/y position based on the cell size and coordinates
        x1 = j * self._cell_size_x + self._x1
        y1 = i * self._cell_size_y + self._y1
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y

        # Draw the left wall if it exists
        if self._cells[i][j].has_left_wall:
            self._win._canvas.create_line(x1, y1, x1, y2, fill="black", width=2)
        else:
            # Draw a line with the background color to "erase" the wall
            self._win._canvas.create_line(x1, y1, x1, y2, fill="#d9d9d9", width=2)

        # Draw the top wall if it exists
        if self._cells[i][j].has_top_wall:
            self._win._canvas.create_line(x1, y1, x2, y1, fill="black", width=2)
        else:
            self._win._canvas.create_line(x1, y1, x2, y1, fill="#d9d9d9", width=2)

        # Draw the right wall if it exists
        if self._cells[i][j].has_right_wall:
            self._win._canvas.create_line(x2, y1, x2, y2, fill="black", width=2)
        else:
            self._win._canvas.create_line(x2, y1, x2, y2, fill="#d9d9d9", width=2)

        # Draw the bottom wall if it exists
        if self._cells[i][j].has_bottom_wall:
            self._win._canvas.create_line(x1, y2, x2, y2, fill="black", width=2)
        else:
            self._win._canvas.create_line(x1, y2, x2, y2, fill="#d9d9d9", width=2)


    def _animate(self):
        # Redraw the window and sleep for a short time
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Entrance at (0, 0): keep the top wall
        self._cells[0][0].has_top_wall = True
        self._draw_cell(0, 0)  # Redraw to update

        # Exit at (num_rows-1, num_cols-1)
        self._cells[self._num_rows - 1][self._num_cols - 1].has_bottom_wall = False  # Remove bottom wall
        self._draw_cell(self._num_rows - 1, self._num_cols - 1)  # Update the drawing
    
    def _draw_move(self, i, j, ni, nj):
            # Draw the path from current cell to the next cell
            x1 = j * self._cell_size_x + self._x1 + self._cell_size_x / 2
            y1 = i * self._cell_size_y + self._y1 + self._cell_size_y / 2
            x2 = nj * self._cell_size_x + self._x1 + self._cell_size_x / 2
            y2 = ni * self._cell_size_y + self._y1 + self._cell_size_y / 2
            self._win._canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    def _undo_move(self, i, j, ni, nj):
        # Draw a line in the background color to "erase" the path
        x1 = j * self._cell_size_x + self._x1 + self._cell_size_x / 2
        y1 = i * self._cell_size_y + self._y1 + self._cell_size_y / 2
        x2 = nj * self._cell_size_x + self._x1 + self._cell_size_x / 2
        y2 = ni * self._cell_size_y + self._y1 + self._cell_size_y / 2
        self._win._canvas.create_line(x1, y1, x2, y2, fill="#d9d9d9", width=2)  # Background color

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()  # Animate the current state
        self._cells[i][j].visited = True  # Mark the current cell as visited

        # Check if we've reached the exit cell
        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True  # Reached the end

        # Check each direction (up, down, left, right)
        directions = [
            (i - 1, j),  # Up
            (i + 1, j),  # Down
            (i, j - 1),  # Left
            (i, j + 1)   # Right
        ]

        for ni, nj in directions:
            if 0 <= ni < self._num_rows and 0 <= nj < self._num_cols:  # Within bounds
                # Check for walls and if the cell hasn't been visited
                if not self._cells[i][j].has_top_wall and ni < i and not self._cells[ni][nj].visited:  # Up
                    self._draw_move(i, j, ni, nj)
                    if self._solve_r(ni, nj):
                        return True
                    self._undo_move(i, j, ni, nj)

                elif not self._cells[i][j].has_bottom_wall and ni > i and not self._cells[ni][nj].visited:  # Down
                    self._draw_move(i, j, ni, nj)
                    if self._solve_r(ni, nj):
                        return True
                    self._undo_move(i, j, ni, nj)

                elif not self._cells[i][j].has_left_wall and nj < j and not self._cells[ni][nj].visited:  # Left
                    self._draw_move(i, j, ni, nj)
                    if self._solve_r(ni, nj):
                        return True
                    self._undo_move(i, j, ni, nj)

                elif not self._cells[i][j].has_right_wall and nj > j and not self._cells[ni][nj].visited:  # Right
                    self._draw_move(i, j, ni, nj)
                    if self._solve_r(ni, nj):
                        return True
                    self._undo_move(i, j, ni, nj)

        return False  # No valid moves found
