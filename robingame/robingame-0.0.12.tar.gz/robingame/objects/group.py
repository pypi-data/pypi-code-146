import pygame


class Group(pygame.sprite.Group):
    """Container for multiple sprite objects."""

    def update(self, *args):
        super().update(*args)

    def draw(self, surface, debug=False):
        """Draws all of the member sprites onto the given surface."""
        sprites = self.sprites()
        for sprite in sprites:
            sprite.draw(surface, debug)
        self.lostsprites = []

    def kill(self):
        """Kill all the sprites in this group. This is different from .empty().
        empty() does not kill the sprites in other groups."""
        for sprite in self:
            sprite.kill()
