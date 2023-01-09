
import sys
from importlib import resources

from dataclasses import dataclass, field

import pygame
from pygame.locals import *

from .assets import get_surface, MUSIC_PATH
from .hero import Hero



class Enemy(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()

    self.image = get_surface("enemy01.png")

    self.rect = self.image.get_rect(
      center = position,
    )

    self.direction = +1

    self.exploding = False
    self.explode_index = 0

    self.explosions = [
      get_surface(f"explode0{i+1}.png")
      for i in range(4)
    ]

  def destroy(self):
    self.exploding = True

  def update(self):
    if self.exploding:
      self.image = self.explosions[self.explode_index]
      self.explode_index += 1
      if self.explode_index >= 4:
        self.kill()
    else:
      self.rect.x += self.direction

      if self.rect.right >= 320 or self.rect.left <= 0:
        self.direction = -self.direction
        self.rect.y += 8


@dataclass(frozen = True)
class Instant:
  t: int
  dt: int

class Game(object):
  def __init__(self):
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()

    self.display_surface = pygame.display.set_mode(
      size = (1280, 720),
    )

    self.render_surface = pygame.surface.Surface(
      size = (320, 180),
    )

    pygame.display.set_caption("kerblaxion")

    self.clock = pygame.time.Clock()
    self.fps = 30

    self.visible_sprites = pygame.sprite.Group()
    self.player_bullets = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()

    self.visible_sprites.add(Hero(
      position = (180, 160),
      game = self,
    ))

    for x in range(16, 260, 24):
      for y in range(16, 100, 24):
        e = Enemy(position = (x, y))
        self.visible_sprites.add(e)
        self.enemies.add(e)



  def run(self):
    pygame.mixer.music.load(MUSIC_PATH.joinpath("level01.mp3").open())
    pygame.mixer.music.play(-1)
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()

      self.visible_sprites.update()

      self.render_surface.fill(color = (0, 0, 0))
      self.visible_sprites.draw(self.render_surface)

      pygame.transform.scale(
        surface = self.render_surface,
        size = (1280, 720),
        dest_surface = self.display_surface,
      )

      pygame.display.update()

      self.clock.tick(self.fps)
