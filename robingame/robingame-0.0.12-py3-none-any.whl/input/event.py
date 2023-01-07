from dataclasses import dataclass, is_dataclass, asdict
from typing import Union

import pygame
from pygame.event import EventType, Event

from robingame.image import init_display

init_display()


class EventQueue:
    """Pygame's pygame.event.get() gets the events in the queue, but also empties the queue. This
    class solves that"""

    # this is intentional. I want to store the events on the class. Only one game will be active
    # at once, so we'll never need more than one instance of this class.
    events = []

    @classmethod
    def add(cls, event: Union[EventType, "dataclass"]):
        """
        Add the event to pygame's event queue, where it will stay until the .update() method
        is called to load it into cls.events.

        This prevents race conditions / order dependency where an event is added to the event
        queue and processed in the same tick.
        """
        if is_dataclass(event):
            event = Event(event.type, **asdict(event))
        pygame.event.post(event)

    @classmethod
    def update(cls):
        """
        Read all the events from pygame's event queue into cls.events
        (also clears pygame's event queue)
        """
        cls.events = pygame.event.get()

    @classmethod
    def filter(cls, **kwargs):
        return [
            event
            for event in cls.events
            if all(getattr(event, attribute, None) == value for attribute, value in kwargs.items())
        ]

    @classmethod
    def get(cls, **kwargs):
        try:
            return cls.filter(**kwargs)[0]
        except IndexError:
            return None
