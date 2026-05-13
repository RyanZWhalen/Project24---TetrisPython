"""Random tetromino generator."""
from __future__ import annotations
import random
from tetris.core.tetromino import Tetromino, ALL_SHAPES


class RandomBag:
    """Pure uniform random draws across the 7 shapes."""

    def __init__(self, board_cols: int, rng: random.Random | None = None):
        self.board_cols = board_cols
        self.rng = rng or random.Random()

    def draw(self) -> Tetromino:
        return Tetromino.spawn(self.rng.choice(ALL_SHAPES), self.board_cols)
