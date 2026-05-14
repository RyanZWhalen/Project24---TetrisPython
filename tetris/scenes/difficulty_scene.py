"""Difficulty selection: three buttons (Easy/Normal/Hard) center-aligned."""
from __future__ import annotations
import pygame
from tetris import config
from tetris.core.difficulty import EASY, NORMAL, HARD
from tetris.ui.widgets import Button


class DifficultyScene:
    NEXT = "countdown"

    def __init__(self):
        self.done = False
        self.payload: dict | None = None
        self.title_font = pygame.font.SysFont("Helvetica", 48, bold=True)
        self.subtitle_font = pygame.font.SysFont("Helvetica", 18)
        button_font = pygame.font.SysFont("Helvetica", 28, bold=True)
        self._buttons = [
            (EASY, Button(
                "Easy", config.BTN_GREEN, config.BTN_GREEN_HOVER,
                config.BTN_TEXT, button_font,
            )),
            (NORMAL, Button(
                "Normal", config.BTN_YELLOW, config.BTN_YELLOW_HOVER,
                config.BTN_TEXT, button_font,
            )),
            (HARD, Button(
                "Hard", config.BTN_RED, config.BTN_RED_HOVER,
                config.BTN_TEXT, button_font,
            )),
        ]

    def handle_event(self, event):
        for difficulty, btn in self._buttons:
            if btn.clicked(event):
                self.payload = {"difficulty": difficulty}
                self.done = True
                return

    def update(self, dt):
        pass

    def draw(self, surface):
        surface.fill(config.BG)
        screen = surface.get_rect()

        title = self.title_font.render("Select Difficulty", True, config.FG)
        surface.blit(title, title.get_rect(center=(screen.centerx, screen.centery - 110)))

        btn_w, btn_h = 180, 80
        gap = 30
        total_w = 3 * btn_w + 2 * gap
        x0 = (screen.w - total_w) // 2
        y0 = (screen.h - btn_h) // 2
        for i, (_, btn) in enumerate(self._buttons):
            btn.set_rect(pygame.Rect(x0 + i * (btn_w + gap), y0, btn_w, btn_h))
            btn.draw(surface)

        hint = self.subtitle_font.render(
            "Easy = slower drops, larger hold queue. Hard = fast drops, hold limit 1.",
            True, config.DIM,
        )
        surface.blit(hint, hint.get_rect(center=(screen.centerx, y0 + btn_h + 50)))
