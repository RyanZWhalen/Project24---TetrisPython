import unittest
from tetris.core.tetromino import (
    Tetromino, ALL_SHAPES, SHAPE_DATA, base_cells, base_box,
    _rotate_in_box_cw, _rotate_in_box_ccw,
)


class TetrominoTests(unittest.TestCase):
    def test_every_shape_has_four_cells(self):
        for kind in ALL_SHAPES:
            self.assertEqual(len(SHAPE_DATA[kind]["cells"]), 4, kind)

    def test_box_sizes_match_srs_conventions(self):
        self.assertEqual(base_box("I"), 4)
        self.assertEqual(base_box("O"), 2)
        for kind in ("T", "S", "Z", "J", "L"):
            self.assertEqual(base_box(kind), 3, kind)

    def test_four_cw_rotations_return_to_original(self):
        for kind in ALL_SHAPES:
            base = base_cells(kind)
            box = base_box(kind)
            rotated = base
            for _ in range(4):
                rotated = _rotate_in_box_cw(rotated, box)
            self.assertEqual(set(rotated), set(base), kind)

    def test_cw_then_ccw_is_identity(self):
        for kind in ALL_SHAPES:
            base = base_cells(kind)
            box = base_box(kind)
            rotated_cw = _rotate_in_box_cw(base, box)
            self.assertEqual(set(_rotate_in_box_ccw(rotated_cw, box)), set(base), kind)

    def test_o_piece_is_rotation_invariant(self):
        base = base_cells("O")
        self.assertEqual(set(_rotate_in_box_cw(base, 2)), set(base))
        self.assertEqual(set(_rotate_in_box_ccw(base, 2)), set(base))

    def test_i_piece_alternates_horizontal_and_vertical(self):
        base = base_cells("I")
        rotated = _rotate_in_box_cw(base, 4)
        rows = {r for r, _ in rotated}
        cols = {c for _, c in rotated}
        self.assertEqual(len(rows), 4)  # vertical: 4 distinct rows
        self.assertEqual(len(cols), 1)  # vertical: 1 column

    def test_srs_rotation_keeps_bounding_box_stable(self):
        # The key SRS property: rotating doesn't shift the piece's (row, col).
        t = Tetromino.spawn("T", board_cols=10)
        self.assertEqual(t.rotated_cw().row, t.row)
        self.assertEqual(t.rotated_cw().col, t.col)
        self.assertEqual(t.rotated_ccw().row, t.row)
        self.assertEqual(t.rotated_ccw().col, t.col)

    def test_spawn_centers_piece_horizontally(self):
        # T uses a 3-wide box -> col = (10 - 3) // 2 = 3
        self.assertEqual(Tetromino.spawn("T", 10).col, 3)
        # I uses a 4-wide box -> col = (10 - 4) // 2 = 3
        self.assertEqual(Tetromino.spawn("I", 10).col, 3)
        # O uses a 2-wide box -> col = (10 - 2) // 2 = 4
        self.assertEqual(Tetromino.spawn("O", 10).col, 4)

    def test_spawn_places_top_visible_cell_at_row_zero(self):
        for kind in ALL_SHAPES:
            t = Tetromino.spawn(kind, 10)
            top_visible = min(r for r, _ in t.absolute_cells())
            self.assertEqual(top_visible, 0, kind)

    def test_moved_does_not_mutate_original(self):
        a = Tetromino.spawn("L", board_cols=10)
        b = a.moved(dr=1, dc=2)
        self.assertEqual(a.row, 0)
        self.assertEqual(b.row, 1)
        self.assertEqual(b.col, a.col + 2)


if __name__ == "__main__":
    unittest.main()
