import unittest
from tetris.core.hold import HoldStack


class HoldStackTests(unittest.TestCase):
    def test_starts_empty(self):
        s = HoldStack()
        self.assertTrue(s.is_empty)
        self.assertEqual(len(s), 0)
        self.assertIsNone(s.pop())

    def test_push_until_full(self):
        s = HoldStack()
        self.assertTrue(s.push("T"))
        self.assertTrue(s.push("L"))
        self.assertTrue(s.push("J"))
        self.assertTrue(s.is_full)
        self.assertFalse(s.push("S"))  # rejected at capacity
        self.assertEqual(len(s), 3)

    def test_pop_returns_lifo_order(self):
        s = HoldStack()
        for k in ("T", "L", "J"):
            s.push(k)
        self.assertEqual(s.pop(), "J")
        self.assertEqual(s.pop(), "L")
        self.assertEqual(s.pop(), "T")
        self.assertTrue(s.is_empty)

    def test_view_returns_bottom_to_top_snapshot(self):
        s = HoldStack()
        for k in ("T", "L", "J"):
            s.push(k)
        self.assertEqual(s.view(), ["T", "L", "J"])
        s.view().append("X")  # mutating returned list must not affect internal state
        self.assertEqual(s.view(), ["T", "L", "J"])


if __name__ == "__main__":
    unittest.main()
