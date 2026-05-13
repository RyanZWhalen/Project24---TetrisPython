"""Start screen: title + a centered green 'Start Game' button."""
import pygame
from tetris import config
from tetris.ui.widgets import Button, center_rect


class StartScene:
    NEXT = "difficulty"

    def __init__(self):
        self.title_font = pygame.font.SysFont("Helvetica", 72, bold=True)
        self.button_font = pygame.font.SysFont("Helvetica", 32, bold=True)
        self.button = Button(
            "Start Game",
            config.BTN_GREEN, config.BTN_GREEN_HOVER, config.BTN_TEXT,
            self.button_font,
        )
        self.done = False

    def handle_event(self, event):
        if self.button.clicked(event):
            self.done = True

    def update(self, dt):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill(config.BG)
        screen_rect = surface.get_rect()

        title = self.title_font.render("TETRIS", True, config.FG)
        surface.blit(
            title,
            title.get_rect(center=(screen_rect.centerx, screen_rect.centery - 80)),
        )

        btn_w, btn_h = 260, 72
        self.button.set_rect(center_rect(screen_rect, btn_w, btn_h, dy=40))
        self.button.draw(surface)
