from tkinter import Tk, BOTH, Canvas
import cell
import maze

class Window:
    def __init__(self, width, height):
        # Create the root widget
        self.__root = Tk()
        self.__root.title("Tkinter Window")

        # Create a canvas widget
        self._canvas = Canvas(self.__root, width=width, height=height)
        self._canvas.pack(fill=BOTH, expand=True)

        # Set running state to False initially
        self.__running = False

        # Handle the window close event
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    # Method to redraw the window
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    # Wait for the window to close
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    # Close the window
    def close(self):
        self.__running = False

    # Draw line
    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

# Main function
def main():
    win = Window(800, 600)
    num_cols = 12
    num_rows = 10
    maze_implementation = maze.Maze(0, 0, num_rows, num_cols, 10, 10, win)
    maze_implementation.solve()  # Call the solve method to animate the solution

if __name__ == "__main__":
    main()