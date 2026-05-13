"""FIFO hold queue for stored tetromino kinds.

Press-C enqueues; press-V dequeues the oldest. Capacity is per-difficulty,
so it's a required constructor arg — no module-level default.
"""
from __future__ import annotations
from collections import deque


class HoldQueue:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self.capacity = capacity
        self._items: deque[str] = deque()

    def __len__(self) -> int:
        return len(self._items)

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.capacity

    @property
    def is_empty(self) -> bool:
        return not self._items

    def push(self, kind: str) -> bool:
        """Enqueue a shape kind. Returns False if at capacity."""
        if self.is_full:
            return False
        self._items.append(kind)
        return True

    def pop(self) -> str | None:
        """Dequeue and return the OLDEST stored shape (FIFO). None if empty."""
        if self.is_empty:
            return None
        return self._items.popleft()

    def view(self) -> list[str]:
        """Oldest-to-newest snapshot for UI rendering."""
        return list(self._items)
