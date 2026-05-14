"""Pre-game countdown state machine.

Three phases: COUNTING (display the seconds remaining as 5..1), GAME_START
(flash "Game Start" for one second), DONE (start play). Hard mode skips
straight to DONE because its Difficulty has countdown_seconds=0 and
show_game_start=False.
"""
from __future__ import annotations
import math
from enum import Enum


GAME_START_DURATION = 1.0  # seconds to flash "Game Start"


class Phase(Enum):
    COUNTING = "counting"
    GAME_START = "game_start"
    DONE = "done"


class Countdown:
    def __init__(self, seconds: int, show_game_start: bool):
        self._counting_duration = float(max(0, seconds))
        self._show_game_start = bool(show_game_start) and self._counting_duration > 0
        self._elapsed = 0.0
        if self._counting_duration <= 0:
            self.phase = Phase.DONE if not self._show_game_start else Phase.GAME_START
        else:
            self.phase = Phase.COUNTING

    def tick(self, dt: float) -> None:
        if dt <= 0 or self.phase == Phase.DONE:
            return
        self._elapsed += dt
        # A single tick may cross multiple phase boundaries (long dt safety).
        while True:
            if self.phase == Phase.COUNTING:
                if self._elapsed < self._counting_duration:
                    return
                self._elapsed -= self._counting_duration
                self.phase = Phase.GAME_START if self._show_game_start else Phase.DONE
                if self.phase == Phase.DONE:
                    return
            elif self.phase == Phase.GAME_START:
                if self._elapsed < GAME_START_DURATION:
                    return
                self._elapsed -= GAME_START_DURATION
                self.phase = Phase.DONE
                return
            else:
                return  # DONE

    @property
    def number(self) -> int:
        """Display value during COUNTING (e.g. 5, 4, 3, 2, 1). Undefined otherwise."""
        remaining = self._counting_duration - self._elapsed
        return max(1, math.ceil(remaining))

    @property
    def is_done(self) -> bool:
        return self.phase == Phase.DONE
