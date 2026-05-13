import unittest
from tetris.core.hold import HoldQueue


class HoldQueueTests(unittest.TestCase):
    def test_starts_empty(self):
        q = HoldQueue(capacity=3)
        self.assertTrue(q.is_empty)
        self.assertEqual(len(q), 0)
        self.assertIsNone(q.pop())

    def test_push_until_full(self):
        q = HoldQueue(capacity=3)
        self.assertTrue(q.push("T"))
        self.assertTrue(q.push("L"))
        self.assertTrue(q.push("J"))
        self.assertTrue(q.is_full)
        self.assertFalse(q.push("S"))
        self.assertEqual(len(q), 3)

    def test_pop_returns_fifo_order(self):
        q = HoldQueue(capacity=3)
        for k in ("T", "L", "J"):
            q.push(k)
        self.assertEqual(q.pop(), "T")  # oldest first
        self.assertEqual(q.pop(), "L")
        self.assertEqual(q.pop(), "J")
        self.assertTrue(q.is_empty)

    def test_view_is_oldest_to_newest_and_isolated(self):
        q = HoldQueue(capacity=3)
        for k in ("T", "L", "J"):
            q.push(k)
        self.assertEqual(q.view(), ["T", "L", "J"])
        q.view().append("X")  # mutating snapshot must not affect internal state
        self.assertEqual(q.view(), ["T", "L", "J"])

    def test_per_difficulty_capacities(self):
        # Hard = 1, Normal = 2, Easy = 3
        for cap in (1, 2, 3):
            q = HoldQueue(capacity=cap)
            for i in range(cap):
                self.assertTrue(q.push(f"k{i}"), f"capacity {cap} should accept push #{i}")
            self.assertFalse(q.push("over"))

    def test_zero_capacity_rejects_everything(self):
        q = HoldQueue(capacity=0)
        self.assertTrue(q.is_full)
        self.assertFalse(q.push("T"))


if __name__ == "__main__":
    unittest.main()
