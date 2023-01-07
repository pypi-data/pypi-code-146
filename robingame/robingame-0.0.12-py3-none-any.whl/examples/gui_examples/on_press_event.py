from dataclasses import dataclass

import pygame.mouse

from robingame.gui.button import Button
from robingame.input import EventQueue
from robingame.objects import Game, Group
from robingame.utils import mouse_hovering_over


class OnPressEventExample(Game):
    """
    This is an example where the hooks increment/decrement a value stored on the outer Game class.
    """

    screen_color = (50, 50, 50)

    def __init__(self):
        super().__init__()
        self.value = 0
        self.buttons = Group()
        self.particles = Group()
        self.child_groups += [self.buttons, self.particles]
        self.buttons.add(
            Button(
                x=200,
                y=100,
                width=200,
                height=50,
                text="change value",
                on_press=lambda button: EventQueue.add(ChangeValue(amount=5)),
                on_release=lambda button: EventQueue.add(ChangeValue(amount=-5)),
                on_focus=lambda button: EventQueue.add(ChangeValue(amount=1)),
                on_unfocus=lambda button: EventQueue.add(ChangeValue(amount=-1)),
            )
        )

    def update(self):
        super().update()

        # listen for events
        if event := EventQueue.get(type=ChangeValue.type):
            self.value += event.amount
        print(f"{self.value=}")

        # button manager stuff
        for button in self.buttons:
            if mouse_hovering_over(button):
                button.is_focused = True
                button.is_pressed = pygame.mouse.get_pressed()[0]
            else:
                button.is_focused = False
                button.is_pressed = False


@dataclass
class ChangeValue:
    type = pygame.event.custom_type()
    amount: int = 1


if __name__ == "__main__":
    OnPressEventExample().main()
