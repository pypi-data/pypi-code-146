import pygame.mouse

from robingame.gui.button import Button
from robingame.objects import Game, Group, Particle
from robingame.utils import mouse_hovering_over, random_int


class ComplicatedOnPressHookExample(Game):
    """
    This is an example where the on_press hook adds particles to the outer Game class at the
    position of the Button instance. To do this it needs access to both the Game and Button
    instances.
    """

    screen_color = (50, 50, 50)

    def __init__(self):
        super().__init__()
        self.buttons = Group()
        self.particles = Group()
        self.child_groups += [self.buttons, self.particles]
        self.buttons.add(
            Button(
                x=200,
                y=100,
                width=400,
                height=50,
                text="press and hold for smoke",
                on_press=(
                    lambda button: (
                        self.particles.add(Flash(x=button.x, y=button.y)),
                        self.particles.add(Glow(x=button.x, y=button.y) for _ in range(10)),
                    )
                ),
                on_release=(lambda button: self.particles.kill()),
            )
        )

    def update(self):
        super().update()

        # button manager stuff
        for button in self.buttons:
            if mouse_hovering_over(button):
                button.is_focused = True
                button.is_pressed = pygame.mouse.get_pressed()[0]
            else:
                button.is_focused = False
                button.is_pressed = False


class Flash(Particle):
    gravity = 0.1
    friction = 0.1
    decay = 20
    color = (150, 200, 150)
    radius = 100


class Glow(Particle):
    gravity = 0.1
    friction = 0.1
    decay = 0.1
    color = (20, 20, 20)
    radius = 50

    def __init__(self, x, y):
        super().__init__(x, y, u=random_int(-5, 5), v=random_int(-5, 5))


if __name__ == "__main__":
    ComplicatedOnPressHookExample().main()
