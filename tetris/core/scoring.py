"""Score + trophy bookkeeping with rollover at SCORE_OVERFLOW_THRESHOLD."""
from __future__ import annotations
from tetris import config


class Score:
    def __init__(self):
        self.points: int = 0
        self.trophies: int = 0

    def add_lines(self, n: int) -> None:
        if n <= 0:
            return
        self.add_points(config.LINE_CLEAR_POINTS.get(n, 0))

    def add_points(self, p: int) -> None:
        if p <= 0 or self.is_capped:
            return
        self.points += p
        if self.points > config.SCORE_OVERFLOW_THRESHOLD:
            if self.trophies < config.TROPHY_MAX:
                self.trophies += 1
                self.points = 0
            else:
                self.points = config.SCORE_OVERFLOW_THRESHOLD

    @property
    def is_capped(self) -> bool:
        return (
            self.trophies >= config.TROPHY_MAX
            and self.points >= config.SCORE_OVERFLOW_THRESHOLD
        )
