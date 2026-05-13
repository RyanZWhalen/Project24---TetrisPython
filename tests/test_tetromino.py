import unittest
from tetris.core.tetromino import (
    Tetromino, ALL_SHAPES, SHAPE_CELLS, _normalize, _rotate_cw, _rotate_ccw,
)


class TetrominoTests(unittest.TestCase):
    def test_every_shape_has_four_cells(self):
        for kind in ALL_SHAPES:
            self.assertEqual(len(SHAPE_CELLS[kind]), 4, kind)

    def test_normalize_brings_corner_to_origin(self):
        cells = _normalize(((2, 3), (2, 4), (3, 3), (3, 4)))
        self.assertEqual(min(r for r, _ in cells), 0)
        self.assertEqual(min(c for _, c in cells), 0)

    def test_four_cw_rotations_return_to_original(self):
        for kind in ALL_SHAPES:
            base = _normalize(SHAPE_CELLS[kind])
            rotated = base
            for _ in range(4):
                rotated = _rotate_cw(rotated)
            self.assertEqual(rotated, base, kind)

    def test_cw_then_ccw_is_identity(self):
        for kind in ALL_SHAPES:
            base = _normalize(SHAPE_CELLS[kind])
            self.assertEqual(_rotate_ccw(_rotate_cw(base)), base, kind)

    def test_o_piece_is_rotation_invariant(self):
        base = _normalize(SHAPE_CELLS["O"])
        self.assertEqual(_rotate_cw(base), base)
        self.assertEqual(_rotate_ccw(base), base)

    def test_i_piece_alternates_horizontal_and_vertical(self):
        base = _normalize(SHAPE_CELLS["I"])  # horizontal: 1 row, 4 cols
        rotated = _rotate_cw(base)
        rows = {r for r, _ in rotated}
        cols = {c for _, c in rotated}
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(cols), 1)

    def test_spawn_centers_piece_horizontally(self):
        t = Tetromino.spawn("T", board_cols=10)
        # T has width 3 → expected col = (10 - 3)//2 = 3
        self.assertEqual(t.col, 3)
        self.assertEqual(t.row, 0)

    def test_moved_does_not_mutate_original(self):
        a = Tetromino.spawn("L", board_cols=10)
        b = a.moved(dr=1, dc=2)
        self.assertEqual(a.row, 0)
        self.assertEqual(a.col, (10 - a.width) // 2)
        self.assertEqual(b.row, 1)
        self.assertEqual(b.col, a.col + 2)


if __name__ == "__main__":
    unittest.main()
