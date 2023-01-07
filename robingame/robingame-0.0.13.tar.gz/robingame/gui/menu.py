import numpy
import pygame

from robingame.animation import ease_in_out
from robingame.objects import Entity, Group
from robingame.input import EventQueue
from robingame.utils import mouse_hovering_over


class Menu(Entity):
    """Base menu class."""

    def __init__(self, *groups):
        super().__init__(*groups)
        self.buttons = Group()
        self.child_groups = [self.buttons]

    def add_button(self, *objects):
        self.add_to_group(*objects, group=self.buttons)

    def update(self):
        self.update_buttons()
        super().update()

    def state_idle(self):
        pass

    def update_buttons(self):
        """todo: if you wanted to make this really efficient, you could only perform updates if
        an event is detected."""
        mouse_click = any(event.type == pygame.MOUSEBUTTONDOWN for event in EventQueue.events)
        for button in self.buttons:
            button.is_focused = False
            button.is_pressed = False
            if mouse_hovering_over(button):
                if mouse_click:
                    button.is_pressed = True
                else:
                    button.is_focused = True


class MyMenu(Menu):
    button_width = 200
    button_height = 50
    button_size = (button_width, button_height)
    transition_length = 40

    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = self.animate_in

    @property
    def game_rect(self):
        return self.game.window.get_rect()

    def arrange_buttons_vertically(self):
        num_buttons = len(self.buttons)
        top = self.game.window.get_rect().top + 150
        bottom = top + self.button_height * 1.5 * num_buttons
        ys = numpy.linspace(top, bottom, num=num_buttons)
        for button, y in zip(self.buttons, ys):
            button.y = y

    def animate_in(self):
        if self.tick == 0:
            self.arrange_buttons_vertically()
        try:
            # todo: maybe make these generators so that you're not generating the entire array
            #  each tick
            centerx = self.game_rect.centerx
            far_left = self.game_rect.left - self.button_width
            x = ease_in_out(x=self.tick, start=far_left, stop=centerx, num=self.transition_length)
            for button in self.buttons:
                button.x = x
        except IndexError:
            self.state = self.state_idle

    def animate_out(self, next_scene=None):
        def _animate_out():
            if next_scene:
                self.game.add_scene(next_scene)
            try:

                centerx = self.game_rect.centerx
                far_right = self.game_rect.right + self.button_width
                x = ease_in_out(
                    x=self.tick, start=centerx, stop=far_right, num=self.transition_length
                )
                for button in self.buttons:
                    button.x = x
            except IndexError:
                self.kill()

        return _animate_out
