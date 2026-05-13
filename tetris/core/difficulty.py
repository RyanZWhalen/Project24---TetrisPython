"""Per-difficulty game parameters bundled into one frozen descriptor.

A Difficulty object is the contract passed from the Difficulty scene forward:
the Countdown scene reads `countdown_seconds` / `show_game_start`; the
GameState reads `drop_interval` and `hold_capacity`. Adding a new difficulty
(or rebalancing one) is a single edit here.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Difficulty:
    name: str                # human-readable label, e.g. "Easy"
    drop_interval: float     # seconds per row at normal speed (soft drop halves it)
    hold_capacity: int       # max items in the FIFO hold queue
    countdown_seconds: int   # pre-game countdown duration (0 = skip entirely)
    show_game_start: bool    # whether to flash "Game Start" after countdown


EASY = Difficulty(
    name="Easy",
    drop_interval=1.0,
    hold_capacity=3,
    countdown_seconds=5,
    show_game_start=True,
)

NORMAL = Difficulty(
    name="Normal",
    drop_interval=0.5,
    hold_capacity=2,
    countdown_seconds=3,
    show_game_start=True,
)

HARD = Difficulty(
    name="Hard",
    drop_interval=1.0 / 3.0,
    hold_capacity=1,
    countdown_seconds=0,
    show_game_start=False,
)

ALL = (EASY, NORMAL, HARD)

# Multiplier applied to drop_interval while the down arrow is held.
SOFT_DROP_SPEEDUP = 2.0
