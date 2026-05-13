"""10x20 play field: collision checks, locking, line clears."""
from __future__ import annotations
from tetris import config
from tetris.core.tetromino import Tetromino


class Board:
    def __init__(self, cols: int = config.BOARD_COLS, rows: int = config.BOARD_ROWS):
        self.cols = cols
        self.rows = rows
        # None = empty cell; otherwise stores the locked piece's color tuple.
        self.grid: list[list] = [[None] * cols for _ in range(rows)]

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_valid(self, piece: Tetromino) -> bool:
        """True if the piece fits: not through walls/floor, not overlapping locked cells.
        Cells above row 0 are allowed (piece may briefly extend above the visible board)."""
        for r, c in piece.absolute_cells():
            if c < 0 or c >= self.cols or r >= self.rows:
                return False
            if r >= 0 and self.grid[r][c] is not None:
                return False
        return True

    def lock(self, piece: Tetromino) -> None:
        for r, c in piece.absolute_cells():
            if self.in_bounds(r, c):
                self.grid[r][c] = piece.color

    def clear_lines(self) -> int:
        """Remove fully-filled rows; shift remaining rows down. Returns rows cleared."""
        kept = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.rows - len(kept)
        if cleared:
            empty = [[None] * self.cols for _ in range(cleared)]
            self.grid = empty + kept
        return cleared
