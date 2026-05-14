"""The 7 standard tetrominoes with SRS-style fixed-box rotation.

Each piece is defined by its cells inside a fixed NxN bounding box (N=4 for I,
N=2 for O, N=3 for everyone else). Rotation maps (r, c) -> (c, N-1-r) for CW,
which is equivalent to rotating around the box center. The box never changes
size on rotation, so the piece's logical (row, col) on the board stays stable
across rotations — this is what makes SRS feel right.
"""
from __future__ import annotations
from dataclasses import dataclass


SHAPE_DATA = {
    # cells: (row, col) offsets inside an NxN bounding box.
    "I": {"cells": ((1, 0), (1, 1), (1, 2), (1, 3)), "box": 4},
    "O": {"cells": ((0, 0), (0, 1), (1, 0), (1, 1)), "box": 2},
    "T": {"cells": ((0, 0), (0, 1), (0, 2), (1, 1)), "box": 3},
    "S": {"cells": ((0, 1), (0, 2), (1, 0), (1, 1)), "box": 3},
    "Z": {"cells": ((0, 0), (0, 1), (1, 1), (1, 2)), "box": 3},
    "J": {"cells": ((0, 0), (1, 0), (1, 1), (1, 2)), "box": 3},
    "L": {"cells": ((0, 2), (1, 0), (1, 1), (1, 2)), "box": 3},
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

ALL_SHAPES = tuple(SHAPE_DATA.keys())


def _rotate_in_box_cw(cells, box):
    return tuple(sorted((c, box - 1 - r) for r, c in cells))


def _rotate_in_box_ccw(cells, box):
    return tuple(sorted((box - 1 - c, r) for r, c in cells))


def base_cells(kind: str):
    """Canonical spawn-rotation cells for a shape (for previews and tests)."""
    return SHAPE_DATA[kind]["cells"]


def base_box(kind: str) -> int:
    return SHAPE_DATA[kind]["box"]


@dataclass(frozen=True)
class Tetromino:
    kind: str
    cells: tuple        # (row, col) offsets within an NxN bounding box
    row: int = 0        # bounding-box top-left row on the board
    col: int = 0        # bounding-box top-left col on the board
    rotation: int = 0   # SRS rotation state: 0 (spawn) / 1 (R) / 2 (180) / 3 (L)

    @classmethod
    def spawn(cls, kind: str, board_cols: int) -> "Tetromino":
        cells = SHAPE_DATA[kind]["cells"]
        box = SHAPE_DATA[kind]["box"]
        min_r = min(r for r, _ in cells)
        return cls(
            kind=kind, cells=cells,
            row=-min_r,                       # top visible cell sits at row 0
            col=(board_cols - box) // 2,      # center by box width
        )

    @property
    def box(self) -> int:
        return SHAPE_DATA[self.kind]["box"]

    def rotated_cw(self) -> "Tetromino":
        return Tetromino(
            self.kind, _rotate_in_box_cw(self.cells, self.box),
            self.row, self.col, (self.rotation + 1) % 4,
        )

    def rotated_ccw(self) -> "Tetromino":
        return Tetromino(
            self.kind, _rotate_in_box_ccw(self.cells, self.box),
            self.row, self.col, (self.rotation - 1) % 4,
        )

    def moved(self, dr: int = 0, dc: int = 0) -> "Tetromino":
        return Tetromino(
            self.kind, self.cells, self.row + dr, self.col + dc, self.rotation,
        )

    def absolute_cells(self):
        return [(self.row + r, self.col + c) for r, c in self.cells]

    @property
    def color(self):
        return SHAPE_COLORS[self.kind]

    @property
    def width(self) -> int:
        cs = [c for _, c in self.cells]
        return max(cs) - min(cs) + 1

    @property
    def height(self) -> int:
        rs = [r for r, _ in self.cells]
        return max(rs) - min(rs) + 1
