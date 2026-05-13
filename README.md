# Project24 — TetrisPython

A native-desktop recreation of Tetris in Python, built with [pygame](https://www.pygame.org/).

## Run from source

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

A packaged single-file build (via PyInstaller) will be added once the game itself is feature-complete.

## Status

Currently scaffolded: window, scene state-machine, and the start screen with the centered green **Start Game** button. Difficulty select, gameplay, scoring, and the hold queue land in subsequent iterations.

## Controls (planned)

| Key            | Action                                     |
| -------------- | ------------------------------------------ |
| Left arrow     | Rotate 90° counter-clockwise               |
| Right arrow    | Rotate 90° clockwise                       |
| Down arrow     | Soft drop (2× fall speed)                  |
| C              | Store / un-store current shape (max 3)     |
