"""The 7 standard tetrominoes, with rotation and movement."""
from __future__ import annotations
from dataclasses import dataclass


SHAPE_CELLS = {
    "I": ((0, 0), (0, 1), (0, 2), (0, 3)),
    "O": ((0, 0), (0, 1), (1, 0), (1, 1)),
    "T": ((0, 0), (0, 1), (0, 2), (1, 1)),
    "S": ((0, 1), (0, 2), (1, 0), (1, 1)),
    "Z": ((0, 0), (0, 1), (1, 1), (1, 2)),
    "J": ((0, 0), (1, 0), (1, 1), (1, 2)),
    "L": ((0, 2), (1, 0), (1, 1), (1, 2)),
}

SHAPE_COLORS = {
    "I": (0, 240, 240),
    "O": (240, 240, 0),
    "T": (160, 0, 240),
    "S": (0, 240, 0),
    "Z": (240, 0, 0),
    "J": (0, 0, 240),
    "L": (240, 160, 0),
}

ALL_SHAPES = tuple(SHAPE_CELLS.keys())


def _normalize(cells):
    cells = tuple(cells)
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def _rotate_cw(cells):
    return _normalize((c, -r) for r, c in cells)


def _rotate_ccw(cells):
    return _normalize((-c, r) for r, c in cells)


def base_cells(kind: str):
    """Canonical normalized cell offsets for a shape — for previews and tests."""
    return _normalize(SHAPE_CELLS[kind])


@dataclass(frozen=True)
class Tetromino:
    kind: str
    cells: tuple  # tuple of (row, col) offsets, normalized so min(row)=min(col)=0
    row: int = 0
    col: int = 0

    @classmethod
    def spawn(cls, kind: str, board_cols: int, spawn_row: int = 0) -> "Tetromino":
        cells = _normalize(SHAPE_CELLS[kind])
        width = max(c for _, c in cells) + 1
        return cls(kind=kind, cells=cells, row=spawn_row, col=(board_cols - width) // 2)

    def rotated_cw(self) -> "Tetromino":
        return Tetromino(self.kind, _rotate_cw(self.cells), self.row, self.col)

    def rotated_ccw(self) -> "Tetromino":
        return Tetromino(self.kind, _rotate_ccw(self.cells), self.row, self.col)

    def moved(self, dr: int = 0, dc: int = 0) -> "Tetromino":
        return Tetromino(self.kind, self.cells, self.row + dr, self.col + dc)

    def absolute_cells(self):
        return [(self.row + r, self.col + c) for r, c in self.cells]

    @property
    def color(self):
        return SHAPE_COLORS[self.kind]

    @property
    def height(self) -> int:
        return max(r for r, _ in self.cells) + 1

    @property
    def width(self) -> int:
        return max(c for _, c in self.cells) + 1
