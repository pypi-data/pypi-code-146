from typing import Callable

import pygame
from pygame import Color
from pygame.rect import Rect

from robingame.objects import PhysicalEntity
from robingame.utils import pulsing_value


class Button(PhysicalEntity):
    """
    GUI button entity. Reacts to changes in the is_focused and is_pressed booleans, but doesn't
    set them (a parent menu class or something else should set them). This is so that each Button
    doesn't have to do its own input detection. It also allows a parent menu class to take into
    account additional context e.g. shifting focus from one button to another using a keyboard or
    joystick input. Operations like this would be beyond the scope of a single Button instance.
    """

    is_focused: bool  # does the button have focus? (e.g. mouse hovering over)
    is_pressed: bool  # is the button down right now
    font_name = "ubuntu"
    font_size = 20
    text_color: Color

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text=None,
        on_press=None,
        on_focus=None,
        on_release=None,
        on_unfocus=None,
    ):
        self.width = width
        self.height = height
        self.text = text
        self.rect = Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.is_focused = False
        self.is_pressed = False
        self._on_press = on_press or (lambda button: None)
        self._on_focus = on_focus or (lambda button: None)
        self._on_release = on_release or (lambda button: None)
        self._on_unfocus = on_unfocus or (lambda button: None)
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        self.state = self.state_idle
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(Color("red"))
        if self.text:
            text = self.font.render(self.text, True, Color("black"))
            textRect = text.get_rect()
            textRect.center = self.image.get_rect().center
            self.image.blit(text, textRect)
        super().__init__()

    # =============================================================================================
    # state functions handle behaviour that happens *every tick* the button is in that state
    # =============================================================================================
    def state_idle(self):
        if self.is_focused:
            self.focus()
        if self.is_pressed:
            self.press()

    def state_focus(self):
        if not self.is_focused:
            self.unfocus()
        if self.is_pressed:
            self.press()

    def state_press(self):
        if not self.is_pressed:
            self.release()

    # =============================================================================================
    # on_* functions handle behaviour that happens *once* at the transition to a new state.
    # By default they just call the hook passed in by the button creator, but Button
    # subclasses can also extend the method to add additional custom behaviour. External effects
    # (e.g. incrementing some value stored in a parent class) should be handled by the hook.
    # Internal effects (i.e. those that require access to the button instance) should be handled
    # by an overridden method on a subclass. A mix of both (e.g. adding particles to the parent
    # class at the button's position) could be solved using an Event.
    # =============================================================================================

    def on_press(self):
        self._on_press(self)

    def on_release(self):
        self._on_release(self)

    def on_focus(self):
        self._on_focus(self)

    def on_unfocus(self):
        self._on_unfocus(self)

    # =============================================================================================
    # courtesy methods to make switching states easy
    # =============================================================================================

    def press(self):
        self.on_press()
        self.state = self.state_press

    def focus(self):
        self.on_focus()
        self.state = self.state_focus

    def release(self):
        self.on_release()
        self.state = self.state_focus if self.is_focused else self.state_idle

    def unfocus(self):
        self.on_unfocus()
        self.state = self.state_idle


class ColoredButton(Button):
    idle_color = (100, 0, 100)  # Color("purple")
    focus_color = Color("orange")
    press_color = Color("red")
    text_color = Color("white")

    def state_idle(self):
        super().state_idle()
        self.color = (pulsing_value(self.tick, 80, 150, 0.03), 30, 75)

    def state_focus(self):
        super().state_focus()
        self.color = (
            pulsing_value(self.tick, 180, 255, 0.3),
            pulsing_value(self.tick, 100, 163, 0.3),
            0,
        )

    def state_press(self):
        super().state_press()
        self.color = self.press_color
