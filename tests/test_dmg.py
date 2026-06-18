"""Guarded macOS .dmg packaging check.

Skips cleanly unless we're on macOS AND Tetris.dmg has already been built
(via `python3 build.py --dmg` or `python3 package_dmg.py`), so the suite stays
green on Windows/Linux and in source-only checkouts. When the .dmg exists it is
mounted, inspected for the app + Applications drop-link, and detached.
"""
import importlib.util
import platform
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DMG_PATH = ROOT / "Tetris.dmg"


@unittest.skipUnless(platform.system() == "Darwin", "macOS-only")
@unittest.skipUnless(DMG_PATH.exists(), "Tetris.dmg not built")
class DmgTests(unittest.TestCase):
    def test_dmg_mounts_with_expected_layout(self):
        spec = importlib.util.spec_from_file_location("package_dmg", ROOT / "package_dmg.py")
        package_dmg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package_dmg)
        self.assertEqual(package_dmg.check_dmg(), 0)


if __name__ == "__main__":
    unittest.main()
