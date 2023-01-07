from typing import Iterable

from pygame.color import Color
from pygame.surface import Surface

from robingame.image import brighten_color
from robingame.input import GamecubeController
from robingame.objects import Entity, Group, Particle


class SmashParticle(Particle):
    radius = 20
    decay = 2
    color = Color("red")
    gravity = 0
    friction = 0
    blit_flag = 0


class GamecubeControllerVisualizer(Entity):
    input: GamecubeController

    def __init__(self, x, y, input: GamecubeController, groups: Iterable = ()):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.input = input
        self.particles = Group()
        self.child_groups = [
            self.particles,
        ]

    def update(self):
        super().update()
        mapping = {
            self.input.LEFT: dict(x=10, y=10 + 50),
            self.input.RIGHT: dict(x=10 + 40, y=10 + 50),
            self.input.UP: dict(x=10 + 20, y=10 + 30),
            self.input.DOWN: dict(x=10 + 20, y=10 + 30 + 40),
            self.input.C_LEFT: dict(x=10 + 70, y=10 + 80 + 10, radius=10),
            self.input.C_RIGHT: dict(x=10 + 70 + 20, y=10 + 80 + 10, radius=10),
            self.input.C_UP: dict(x=10 + 70 + 10, y=10 + 80, radius=10),
            self.input.C_DOWN: dict(x=10 + 70 + 10, y=10 + 80 + 20, radius=10),
        }
        for input, kwargs in mapping.items():
            if input.is_smashed:
                self.particles.add(SmashParticle(**kwargs))

    def draw(self, surface, debug=False):
        background = Surface((160, 120))
        background.fill(Color("black"))

        # buttons
        self.draw_button(background, (20, 20), Color("cyan"), self.input.A, (100, 50))
        self.draw_button(background, (10, 10), Color("red"), self.input.B, (100, 80))
        self.draw_button(background, (20, 10), Color("gray"), self.input.Y, (100, 30))
        self.draw_button(background, (10, 20), Color("gray"), self.input.X, (130, 50))
        self.draw_button(background, (10, 10), Color("gray"), self.input.START, (65, 50))
        self.draw_button(background, (10, 10), Color("purple"), self.input.Z, (130, 30))
        self.draw_button(background, (7, 7), Color("gray"), self.input.D_PAD_UP, (40 + 8, 87 - 8))
        self.draw_button(background, (7, 7), Color("gray"), self.input.D_PAD_DOWN, (40 + 8, 87 + 8))
        self.draw_button(background, (7, 7), Color("gray"), self.input.D_PAD_LEFT, (40, 87))
        self.draw_button(background, (7, 7), Color("gray"), self.input.D_PAD_RIGHT, (40 + 16, 87))

        super().draw(background, debug)
        # sticks
        self.draw_joystick(
            background,
            (40, 40),
            Color("gray"),
            x_axis=(self.input.LEFT, self.input.RIGHT),
            y_axis=(self.input.UP, self.input.DOWN),
            xy=(0, 30),
        )
        self.draw_joystick(
            background,
            (20, 20),
            Color("orange"),
            x_axis=(self.input.C_LEFT, self.input.C_RIGHT),
            y_axis=(self.input.C_UP, self.input.C_DOWN),
            xy=(70, 80),
        )

        self.draw_trigger(
            background,
            (40, 20),
            Color("gray"),
            axis=self.input.R_AXIS,
            button=self.input.R,
            xy=(100, 0),
        )
        self.draw_trigger(
            background,
            (40, 20),
            Color("gray"),
            axis=self.input.L_AXIS,
            button=self.input.L,
            xy=(0, 0),
        )
        rect = background.get_rect()
        rect.topleft = self.x, self.y
        surface.blit(background, rect)

    def draw_trigger(self, surface, size, color, axis, button, xy):
        dx, dy = xy

        bbox = Surface(size)
        bbox.fill(color)
        bbox_rect = bbox.get_rect()
        bbox_rect.topleft = (dx + 10, dy + 10)
        surface.blit(bbox, bbox_rect)

        btn = Surface((size[0], size[1] - (size[1] * 0.8 * axis.value)))
        btn.fill(Color("red") if button.is_down else brighten_color(color, 100))
        btn_rect = btn.get_rect()
        btn_rect.centerx = bbox_rect.centerx
        btn_rect.bottom = bbox_rect.bottom
        surface.blit(btn, btn_rect)

    def draw_joystick(self, surface, size, color, x_axis, y_axis, xy):
        left, right = x_axis
        up, down = y_axis
        x_axis = right - left
        y_axis = down - up
        bbox = Surface(size)
        bbox.fill(color)
        bbox_rect = bbox.get_rect()
        dx, dy = xy
        bbox_rect.topleft = (dx + 10, dy + 10)
        surface.blit(bbox, bbox_rect)

        stick = Surface(tuple(s // 2 for s in size))
        is_smashed = any(input.is_smashed for input in (left, right, up, down))
        stick.fill(Color("red") if is_smashed else brighten_color(color, 100))
        rect = stick.get_rect()
        rect.center = (
            bbox_rect.centerx + x_axis * size[0] // 2,
            bbox_rect.centery + y_axis * size[1] // 2,
        )
        surface.blit(stick, rect)

    def draw_button(self, surface, size, color, input, xy):
        # B button
        btn = Surface(size)
        btn.fill(Color("white") if input.is_down else color)
        rect = btn.get_rect()
        dx, dy = xy
        rect.topleft = (dx + 10, dy + 10)
        surface.blit(btn, rect)


if __name__ == "__main__":

    class GCVizGame(Game):
        screen_color = Color("darkgray")

        def __init__(self):
            super().__init__()
            self.input = GamecubeController(controller_id=0)
            self.objects = Group()
            self.child_groups = [
                self.objects,
            ]
            self.visualizer = GamecubeControllerVisualizer(
                x=0,
                y=0,
                input=self.input,
                groups=[self.objects],
            )

        def read_inputs(self):
            super().read_inputs()
            self.input.read_new_inputs()

    GCVizGame().main()
