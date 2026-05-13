import unittest
from tetris.core.board import Board
from tetris.core.tetromino import Tetromino


class BoardTests(unittest.TestCase):
    def test_empty_board_has_no_full_rows(self):
        b = Board()
        self.assertEqual(b.clear_lines(), 0)

    def test_lock_writes_color_into_cells(self):
        b = Board()
        piece = Tetromino.spawn("O", b.cols).moved(dr=18)  # park near bottom
        b.lock(piece)
        for r, c in piece.absolute_cells():
            self.assertEqual(b.grid[r][c], piece.color)

    def test_full_single_row_clears(self):
        b = Board()
        b.grid[19] = [(1, 1, 1)] * b.cols
        self.assertEqual(b.clear_lines(), 1)
        self.assertTrue(all(cell is None for cell in b.grid[19]))

    def test_four_full_rows_clear_simultaneously(self):
        b = Board()
        for r in range(16, 20):
            b.grid[r] = [(1, 1, 1)] * b.cols
        self.assertEqual(b.clear_lines(), 4)
        for row in b.grid:
            self.assertTrue(all(cell is None for cell in row))

    def test_full_row_clear_shifts_upper_rows_down(self):
        b = Board()
        b.grid[18][0] = (2, 2, 2)  # marker block in row 18
        b.grid[19] = [(1, 1, 1)] * b.cols  # full row 19
        self.assertEqual(b.clear_lines(), 1)
        # Marker should have moved from row 18 to row 19.
        self.assertEqual(b.grid[19][0], (2, 2, 2))
        self.assertTrue(all(cell is None for cell in b.grid[18]))

    def test_is_valid_rejects_wall_collision(self):
        b = Board()
        piece = Tetromino.spawn("I", b.cols).moved(dc=-100)
        self.assertFalse(b.is_valid(piece))

    def test_is_valid_rejects_floor_collision(self):
        b = Board()
        piece = Tetromino.spawn("I", b.cols).moved(dr=100)
        self.assertFalse(b.is_valid(piece))

    def test_is_valid_rejects_stack_collision(self):
        b = Board()
        b.grid[0][4] = (1, 1, 1)
        piece = Tetromino.spawn("I", b.cols)  # spawns at row 0, cols 3-6
        self.assertFalse(b.is_valid(piece))

    def test_is_valid_allows_cells_above_top(self):
        b = Board()
        piece = Tetromino.spawn("T", b.cols).moved(dr=-1)
        self.assertTrue(b.is_valid(piece))


if __name__ == "__main__":
    unittest.main()
