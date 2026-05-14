"""The active gameplay scene: board, side panels, controls cheat-sheet."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import pygame
from tetris import config
from tetris.core.difficulty import Difficulty, EASY
from tetris.core.game_state import GameState
from tetris.ui import render


@dataclass
class _RepeatState:
    """Per-held-key auto-repeat bookkeeping (DAS / ARR model)."""
    held_for: float        # total seconds since key was first pressed
    next_fire: float       # held_for value at which the next repeat should fire
    interval: float        # seconds between repeats once auto-repeat begins
    action: Callable[[], object]


CONTROL_LINES = [
    "A / D       move left / right",
    "Left / Right    rotate CCW / CW",
    "Down        soft drop (20x)",
    f"{config.KEY_STORE}            store shape",
    f"{config.KEY_RETRIEVE}            retrieve oldest",
    "Esc          pause / unpause",
]


class GameScene:
    NEXT = "start"

    # DAS = delay before auto-repeat kicks in; ARR = interval between repeats.
    MOVE_DAS = 0.17
    MOVE_ARR = 0.05
    ROTATE_DAS = 0.17
    ROTATE_ARR = 0.15

    def __init__(self, difficulty: Difficulty = EASY):
        self.difficulty = difficulty
        self.game = GameState(difficulty)
        self.done = False
        self.paused = False
        self._held: dict[int, _RepeatState] = {}
        self.title_font = pygame.font.SysFont("Helvetica", 24, bold=True)
        self.label_font = pygame.font.SysFont("Helvetica", 15, bold=True)
        self.value_font = pygame.font.SysFont("Helvetica", 30, bold=True)
        self.small_font = pygame.font.SysFont("Helvetica", 12)
        self.gameover_font = pygame.font.SysFont("Helvetica", 64, bold=True)

    def _start_repeat(self, key: int, das: float, arr: float, action: Callable[[], object]) -> None:
        self._held[key] = _RepeatState(held_for=0.0, next_fire=das, interval=arr, action=action)

    def _stop_repeat(self, key: int) -> None:
        self._held.pop(key, None)

    def handle_event(self, event):
        if self.game.game_over:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.done = True
            return
        # Esc toggles pause regardless of state; clear auto-repeats and soft-drop
        # so the piece doesn't keep doing things the moment we unpause.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            if self.paused:
                self.game.set_soft_drop(False)
                self._held.clear()
            return
        if self.paused:
            return
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_a:
                self.game.move_left()
                self._start_repeat(key, self.MOVE_DAS, self.MOVE_ARR, self.game.move_left)
            elif key == pygame.K_d:
                self.game.move_right()
                self._start_repeat(key, self.MOVE_DAS, self.MOVE_ARR, self.game.move_right)
            elif key == pygame.K_LEFT:
                self.game.rotate_ccw()
                self._start_repeat(key, self.ROTATE_DAS, self.ROTATE_ARR, self.game.rotate_ccw)
            elif key == pygame.K_RIGHT:
                self.game.rotate_cw()
                self._start_repeat(key, self.ROTATE_DAS, self.ROTATE_ARR, self.game.rotate_cw)
            elif key == pygame.K_DOWN:
                self.game.set_soft_drop(True)
            elif key == pygame.K_c:
                self.game.try_store()
            elif key == pygame.K_v:
                self.game.try_retrieve()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                self.game.set_soft_drop(False)
            self._stop_repeat(event.key)

    def update(self, dt):
        if self.paused:
            return
        for state in self._held.values():
            state.held_for += dt
            while state.held_for >= state.next_fire:
                state.action()
                state.next_fire += state.interval
        self.game.tick(dt)

    def draw(self, surface):
        surface.fill(config.BG)
        screen = surface.get_rect()
        cell = config.CELL_PX
        board_w = self.game.board.cols * cell
        board_h = self.game.board.rows * cell
        board_x = (screen.w - board_w) // 2
        board_y = (screen.h - board_h) // 2
        board_rect = pygame.Rect(board_x, board_y, board_w, board_h)

        left = pygame.Rect(10, board_y, max(0, board_x - 20), board_h)
        right = pygame.Rect(
            board_x + board_w + 10, board_y,
            max(0, screen.w - (board_x + board_w + 20)), board_h,
        )

        # Board background, locked cells, grid, then live piece overlay.
        pygame.draw.rect(surface, (24, 24, 30), board_rect)
        render.draw_board_cells(surface, self.game.board, (board_x, board_y), cell)
        render.draw_grid_lines(
            surface, (board_x, board_y), cell,
            self.game.board.cols, self.game.board.rows,
        )
        render.draw_piece_on_board(
            surface, self.game.current, (board_x, board_y), cell,
            self.game.board.rows, self.game.board.cols,
        )
        pygame.draw.rect(surface, config.FG, board_rect, width=2)

        if left.w > 60:
            self._draw_left_panel(surface, left)
        if right.w > 60:
            self._draw_right_panel(surface, right)

        if self.paused and not self.game.game_over:
            self._draw_paused_overlay(surface, screen)
        if self.game.game_over:
            self._draw_gameover_overlay(surface, screen)

    def _draw_left_panel(self, surface, rect):
        render.draw_panel(surface, rect)
        section_h = rect.h // 3
        sections = [
            ("Current", lambda r: render.draw_shape_preview(
                surface, self.game.current.kind, r.center, cell_size=18)),
            ("Next", lambda r: render.draw_shape_preview(
                surface, self.game.next.kind, r.center, cell_size=18)),
            ("Hold", lambda r: self._draw_hold_section(surface, r)),
        ]
        for i, (title, draw_content) in enumerate(sections):
            sec = pygame.Rect(rect.x, rect.y + i * section_h, rect.w, section_h)
            label = self.label_font.render(title, True, config.DIM)
            surface.blit(label, (sec.x + 12, sec.y + 8))
            content = pygame.Rect(sec.x, sec.y + 28, sec.w, sec.h - 32)
            draw_content(content)

    def _draw_hold_section(self, surface, rect):
        items = self.game.hold.view()
        capacity = self.difficulty.hold_capacity
        if not items:
            text = self.small_font.render(
                f"empty (max {capacity})", True, config.DIM,
            )
            surface.blit(text, text.get_rect(center=rect.center))
            return
        slot_h = rect.h // capacity
        for i, kind in enumerate(items):
            slot = pygame.Rect(rect.x, rect.y + i * slot_h, rect.w, slot_h)
            render.draw_shape_preview(surface, kind, slot.center, cell_size=14)

    def _draw_right_panel(self, surface, rect):
        render.draw_panel(surface, rect)

        # Score (top)
        x = rect.x + 12
        y = rect.y + 12
        surface.blit(self.label_font.render("Score", True, config.DIM), (x, y))
        y += 20
        score_text = self.value_font.render(str(self.game.score.points), True, config.FG)
        surface.blit(score_text, (x, y))
        y += 44

        # Trophies (only shown after first overflow)
        if self.game.score.trophies > 0:
            surface.blit(self.label_font.render("Trophies", True, config.DIM), (x, y))
            y += 22
            grid_rect = pygame.Rect(x, y, rect.w - 24, 110)
            self._draw_trophy_grid(surface, grid_rect)
            y += grid_rect.h + 12

        # Controls (bottom corner)
        line_h = 16
        controls_h = line_h * (len(CONTROL_LINES) + 1) + 8
        controls_y = max(y + 8, rect.bottom - controls_h - 10)
        surface.blit(self.label_font.render("Controls", True, config.DIM), (x, controls_y))
        for i, line in enumerate(CONTROL_LINES):
            text = self.small_font.render(line, True, config.FG)
            surface.blit(text, (x, controls_y + 20 + i * line_h))

    def _draw_trophy_grid(self, surface, rect):
        cols = config.TROPHY_GRID_COLS
        rows = config.TROPHY_GRID_ROWS
        cell = min(rect.w // cols, rect.h // rows)
        if cell <= 0:
            return
        for i in range(cols * rows):
            r = i // cols
            c = i % cols
            x = rect.x + c * cell
            y = rect.y + r * cell
            pad = cell // 6
            slot = pygame.Rect(x + pad, y + pad, cell - 2 * pad, cell - 2 * pad)
            if i < self.game.score.trophies:
                pygame.draw.rect(surface, (240, 200, 50), slot, border_radius=3)
                pygame.draw.rect(surface, (180, 140, 20), slot, width=1, border_radius=3)
            else:
                pygame.draw.rect(surface, config.GRID_LINE, slot, width=1, border_radius=3)

    def _draw_paused_overlay(self, surface, screen):
        overlay = pygame.Surface((screen.w, screen.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        title = self.gameover_font.render("Paused", True, config.FG)
        surface.blit(title, title.get_rect(center=(screen.centerx, screen.centery - 20)))
        hint = self.label_font.render("Press Esc to resume", True, config.DIM)
        surface.blit(hint, hint.get_rect(center=(screen.centerx, screen.centery + 40)))

    def _draw_gameover_overlay(self, surface, screen):
        overlay = pygame.Surface((screen.w, screen.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        title = self.gameover_font.render("Game Over", True, config.FG)
        surface.blit(title, title.get_rect(center=(screen.centerx, screen.centery - 40)))
        score_str = f"Score: {self.game.score.points}    Trophies: {self.game.score.trophies}"
        score_line = self.title_font.render(score_str, True, config.FG)
        surface.blit(score_line, score_line.get_rect(center=(screen.centerx, screen.centery + 20)))
        hint = self.label_font.render("Press any key to return", True, config.DIM)
        surface.blit(hint, hint.get_rect(center=(screen.centerx, screen.centery + 60)))
