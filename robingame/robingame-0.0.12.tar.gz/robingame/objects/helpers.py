import time
from collections import deque

import pygame
from pygame.color import Color
from pygame.surface import Surface

from robingame.objects.entity import Entity
from robingame.text.font import fonts


class FpsTracker(Entity):
    """Displays a little number in the top right of the window if debug=True"""

    buffer_length = 60
    font = fonts.cellphone_black

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.queue = deque(maxlen=self.buffer_length)

    def update(self):
        t = time.perf_counter()
        self.queue.append(t)
        seconds = self.queue[-1] - self.queue[0]
        self.fps = int(self.buffer_length / seconds) if seconds else 0

    def draw(self, surface: Surface, debug: bool = False):
        if debug:
            scale = 2
            width = 50 * scale
            surf = Surface((width, width // 4))
            surf.fill(Color("white"))
            self.font.render(surf, f"FPS: {self.fps}", wrap=width, align=0, scale=scale)
            rect = surf.get_rect()
            rect.right = surface.get_rect().right - 10
            rect.top = surface.get_rect().top + 10
            surface.blit(surf, rect)
