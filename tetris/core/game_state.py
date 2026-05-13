"""The active-game conductor.

Owns the board, the current and next pieces, the hold queue, the score, and
the drop timer. All keyboard actions resolve to one of its public methods:

    move_left / move_right
    rotate_cw / rotate_ccw
    set_soft_drop(active)            # down arrow held / released
    try_store()                      # C key
    try_retrieve()                   # V key
    tick(dt)                         # one frame of elapsed time

Game over is a terminal state: once `game_over` flips True, further inputs
are no-ops and `tick` does nothing.
"""
from __future__ import annotations
import random
from tetris.core.bag import RandomBag
from tetris.core.board import Board
from tetris.core.difficulty import Difficulty, SOFT_DROP_SPEEDUP
from tetris.core.hold import HoldQueue
from tetris.core.scoring import Score
from tetris.core.tetromino import Tetromino


class GameState:
    def __init__(self, difficulty: Difficulty, rng: random.Random | None = None):
        self.difficulty = difficulty
        self.board = Board()
        self.bag = RandomBag(self.board.cols, rng=rng)
        self.hold = HoldQueue(capacity=difficulty.hold_capacity)
        self.score = Score()
        self.current: Tetromino = self.bag.draw()
        self.next: Tetromino = self.bag.draw()
        self.soft_drop = False
        self._drop_accum = 0.0
        self.game_over = False
        if not self.board.is_valid(self.current):
            self.game_over = True

    @property
    def drop_interval(self) -> float:
        base = self.difficulty.drop_interval
        return base / SOFT_DROP_SPEEDUP if self.soft_drop else base

    def tick(self, dt: float) -> None:
        if self.game_over or dt <= 0:
            return
        self._drop_accum += dt
        interval = self.drop_interval
        while self._drop_accum >= interval and not self.game_over:
            self._drop_accum -= interval
            self._step_down()

    def _step_down(self) -> None:
        candidate = self.current.moved(dr=1)
        if self.board.is_valid(candidate):
            self.current = candidate
        else:
            self._lock_current_and_advance()

    def _lock_current_and_advance(self) -> None:
        self.board.lock(self.current)
        cleared = self.board.clear_lines()
        self.score.add_lines(cleared)
        self.current = self.next
        self.next = self.bag.draw()
        self._drop_accum = 0.0
        if not self.board.is_valid(self.current):
            self.game_over = True

    def move_left(self) -> bool:
        return self._try_replace_current(self.current.moved(dc=-1))

    def move_right(self) -> bool:
        return self._try_replace_current(self.current.moved(dc=1))

    def rotate_cw(self) -> bool:
        return self._try_replace_current(self.current.rotated_cw())

    def rotate_ccw(self) -> bool:
        return self._try_replace_current(self.current.rotated_ccw())

    def _try_replace_current(self, candidate: Tetromino) -> bool:
        if self.game_over:
            return False
        if self.board.is_valid(candidate):
            self.current = candidate
            return True
        return False

    def set_soft_drop(self, active: bool) -> None:
        self.soft_drop = bool(active)

    def try_store(self) -> bool:
        """C key: enqueue current piece into the hold queue; receive the next piece.
        Returns False (no-op) if game over or hold is at capacity."""
        if self.game_over or self.hold.is_full:
            return False
        self.hold.push(self.current.kind)
        self._advance_to_next()
        return True

    def try_retrieve(self) -> bool:
        """V key: replace current piece with the OLDEST stored piece (FIFO dequeue).
        The previous current piece is discarded. Returns False if hold is empty."""
        if self.game_over or self.hold.is_empty:
            return False
        kind = self.hold.pop()
        assert kind is not None  # is_empty already checked
        self.current = Tetromino.spawn(kind, self.board.cols)
        self._drop_accum = 0.0
        if not self.board.is_valid(self.current):
            self.game_over = True
        return True

    def _advance_to_next(self) -> None:
        self.current = self.next
        self.next = self.bag.draw()
        self._drop_accum = 0.0
        if not self.board.is_valid(self.current):
            self.game_over = True
