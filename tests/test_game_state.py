import random
import unittest

from tetris.core.difficulty import EASY, NORMAL, HARD, SOFT_DROP_SPEEDUP
from tetris.core.game_state import GameState
from tetris.core.tetromino import Tetromino


def fresh(difficulty=EASY, seed=0) -> GameState:
    return GameState(difficulty, rng=random.Random(seed))


class GameStateBasicTests(unittest.TestCase):
    def test_initial_state(self):
        gs = fresh()
        self.assertIsNotNone(gs.current)
        self.assertIsNotNone(gs.next)
        self.assertFalse(gs.game_over)
        self.assertEqual(gs.score.points, 0)
        self.assertEqual(gs.score.trophies, 0)
        self.assertEqual(len(gs.hold), 0)

    def test_hold_capacity_matches_difficulty(self):
        self.assertEqual(fresh(EASY).hold.capacity, 3)
        self.assertEqual(fresh(NORMAL).hold.capacity, 2)
        self.assertEqual(fresh(HARD).hold.capacity, 1)


class GameStateTimingTests(unittest.TestCase):
    def test_tick_drops_piece_one_row_per_interval(self):
        gs = fresh(EASY)
        start_row = gs.current.row
        gs.tick(EASY.drop_interval + 1e-6)
        self.assertEqual(gs.current.row, start_row + 1)

    def test_soft_drop_halves_interval(self):
        gs = fresh(EASY)
        gs.set_soft_drop(True)
        start_row = gs.current.row
        half = EASY.drop_interval / SOFT_DROP_SPEEDUP + 1e-6
        gs.tick(half)
        self.assertEqual(gs.current.row, start_row + 1)

    def test_releasing_soft_drop_restores_normal_speed(self):
        gs = fresh(EASY)
        gs.set_soft_drop(True)
        gs.set_soft_drop(False)
        self.assertAlmostEqual(gs.drop_interval, EASY.drop_interval)

    def test_tick_drops_multiple_rows_on_long_dt(self):
        gs = fresh(EASY)
        start_row = gs.current.row
        gs.tick(EASY.drop_interval * 3 + 1e-6)
        self.assertEqual(gs.current.row, start_row + 3)


class GameStateMovementTests(unittest.TestCase):
    def test_move_left_then_right_restores_column(self):
        gs = fresh(EASY)
        start_col = gs.current.col
        gs.move_left()
        self.assertLess(gs.current.col, start_col)
        gs.move_right()
        self.assertEqual(gs.current.col, start_col)

    def test_move_left_blocked_at_wall(self):
        gs = fresh(EASY)
        while gs.move_left():
            pass
        col = gs.current.col
        self.assertFalse(gs.move_left())
        self.assertEqual(gs.current.col, col)

    def test_rotate_cw_changes_cells_for_non_o_piece(self):
        gs = fresh(EASY)
        gs.current = Tetromino.spawn("T", gs.board.cols)
        before = gs.current.cells
        self.assertTrue(gs.rotate_cw())
        self.assertNotEqual(gs.current.cells, before)

    def test_rotate_cw_then_ccw_restores_cells(self):
        gs = fresh(EASY)
        gs.current = Tetromino.spawn("L", gs.board.cols)
        before = gs.current.cells
        gs.rotate_cw()
        gs.rotate_ccw()
        self.assertEqual(gs.current.cells, before)

    def test_rotation_blocked_by_collision_is_rejected(self):
        gs = fresh(EASY)
        gs.current = Tetromino.spawn("I", gs.board.cols)
        # Surround with locked cells so any rotation must collide.
        for r in range(gs.board.rows):
            for c in range(gs.board.cols):
                if (r, c) not in gs.current.absolute_cells():
                    gs.board.grid[r][c] = (1, 1, 1)
        before = gs.current.cells
        self.assertFalse(gs.rotate_cw())
        self.assertEqual(gs.current.cells, before)

    def test_t_spin_uses_srs_fifth_kick(self):
        # Classic T-spin: a T-shaped slot two rows deep, only reachable by
        # rotating into it via the SRS 5th kick (which includes a 2-row drop).
        # This test only passes with the per-transition SRS kick tables; the
        # old flat 6-entry kick list could not reach it.
        gs = fresh(EASY)
        rows = gs.board.rows
        cols = gs.board.cols
        # Build a wall on cols 0-2 and 4-9; col 3 is open. Bottom row is
        # filled except for col 3, with col 4 also empty just below the cap:
        #
        #   col: 0 1 2 3 4 5 6 7 8 9
        #   r-2: # # # . . # # # # #
        #   r-1: # # # . # # # # # #     <-- target T-spin slot at (r-1, 3..4) hump at (r-2, 3)
        for c in range(cols):
            if c not in (3, 4):
                gs.board.grid[rows - 2][c] = (1, 1, 1)
            if c != 3:
                gs.board.grid[rows - 1][c] = (1, 1, 1)
        gs.board.grid[rows - 2][4] = None  # carve the slot
        # Place a T-piece in rotation state L (pointing left), hovering above
        # the slot. From this state, rotating CW should pivot the T into the
        # slot via a kick.
        t = Tetromino.spawn("T", cols).rotated_ccw()      # state L (3)
        # Move it horizontally so the piece sits over column 3.
        t = Tetromino(
            kind=t.kind, cells=t.cells,
            row=rows - 4, col=2, rotation=t.rotation,
        )
        gs.current = t
        # In-place CW rotation collides with the wall; only the kick table
        # rescues it.
        self.assertTrue(gs.rotate_cw())
        # After the T-spin, the bottom row gap at col 3 should be filled by
        # part of the rotated T.
        abs_cells = set(gs.current.absolute_cells())
        self.assertIn((rows - 1, 3), abs_cells)

    def test_wall_kick_rescues_rotation_at_right_wall(self):
        # Stand the I-piece up vertically, jam it against the right wall, then
        # rotate again: the raw rotated horizontal form would put a cell at
        # column 10 (off the board). The (0, -1) kick should rescue it.
        gs = fresh(EASY)
        gs.current = Tetromino.spawn("I", gs.board.cols)
        self.assertTrue(gs.rotate_cw())  # vertical
        while gs.move_right():
            pass
        col_before_rotate = gs.current.col
        self.assertTrue(gs.rotate_cw())
        # The kick should have shifted the piece left by at least one column.
        max_c_after = max(c for _, c in gs.current.absolute_cells())
        self.assertLess(max_c_after, gs.board.cols)
        self.assertLess(gs.current.col, col_before_rotate)


class GameStateHoldTests(unittest.TestCase):
    def test_store_when_empty_consumes_next(self):
        gs = fresh(EASY)
        cur_kind = gs.current.kind
        next_kind = gs.next.kind
        self.assertTrue(gs.try_store())
        self.assertEqual(gs.current.kind, next_kind)
        self.assertEqual(gs.hold.view(), [cur_kind])

    def test_store_blocked_when_hold_full(self):
        gs = fresh(HARD)  # capacity = 1
        gs.try_store()  # hold = [X]
        current_before = gs.current.kind
        hold_before = gs.hold.view()
        self.assertFalse(gs.try_store())
        self.assertEqual(gs.current.kind, current_before)
        self.assertEqual(gs.hold.view(), hold_before)

    def test_retrieve_returns_oldest_stored_fifo(self):
        gs = fresh(EASY)  # capacity = 3
        stored = []
        for _ in range(3):
            stored.append(gs.current.kind)
            self.assertTrue(gs.try_store())
        self.assertEqual(gs.hold.view(), stored)
        self.assertTrue(gs.try_retrieve())
        self.assertEqual(gs.current.kind, stored[0])  # oldest out first
        self.assertEqual(gs.hold.view(), stored[1:])

    def test_retrieve_empty_is_noop(self):
        gs = fresh(EASY)
        before = gs.current.kind
        self.assertFalse(gs.try_retrieve())
        self.assertEqual(gs.current.kind, before)

    def test_retrieve_when_partially_full_works_too(self):
        # 4-case truth-table line 2: not-full hold + retrieve should still pull oldest.
        gs = fresh(EASY)
        stored_kind = gs.current.kind
        gs.try_store()  # hold = [stored_kind]
        gs.try_retrieve()
        self.assertEqual(gs.current.kind, stored_kind)
        self.assertTrue(gs.hold.is_empty)


class GameStateLockingTests(unittest.TestCase):
    def test_full_row_clears_and_awards_points(self):
        gs = fresh(EASY)
        # Fill row 19 except column 0; drop a 1x1 sliver into that hole.
        for c in range(1, gs.board.cols):
            gs.board.grid[19][c] = (1, 1, 1)
        gs.current = Tetromino.spawn("O", gs.board.cols)  # any piece is fine
        # Place a single-cell synthetic piece into (19, 0) by direct lock+clear.
        gs.board.grid[19][0] = (2, 2, 2)
        cleared = gs.board.clear_lines()
        self.assertEqual(cleared, 1)
        gs.score.add_lines(cleared)
        self.assertEqual(gs.score.points, 40)

    def test_game_over_when_next_spawn_overlaps_grid(self):
        gs = fresh(EASY)
        # Fill rows 0 and 1 leaving one (different) gap per row so neither row clears.
        for r in (0, 1):
            for c in range(gs.board.cols):
                if c != r:
                    gs.board.grid[r][c] = (1, 1, 1)
        # Force a lock-and-advance: the new spawn must collide → game over.
        gs._lock_current_and_advance()
        self.assertTrue(gs.game_over)

    def test_inputs_are_noops_after_game_over(self):
        gs = fresh(EASY)
        gs.game_over = True
        self.assertFalse(gs.move_left())
        self.assertFalse(gs.move_right())
        self.assertFalse(gs.rotate_cw())
        self.assertFalse(gs.rotate_ccw())
        self.assertFalse(gs.try_store())
        self.assertFalse(gs.try_retrieve())
        before_row = gs.current.row
        gs.tick(10.0)
        self.assertEqual(gs.current.row, before_row)


if __name__ == "__main__":
    unittest.main()
