"""Package dist/Tetris.app into a drag-to-Applications Tetris.dmg (macOS only).

The .dmg is written to the repo root (next to Tetris.app.zip) so it's easy to
find rather than buried in dist/.

Usage:
    python3 package_dmg.py            # build Tetris.dmg from dist/Tetris.app
    python3 package_dmg.py --check    # mount the built .dmg, verify layout, detach

This is an ADDITIVE macOS-only step. It does nothing on Windows/Linux. The
existing .app / .zip / .exe / .tar.gz build paths are untouched.

The .dmg ships UNSIGNED and un-notarized: there is no Apple Developer cert on
this project. Users must do a one-time Gatekeeper bypass on first launch — see
README.md ("can't be opened" workaround).

Preferred backend is `create-dmg` (brew install create-dmg), which lays out the
window with the app icon on the left and an /Applications drop-link on the
right. If create-dmg is unavailable we fall back to a plain `hdiutil create`
disk image that still contains Tetris.app plus an Applications symlink.
"""
from __future__ import annotations
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).parent.resolve()
APP_NAME = "Tetris"
VOLNAME = "Tetris"
APP_PATH = ROOT / "dist" / f"{APP_NAME}.app"
# Output to the repo root (next to Tetris.app.zip) so the deliverable is easy to
# find rather than buried in dist/. Gitignored so it still isn't committed.
DMG_PATH = ROOT / f"{APP_NAME}.dmg"


def _require_macos() -> None:
    if platform.system() != "Darwin":
        print("package_dmg: .dmg packaging is macOS-only; skipping.")
        raise SystemExit(0)


def _build_with_create_dmg() -> int:
    """Layout matches the README: app on the left, Applications drop on the right."""
    cmd = [
        "create-dmg",
        "--volname", VOLNAME,
        "--window-size", "600", "400",
        "--icon", f"{APP_NAME}.app", "150", "190",
        "--app-drop-link", "450", "190",
        "--hide-extension", f"{APP_NAME}.app",
        str(DMG_PATH),
        str(APP_PATH),
    ]
    print("Running:", " ".join(cmd))
    # create-dmg returns 2 when it succeeds but couldn't set the volume icon
    # (harmless, common in headless/CI). Treat 0 and 2 as success if the .dmg exists.
    result = subprocess.run(cmd, cwd=str(ROOT))
    if result.returncode not in (0, 2):
        return result.returncode
    return 0 if DMG_PATH.exists() else (result.returncode or 1)


def _build_with_hdiutil() -> int:
    """Fallback: stage app + /Applications symlink, then hdiutil create."""
    print("create-dmg not found; falling back to hdiutil.")
    with tempfile.TemporaryDirectory() as tmp:
        stage = Path(tmp) / VOLNAME
        stage.mkdir()
        print(f"Staging {APP_PATH.name} -> {stage}")
        shutil.copytree(APP_PATH, stage / APP_PATH.name, symlinks=True)
        (stage / "Applications").symlink_to("/Applications")
        cmd = [
            "hdiutil", "create",
            "-volname", VOLNAME,
            "-srcfolder", str(stage),
            "-ov",                 # overwrite an existing .dmg
            "-format", "UDZO",     # compressed, read-only
            str(DMG_PATH),
        ]
        print("Running:", " ".join(cmd))
        result = subprocess.run(cmd, cwd=str(ROOT))
        return result.returncode


def build_dmg() -> int:
    _require_macos()
    if not APP_PATH.exists():
        print(f"error: {APP_PATH} not found. Run `python3 build.py` first.", file=sys.stderr)
        return 1
    if DMG_PATH.exists():
        print(f"Removing existing {DMG_PATH.relative_to(ROOT)}")
        DMG_PATH.unlink()

    rc = _build_with_create_dmg() if shutil.which("create-dmg") else _build_with_hdiutil()
    if rc != 0 or not DMG_PATH.exists():
        print("error: .dmg build failed.", file=sys.stderr)
        return rc or 1

    size_mb = DMG_PATH.stat().st_size / (1024 * 1024)
    print(f"\nBuilt {DMG_PATH.name} ({size_mb:.1f} MB)")
    print(f"  -> {DMG_PATH}")
    print("NOTE: unsigned/un-notarized — first-launch Gatekeeper bypass required (see README).")
    # Reveal it in Finder so it's easy to grab (best-effort; ignored if unavailable).
    subprocess.run(["open", "-R", str(DMG_PATH)], capture_output=True)
    return 0


def check_dmg() -> int:
    """Mount the built .dmg, confirm it contains the app + Applications link, detach."""
    _require_macos()
    if not DMG_PATH.exists():
        print(f"error: {DMG_PATH} not found. Build it first.", file=sys.stderr)
        return 1

    print(f"Mounting {DMG_PATH.relative_to(ROOT)} ...")
    out = subprocess.run(
        ["hdiutil", "attach", str(DMG_PATH), "-nobrowse", "-readonly"],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        print(out.stderr, file=sys.stderr)
        return out.returncode

    # Last whitespace-delimited field of the attach output is the mount point.
    mount_point = None
    for line in out.stdout.splitlines():
        if "/Volumes/" in line:
            mount_point = line.split("\t")[-1].strip() or line.split()[-1]
    try:
        if not mount_point:
            print("error: could not determine mount point.", file=sys.stderr)
            return 1
        mp = Path(mount_point)
        app_ok = (mp / f"{APP_NAME}.app").exists()
        apps_link = mp / "Applications"
        apps_ok = apps_link.is_symlink() or apps_link.exists()
        print(f"  mounted at {mp}")
        print(f"  {APP_NAME}.app present: {app_ok}")
        print(f"  Applications drop-link present: {apps_ok}")
        ok = app_ok and apps_ok
    finally:
        print("Detaching ...")
        subprocess.run(["hdiutil", "detach", mount_point], capture_output=True, text=True)

    print("OK" if ok else "FAILED")
    return 0 if ok else 1


def main() -> int:
    if "--check" in sys.argv:
        return check_dmg()
    return build_dmg()


if __name__ == "__main__":
    sys.exit(main())
