"""LIFO storage queue (capacity 3) for held tetromino kinds."""
from __future__ import annotations
from tetris import config


class HoldStack:
    def __init__(self, capacity: int = config.HOLD_CAPACITY):
        self.capacity = capacity
        self._stack: list[str] = []

    def __len__(self) -> int:
        return len(self._stack)

    @property
    def is_full(self) -> bool:
        return len(self._stack) >= self.capacity

    @property
    def is_empty(self) -> bool:
        return not self._stack

    def push(self, kind: str) -> bool:
        if self.is_full:
            return False
        self._stack.append(kind)
        return True

    def pop(self) -> str | None:
        if self.is_empty:
            return None
        return self._stack.pop()

    def view(self) -> list[str]:
        """Bottom-to-top snapshot of stored shapes (for UI rendering)."""
        return list(self._stack)
