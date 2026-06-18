# Project24 — TetrisPython

A native-desktop recreation of Tetris in Python.

## About this project

TetrisPython is a clean-room recreation of Tetris that deliberately fuses elements from different eras of the game rather than copying a single one:

- **NES Tetris scoring (1989)** — the classic line-clear curve of **40 / 100 / 300 / 1200** points for clearing 1 / 2 / 3 / 4 rows in a single drop, and the single-shape "next piece" preview.
- **Modern Tetris mechanics (Tetris Guideline, ~2001+)** — full **Super Rotation System (SRS)** with per-piece wall-kick tables (including I-piece kicks and T-spin–enabling 5th tests), **20× soft drop** when down is held, smooth piece movement with **DAS** (Delayed Auto-Shift) repeat on held movement and rotation keys.
- **Original additions** — a **FIFO hold queue** with capacity that varies by difficulty (1 / 2 / 3 slots), three difficulty tiers with their own pre-game countdowns, and a **trophy-overflow scoring system** so the score never truly maxes out — once you cross 999,999 your score rolls back to 0 and you mint a trophy, displayed in a 5×5 grid for up to 25 trophies total.

Single-file native-desktop application. No browser, no web stack, no servers — `python3 run.py` and you're playing.

## Install

### The easy way: download a prebuilt binary

Grab the prebuilt artifact for your OS from the **[Releases page](https://github.com/RyanZWhalen/Project24---TetrisPython/releases)**. No Python or dependencies required.

| OS | Artifact | How to launch |
|----|----------|---------------|
| macOS | `Tetris.dmg` | Double-click, drag **Tetris.app** into **Applications**, then see the note below |
| macOS | `Tetris.app.zip` | Unzip, double-click `Tetris.app` (or `open Tetris.app`) |
| Windows | `Tetris.exe` | Double-click |
| Linux | `Tetris.tar.gz` | Untar, run `./Tetris/Tetris` |

> If no release artifact is available for your OS, fall back to one of the source paths below.

#### ⚠️ macOS first-launch note (unsigned app)

The app isn't code-signed or notarized (no Apple Developer account), so macOS Gatekeeper blocks it the first time with a *"can't be opened because the developer cannot be verified"* (or *"damaged"*) warning. This is a **one-time** step — do **one** of the following:

- **Right-click** `Tetris.app` in Applications → **Open** → **Open** in the dialog. (On macOS 15 Sequoia, instead try to open it, then go to **System Settings → Privacy & Security → Open Anyway**.)
- Or run this in Terminal once: `xattr -cr /Applications/Tetris.app`

After that it opens normally on every launch.

### Build the binary yourself (if you'd rather not trust a download)

You need Python 3.9+ and `pip`. The resulting `dist/Tetris.app` (or `.exe` / binary) is fully self-contained — no Python installation required to *run* it.

```bash
git clone https://github.com/RyanZWhalen/Project24---TetrisPython.git
cd Project24---TetrisPython
pip install -r requirements.txt
pip install pyinstaller
python3 build.py
```

`build.py` auto-selects the right PyInstaller mode for your OS:

| OS | Output | How to launch |
|----|--------|---------------|
| macOS | `dist/Tetris.app` | Double-click, or `open dist/Tetris.app` |
| Windows | `dist/Tetris.exe` | Double-click |
| Linux | `dist/Tetris/Tetris` | Run the binary inside `dist/Tetris/` |

Pass `--onefile` or `--onedir` to override the default mode.

#### Package a macOS `.dmg` (optional, macOS only)

To produce a polished drag-to-Applications `Tetris.dmg` (written to the repo
root, next to `Tetris.app.zip`, so it's easy to find):

```bash
brew install create-dmg        # preferred; falls back to hdiutil if absent
python3 build.py --dmg         # build the .app, then wrap it in Tetris.dmg
# or, against an already-built dist/Tetris.app:
python3 package_dmg.py
python3 package_dmg.py --check # mount, verify layout, detach
```

The resulting `.dmg` is **unsigned/un-notarized** — recipients need the one-time first-launch step described above. This step is a no-op on Windows/Linux.

### Run from source (for development)

```bash
git clone https://github.com/RyanZWhalen/Project24---TetrisPython.git
cd Project24---TetrisPython
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 run.py
```

## Controls

| Key | Action |
|-----|--------|
| **A / D** | Move piece left / right (hold to auto-repeat) |
| **← / →** | Rotate CCW / CW (hold to auto-repeat) |
| **↓** | Soft drop (20× drop speed while held) |
| **C** | Store current shape (FIFO queue, capacity by difficulty) |
| **V** | Retrieve oldest stored shape |
| **Esc** | Pause / unpause |

## Difficulty

| Mode | Drop speed | Pre-game countdown | Hold queue size |
|------|-----------|--------------------|-----------------|
| Easy | 1 row/sec | 5 seconds | 3 |
| Normal | 2 rows/sec | 3 seconds | 2 |
| Hard | 3 rows/sec | (none) | 1 |

## Scoring

| Lines cleared in one drop | Points |
|---------------------------|-------|
| 1 | 40 |
| 2 | 100 |
| 3 | 300 |
| 4 (Tetris) | 1200 |

Score caps at 999,999 — each overflow mints a trophy (shown in a 5×5 grid on the right panel) and resets the score to 0. Maximum 25 trophies.

## Development

Run the test suite (77 tests, pure stdlib `unittest`, no pygame required):

```bash
python3 -m unittest discover tests
```

## Got a high score? Liked the project?

If you enjoyed playing, here are two ways to support the project:

- **Star the repo** at [github.com/RyanZWhalen/Project24---TetrisPython](https://github.com/RyanZWhalen/Project24---TetrisPython) — it takes one click and helps me see that people are using it.
- **Share your high score** — message me on GitHub at [@RyanZWhalen](https://github.com/RyanZWhalen), or open an issue with a screenshot of your final score and trophy count. I'm genuinely curious how far players get on Hard mode.

Bug reports and pull requests welcome on the [Issues page](https://github.com/RyanZWhalen/Project24---TetrisPython/issues).
