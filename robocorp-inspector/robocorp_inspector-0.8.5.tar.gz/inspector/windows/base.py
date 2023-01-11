import os
from abc import ABC
from enum import Enum, auto

import webview  # type: ignore

from inspector_commons.bridge.base import Bridge  # type: ignore


APP_WINDOW_TITLE = "UI Inspector"


class WindowState(Enum):
    CREATED = auto()
    SHOWN = auto()
    LOADED = auto()
    CLOSING = auto()
    CLOSED = auto()


class Window(ABC):
    BRIDGE = Bridge
    DEFAULTS = {
        "title": "Title",
        "url": "index.html",
        "width": 640,
        "height": 480,
    }

    @classmethod
    def create(cls, context, **kwargs):
        options = dict(cls.DEFAULTS)
        options.update(kwargs)
        options.setdefault("title", APP_WINDOW_TITLE)

        context.logger.info("Window Context: %s", context)
        context.logger.info("Entrypoint: %s", context.entrypoint)
        options["url"] = os.path.join(context.entrypoint, options["url"])

        context.logger.info("Options: %s", options)
        bridge = cls.BRIDGE(context)
        window = webview.create_window(
            js_api=bridge,
            resizable=False,
            **options,
        )
        instance = cls(context, window, bridge)
        bridge.set_window(instance)

        context.logger.info("Window Created: %s", window)
        return instance

    def __init__(self, context, window, bridge):
        self._context = context
        self._window = window
        self._bridge = bridge
        self._state = WindowState.CREATED

        # Attach event callbacks
        self._window.events.closed += self.on_closed
        self._window.events.closing += self.on_closing
        self._window.events.shown += self.on_shown
        self._window.events.loaded += self.on_loaded

        # MacOS closing flag
        self._force_closing = False

    def __getattr__(self, name):
        return getattr(self._window, name)

    @property
    def logger(self):
        return self._context.logger

    @property
    def state(self):
        return self._state

    @property
    def is_valid(self):
        return self.state not in (WindowState.CLOSING, WindowState.CLOSED)

    def on_shown(self):
        self.logger.debug("Window shown")
        self._state = WindowState.SHOWN

    def on_loaded(self):
        self.logger.debug("Window loaded")
        self._state = WindowState.LOADED

    def on_closing(self):
        self.logger.debug("Window closing")
        self._state = WindowState.CLOSING

    def on_closed(self):
        self.logger.debug("Window closed")
        self._state = WindowState.CLOSED

    def save(self, name, locator):
        self.logger.debug("Saving Locator: %s - %s", name, locator)
