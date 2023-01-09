
import pygame
from pygame.locals import *

from .assets import get_surface, get_sound

class Bullet(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    self.image = pygame.surface.Surface(size = (4, 4))
    self.image.fill(color = (255, 255, 0))

    self.rect = self.image.get_rect(
      center = position,
    )

    self.explode_sfx = get_sound("hero-explode.wav")

  def update(self):
    self.rect.y -= 4

    collisions = pygame.sprite.spritecollide(
      sprite = self,
      group = self.game.enemies,
      dokill = False,
    )

    if len(collisions) > 0:
      for c in collisions:
        c.destroy()
      self.explode_sfx.play()
      self.kill()
      return

    if self.rect.bottom < 0:
      self.kill()


class Hero(pygame.sprite.Sprite):
  def __init__(self, position, game):
    super().__init__()
    self.game = game

    self.images = [
      get_surface(f"hero/hero0{i + 1}.png")
      for i in range(4)
    ]

    self.image_index = 0

    self.rect = self.image.get_rect(
      center = position,
    )

    self.shoot_sfx = get_sound("shoot.wav")

    self.shooting = False

  @property
  def image(self):
    return self.images[self.image_index]

  def update(self):
    self.image_index += 1
    if self.image_index >= 4:
      self.image_index = 0

    pressed = pygame.key.get_pressed()
    boosted = pressed[K_LSHIFT]

    v = 2 * (2 if boosted else 1)

    if pressed[K_LEFT]:
      self.rect.x -= v

    if pressed[K_RIGHT]:
      self.rect.x += v

    if pressed[K_SPACE]:
      if not self.shooting:
        self.game.visible_sprites.add(
          Bullet(
            position = self.rect.center,
            game = self.game,
          )
        )
        self.shoot_sfx.play()
        self.shooting = True
    else:
      self.shooting = False

