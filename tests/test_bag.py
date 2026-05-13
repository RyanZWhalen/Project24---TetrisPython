import random
import unittest
from tetris.core.bag import RandomBag
from tetris.core.tetromino import ALL_SHAPES


class BagTests(unittest.TestCase):
    def test_draws_produce_all_seven_shapes(self):
        bag = RandomBag(board_cols=10, rng=random.Random(42))
        seen = {bag.draw().kind for _ in range(1000)}
        self.assertEqual(seen, set(ALL_SHAPES))

    def test_drawn_piece_is_within_board_columns(self):
        bag = RandomBag(board_cols=10, rng=random.Random(0))
        for _ in range(100):
            p = bag.draw()
            cols = {p.col + c for _, c in p.cells}
            self.assertTrue(min(cols) >= 0)
            self.assertTrue(max(cols) < 10)


if __name__ == "__main__":
    unittest.main()
