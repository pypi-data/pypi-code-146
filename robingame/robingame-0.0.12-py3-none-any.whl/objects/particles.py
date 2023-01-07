import pygame
from pygame import Rect
from pygame.color import Color

from robingame.objects.entity import PhysicalEntity
from robingame.utils import circle_surf


class Particle(PhysicalEntity):
    blit_flag = pygame.BLEND_RGB_ADD
    gravity: float
    friction: float
    decay: float
    color: Color
    radius: float

    def __init__(
        self,
        x,
        y,
        u=0,
        v=0,
        radius=None,
        color=None,
        gravity=None,
        friction=None,
        decay=None,
        blit_flag=None,
    ):
        super().__init__()
        self.color = self.color if color is None else color
        self.gravity = self.gravity if gravity is None else gravity
        self.friction = self.friction if friction is None else friction
        self.decay = self.decay if decay is None else decay
        self.blit_flag = self.blit_flag if blit_flag is None else blit_flag
        self.radius = self.radius if radius is None else radius
        self.rect = Rect(0, 0, 0, 0)
        self.x = x
        self.y = y
        self.u = u
        self.v = v

    def update(self):
        self.x += self.u
        self.y += self.v
        self.v += self.gravity
        self.u *= 1 - self.friction
        self.v *= 1 - self.friction
        self.radius -= self.decay
        if self.death_condition:
            self.kill()

    def draw(self, surface, debug=False):
        surf = circle_surf(round(self.radius), self.color)
        image_rect = surf.get_rect()
        image_rect.center = self.rect.center
        surface.blit(surf, image_rect, special_flags=self.blit_flag)

    @property
    def death_condition(self):
        return self.radius <= 0
