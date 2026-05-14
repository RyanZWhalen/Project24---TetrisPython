"""Low-level drawing helpers: cells, shape previews, the play field."""
from __future__ import annotations
import pygame
from tetris import config
from tetris.core.board import Board
from tetris.core.tetromino import Tetromino, SHAPE_COLORS, base_cells


def draw_cell(surface: pygame.Surface, color, rect: pygame.Rect) -> None:
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, width=1)


def draw_grid_lines(surface: pygame.Surface, top_left, cell_size, cols, rows) -> None:
    x0, y0 = top_left
    for c in range(cols + 1):
        x = x0 + c * cell_size
        pygame.draw.line(surface, config.GRID_LINE, (x, y0), (x, y0 + rows * cell_size))
    for r in range(rows + 1):
        y = y0 + r * cell_size
        pygame.draw.line(surface, config.GRID_LINE, (x0, y), (x0 + cols * cell_size, y))


def draw_board_cells(surface: pygame.Surface, board: Board, top_left, cell_size) -> None:
    x0, y0 = top_left
    for r in range(board.rows):
        for c in range(board.cols):
            color = board.grid[r][c]
            if color is not None:
                rect = pygame.Rect(x0 + c * cell_size, y0 + r * cell_size, cell_size, cell_size)
                draw_cell(surface, color, rect)


def draw_piece_on_board(surface: pygame.Surface, piece: Tetromino, top_left, cell_size, board_rows, board_cols) -> None:
    x0, y0 = top_left
    for r, c in piece.absolute_cells():
        if r < 0 or r >= board_rows or c < 0 or c >= board_cols:
            continue
        rect = pygame.Rect(x0 + c * cell_size, y0 + r * cell_size, cell_size, cell_size)
        draw_cell(surface, piece.color, rect)


def draw_shape_preview(surface: pygame.Surface, kind: str, center, cell_size: int) -> None:
    """Render a tetromino centered at `center` in a small preview area."""
    cells = base_cells(kind)
    color = SHAPE_COLORS[kind]
    w = max(c for _, c in cells) + 1
    h = max(r for r, _ in cells) + 1
    cx, cy = center
    x0 = cx - (w * cell_size) // 2
    y0 = cy - (h * cell_size) // 2
    for r, c in cells:
        rect = pygame.Rect(x0 + c * cell_size, y0 + r * cell_size, cell_size, cell_size)
        draw_cell(surface, color, rect)


def draw_panel(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Outlined rounded container — caller draws content on top."""
    pygame.draw.rect(surface, (28, 28, 36), rect, border_radius=8)
    pygame.draw.rect(surface, config.GRID_LINE, rect, width=2, border_radius=8)
