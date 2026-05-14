"""Pre-game countdown scene.

Easy: shows 5 -> 4 -> 3 -> 2 -> 1 (one second each), then flashes "Game Start"
for one second, then transitions to GameScene.
Normal: same shape, starting from 3.
Hard: skips entirely (countdown_seconds=0 + show_game_start=False on the Difficulty).
"""
from __future__ import annotations
import pygame
from tetris import config
from tetris.core.countdown import Countdown, Phase
from tetris.core.difficulty import Difficulty


class CountdownScene:
    NEXT = "game"

    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self.countdown = Countdown(
            seconds=difficulty.countdown_seconds,
            show_game_start=difficulty.show_game_start,
        )
        self.payload = {"difficulty": difficulty}
        self.done = self.countdown.is_done  # Hard mode: nothing to render
        self.number_font = pygame.font.SysFont("Helvetica", 200, bold=True)
        self.text_font = pygame.font.SysFont("Helvetica", 80, bold=True)

    def handle_event(self, event):
        # Countdown is non-interactive; inputs are ignored.
        pass

    def update(self, dt):
        if self.done:
            return
        self.countdown.tick(dt)
        if self.countdown.is_done:
            self.done = True

    def draw(self, surface):
        surface.fill(config.BG)
        if self.done:
            return  # one-frame blank before transition; Hard mode never lingers
        screen = surface.get_rect()
        if self.countdown.phase == Phase.COUNTING:
            text = self.number_font.render(str(self.countdown.number), True, config.FG)
            surface.blit(text, text.get_rect(center=screen.center))
        elif self.countdown.phase == Phase.GAME_START:
            text = self.text_font.render("Game Start", True, config.FG)
            surface.blit(text, text.get_rect(center=screen.center))
