"""Central game constants: window, board, colors, speeds, scoring."""

# Window
WINDOW_W = 800
WINDOW_H = 720
MIN_WINDOW_W = 480
MIN_WINDOW_H = 540
TITLE = "Tetris"
FPS = 60

# Board geometry
BOARD_COLS = 10
BOARD_ROWS = 20
CELL_PX = 30

# Colors (R, G, B)
BG = (18, 18, 24)
FG = (240, 240, 245)
DIM = (140, 140, 150)
BTN_GREEN = (70, 180, 90)
BTN_GREEN_HOVER = (90, 210, 110)
BTN_YELLOW = (230, 200, 60)
BTN_YELLOW_HOVER = (250, 220, 80)
BTN_RED = (210, 70, 70)
BTN_RED_HOVER = (235, 95, 95)
BTN_TEXT = (12, 12, 16)
GRID_LINE = (40, 40, 50)

# Key bindings (display names; per-difficulty drop intervals, hold capacity,
# and countdown live in tetris.core.difficulty)
KEY_STORE = "C"
KEY_RETRIEVE = "V"

# Scoring (classic NES line-clear curve)
LINE_CLEAR_POINTS = {1: 40, 2: 100, 3: 300, 4: 1200}

# Trophy overflow: when score would exceed this, mint a trophy and carry the overage.
SCORE_OVERFLOW_THRESHOLD = 999_999
TROPHY_GRID_COLS = 5
TROPHY_GRID_ROWS = 5
TROPHY_MAX = TROPHY_GRID_COLS * TROPHY_GRID_ROWS  # 25
