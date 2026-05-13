"""Reusable widgets and layout helpers."""
import pygame


def center_rect(outer: pygame.Rect, w: int, h: int, dy: int = 0) -> pygame.Rect:
    """An (w x h) rect centered inside `outer`, with optional vertical offset."""
    return pygame.Rect(
        outer.x + (outer.w - w) // 2,
        outer.y + (outer.h - h) // 2 + dy,
        w, h,
    )


class Button:
    def __init__(self, label, color, hover_color, text_color, font, radius=14):
        self.label = label
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font
        self.radius = radius
        self.rect = pygame.Rect(0, 0, 0, 0)

    def set_rect(self, rect: pygame.Rect):
        self.rect = rect

    def draw(self, surface: pygame.Surface):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.hover_color if hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.radius)
        text = self.font.render(self.label, True, self.text_color)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
