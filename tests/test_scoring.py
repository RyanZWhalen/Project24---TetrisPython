import unittest
from tetris import config
from tetris.core.scoring import Score


class ScoringTests(unittest.TestCase):
    def test_initial_state(self):
        s = Score()
        self.assertEqual(s.points, 0)
        self.assertEqual(s.trophies, 0)

    def test_line_clear_values(self):
        for n, expected in config.LINE_CLEAR_POINTS.items():
            s = Score()
            s.add_lines(n)
            self.assertEqual(s.points, expected)

    def test_zero_or_negative_lines_noop(self):
        s = Score()
        s.add_lines(0)
        s.add_lines(-3)
        self.assertEqual(s.points, 0)

    def test_unknown_line_count_gives_no_points(self):
        s = Score()
        s.add_lines(5)
        self.assertEqual(s.points, 0)

    def test_overflow_mints_trophy_and_resets_to_zero(self):
        s = Score()
        s.points = config.SCORE_OVERFLOW_THRESHOLD  # 999_999
        s.add_lines(1)  # +40 -> overflow
        self.assertEqual(s.trophies, 1)
        self.assertEqual(s.points, 0)

    def test_no_overflow_when_just_under_threshold(self):
        s = Score()
        s.points = config.SCORE_OVERFLOW_THRESHOLD - 40  # 999_959
        s.add_lines(1)  # +40 -> exactly threshold, not over
        self.assertEqual(s.trophies, 0)
        self.assertEqual(s.points, config.SCORE_OVERFLOW_THRESHOLD)

    def test_trophy_cap_holds_at_max(self):
        s = Score()
        s.trophies = config.TROPHY_MAX  # 25
        s.points = config.SCORE_OVERFLOW_THRESHOLD - 10
        s.add_lines(4)  # +1200 -> would overflow, but trophies maxed
        self.assertEqual(s.trophies, config.TROPHY_MAX)
        self.assertEqual(s.points, config.SCORE_OVERFLOW_THRESHOLD)
        self.assertTrue(s.is_capped)


if __name__ == "__main__":
    unittest.main()
