"""Top-level pygame app: window, main loop, scene state machine."""
import pygame
from tetris import config
from tetris.scenes.game_scene import GameScene
from tetris.scenes.start_scene import StartScene


SCENES = {
    "start": StartScene,
    "game": GameScene,  # Phase 3: directly from start. Phase 4 inserts difficulty + countdown.
    # "difficulty": DifficultyScene,
    # "countdown":  CountdownScene,
}


def make_screen(w: int, h: int) -> pygame.Surface:
    # Respect minimum size: below it, stop shrinking content (per spec).
    w = max(w, config.MIN_WINDOW_W)
    h = max(h, config.MIN_WINDOW_H)
    return pygame.display.set_mode((w, h), pygame.RESIZABLE)


def run():
    pygame.init()
    pygame.display.set_caption(config.TITLE)
    screen = make_screen(config.WINDOW_W, config.WINDOW_H)
    clock = pygame.time.Clock()

    scene_name = "start"
    scene = SCENES[scene_name]()

    running = True
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = make_screen(event.w, event.h)
            else:
                scene.handle_event(event)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

        if getattr(scene, "done", False):
            next_name = getattr(scene, "NEXT", None)
            if next_name in SCENES:
                scene = SCENES[next_name]()
            else:
                running = False

    pygame.quit()
