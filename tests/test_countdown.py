import unittest
from tetris.core.countdown import Countdown, Phase, GAME_START_DURATION
from tetris.core.difficulty import EASY, NORMAL, HARD


class CountdownTests(unittest.TestCase):
    # --- Easy: 5s countdown -> "Game Start" -> done ---

    def test_easy_initial_state(self):
        c = Countdown(seconds=EASY.countdown_seconds, show_game_start=EASY.show_game_start)
        self.assertEqual(c.phase, Phase.COUNTING)
        self.assertEqual(c.number, 5)
        self.assertFalse(c.is_done)

    def test_easy_displays_5_4_3_2_1_as_time_elapses(self):
        c = Countdown(seconds=5, show_game_start=True)
        observed = [c.number]
        for _ in range(4):
            c.tick(1.0)
            observed.append(c.number)
        self.assertEqual(observed, [5, 4, 3, 2, 1])
        self.assertEqual(c.phase, Phase.COUNTING)

    def test_easy_transitions_to_game_start_after_5s(self):
        c = Countdown(seconds=5, show_game_start=True)
        c.tick(5.0 + 1e-6)
        self.assertEqual(c.phase, Phase.GAME_START)

    def test_easy_transitions_to_done_after_game_start_duration(self):
        c = Countdown(seconds=5, show_game_start=True)
        c.tick(5.0 + 1e-6)
        c.tick(GAME_START_DURATION + 1e-6)
        self.assertEqual(c.phase, Phase.DONE)
        self.assertTrue(c.is_done)

    # --- Normal: 3s countdown -> "Game Start" -> done ---

    def test_normal_runs_3_seconds_then_game_start(self):
        c = Countdown(seconds=NORMAL.countdown_seconds, show_game_start=NORMAL.show_game_start)
        c.tick(3.0 + 1e-6)
        self.assertEqual(c.phase, Phase.GAME_START)

    def test_normal_displays_3_2_1(self):
        c = Countdown(seconds=3, show_game_start=True)
        self.assertEqual(c.number, 3)
        c.tick(1.0); self.assertEqual(c.number, 2)
        c.tick(1.0); self.assertEqual(c.number, 1)

    # --- Hard: skip everything ---

    def test_hard_skips_to_done_immediately(self):
        c = Countdown(seconds=HARD.countdown_seconds, show_game_start=HARD.show_game_start)
        self.assertEqual(c.phase, Phase.DONE)
        self.assertTrue(c.is_done)

    def test_hard_tick_after_done_stays_done(self):
        c = Countdown(seconds=0, show_game_start=False)
        c.tick(10.0)
        self.assertEqual(c.phase, Phase.DONE)

    # --- Long-dt safety ---

    def test_single_long_tick_crosses_both_phases(self):
        c = Countdown(seconds=5, show_game_start=True)
        # 5s countdown + 1s game-start + slack => should end in DONE
        c.tick(5.0 + GAME_START_DURATION + 0.5)
        self.assertEqual(c.phase, Phase.DONE)

    # --- Boundary numbers ---

    def test_number_clamps_to_one_near_end(self):
        c = Countdown(seconds=5, show_game_start=True)
        c.tick(4.999)
        self.assertEqual(c.number, 1)

    def test_number_at_exact_boundary_is_correct(self):
        c = Countdown(seconds=5, show_game_start=True)
        # exactly 4.0 elapsed -> 1.0s remaining -> ceil(1.0) = 1
        c.tick(4.0)
        self.assertEqual(c.number, 1)


if __name__ == "__main__":
    unittest.main()
