# Project24 — TetrisPython

A native-desktop recreation of Tetris in Python, built with [pygame](https://www.pygame.org/).

## Run from source

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 run.py
```

## Build a standalone app (no Python required to run)

```bash
pip install pyinstaller
python3 build.py
```

`build.py` auto-selects the right PyInstaller mode for your OS:

| OS | Output | How to launch |
|----|--------|---------------|
| macOS | `dist/Tetris.app` | Double-click, or `open dist/Tetris.app` |
| Windows | `dist/Tetris.exe` | Double-click |
| Linux | `dist/Tetris/Tetris` | Run the binary inside `dist/Tetris/` |

You only need Python + pyinstaller installed to *build* the artifact. The artifact itself is self-contained — ship it to anyone on the same OS / CPU architecture and they can run it without installing Python.

Pass `--onefile` or `--onedir` to override the default mode.

## Controls

| Key | Action |
|-----|--------|
| **A / D** | Move piece left / right (hold to repeat) |
| **← / →** | Rotate CCW / CW (hold to repeat) |
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

## Tests

```bash
python3 -m unittest discover tests
```
