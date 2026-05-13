import unittest
from tetris.core.difficulty import EASY, NORMAL, HARD, ALL, SOFT_DROP_SPEEDUP


class DifficultyTests(unittest.TestCase):
    def test_all_contains_three_in_easy_to_hard_order(self):
        self.assertEqual(ALL, (EASY, NORMAL, HARD))

    def test_drop_intervals_match_spec(self):
        self.assertAlmostEqual(EASY.drop_interval, 1.0)
        self.assertAlmostEqual(NORMAL.drop_interval, 0.5)
        self.assertAlmostEqual(HARD.drop_interval, 1.0 / 3.0)

    def test_hold_capacities_match_spec(self):
        self.assertEqual(EASY.hold_capacity, 3)
        self.assertEqual(NORMAL.hold_capacity, 2)
        self.assertEqual(HARD.hold_capacity, 1)

    def test_countdowns_match_spec(self):
        self.assertEqual(EASY.countdown_seconds, 5)
        self.assertEqual(NORMAL.countdown_seconds, 3)
        self.assertEqual(HARD.countdown_seconds, 0)
        self.assertTrue(EASY.show_game_start)
        self.assertTrue(NORMAL.show_game_start)
        self.assertFalse(HARD.show_game_start)

    def test_soft_drop_halves_interval_across_modes(self):
        # Total traversal for 20 rows under soft drop should be exactly half
        # of the normal traversal, in every mode.
        for d in ALL:
            normal_total = 20 * d.drop_interval
            soft_total = 20 * (d.drop_interval / SOFT_DROP_SPEEDUP)
            self.assertAlmostEqual(soft_total, normal_total / 2.0)

    def test_difficulty_is_frozen(self):
        with self.assertRaises(Exception):
            EASY.drop_interval = 0.1  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
