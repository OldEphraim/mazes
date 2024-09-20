import unittest
from maze import Maze
from window import Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)

        # Check that the number of rows is correct
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        
        # Check that the number of columns in the first row is correct
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )
    
    def setUp(self):
        self.win = Window(800, 600)
        self.maze = Maze(0, 0, 10, 12, 10, 10, self.win)

    def test_reset_cells_visited(self):
        # Set some cells as visited for testing
        self.maze._cells[0][0].visited = True
        self.maze._cells[1][1].visited = True

        # Call the reset method
        self.maze._reset_cells_visited()

        # Check that all cells are now unvisited
        for row in self.maze._cells:
            for cell in row:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()