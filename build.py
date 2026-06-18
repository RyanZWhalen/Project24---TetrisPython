"""Build a standalone executable with PyInstaller.

Usage:
    python3 build.py

Produces in dist/:
    macOS    dist/Tetris.app              double-click, or `open dist/Tetris.app`
    Windows  dist/Tetris.exe              double-click
    Linux    dist/Tetris/Tetris           launch the binary inside the folder

Mode is chosen automatically:
    - macOS uses onedir (PyInstaller deprecates onefile+windowed for .app bundles).
    - Windows uses onefile so the deliverable is a single .exe.
    - Linux uses onedir (so SDL libs co-locate with the binary).

Override with --onefile or --onedir if you have a reason to.

Pass --dmg (macOS only) to also wrap dist/Tetris.app in a drag-to-Applications
dist/Tetris.dmg after the build. No-op on Windows/Linux. See package_dmg.py.
"""
from __future__ import annotations
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.resolve()
APP_NAME = "Tetris"


def pick_mode() -> str:
    if "--onefile" in sys.argv:
        return "--onefile"
    if "--onedir" in sys.argv:
        return "--onedir"
    system = platform.system()
    if system == "Darwin":
        return "--onedir"   # required for .app bundles
    if system == "Windows":
        return "--onefile"  # clean single .exe deliverable
    return "--onedir"       # Linux: keep SDL libs next to the binary


def clean_previous_artifacts() -> None:
    for d in ("build", "dist"):
        p = ROOT / d
        if p.exists():
            print(f"Removing {p}")
            shutil.rmtree(p)
    for spec in ROOT.glob("*.spec"):
        print(f"Removing {spec}")
        spec.unlink()


def main() -> int:
    mode = pick_mode()
    clean_previous_artifacts()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_NAME,
        "--windowed",
        mode,
        "--noconfirm",
        str(ROOT / "run.py"),
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode != 0:
        return result.returncode

    if "--dmg" in sys.argv:
        if platform.system() == "Darwin":
            print("\nPackaging .dmg ...")
            import package_dmg
            rc = package_dmg.build_dmg()
            if rc != 0:
                return rc
        else:
            print("\n--dmg ignored: .dmg packaging is macOS-only.")

    print()
    print(f"Build complete ({mode}). Artifacts in dist/:")
    for f in sorted((ROOT / "dist").iterdir()):
        print(f"  {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
