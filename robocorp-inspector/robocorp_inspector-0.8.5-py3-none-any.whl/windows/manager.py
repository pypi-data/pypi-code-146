from pathlib import Path
from typing import List
from enum import Enum

from inspector_commons.utils import IS_WINDOWS  # type: ignore
from inspector_commons.bridge.mixin import traceback  # type: ignore
from inspector.windows.base import Bridge, Window
from .web_recorder import WebRecorderWindow
from .browser import BrowserWindow
from .image import ImageWindow

IWW = None
try:
    from inspector.windows.windows import WindowsWindow

    IWW = WindowsWindow  # type: ignore
except Exception as exc:  # type: ignore # pylint: disable=broad-except, useless-suppression # noqa: E501
    print("Importing the WIN32 packages failed. Will continue. Exception: %s", exc)


class SupportedInstances(Enum):
    MANAGER = "manager"
    BROWSER = "browser"
    IMAGE = "image"
    WEBRECORDER = "web-recorder"
    WINDOWS = "windows"


class ManagerBridge(Bridge):
    """Javascript API bridge."""

    def path(self, length=32):
        # Return absolute path if short enough
        absolute = Path(self.ctx.database.path).resolve()
        if len(str(absolute)) <= length:
            return str(absolute)

        # Return partial path by removing parent directories
        parts = absolute.parts
        while parts:
            parts = parts[1:]
            shortened = str(Path("...", *parts))
            if len(shortened) <= length:
                return shortened

        # Return just filename or partial filename
        if len(absolute.name) > length:
            return "..." + absolute.name[-length:]
        else:
            return absolute.name

    def list(self):
        with self.ctx.database.lock:
            self.ctx.database.load()
            db_list = self.ctx.database.list()
            return db_list

    @traceback
    def rename(self, before, after):
        with self.ctx.database.lock:
            self.ctx.database.load()
            locator = self.ctx.database.pop(before)
            self.ctx.database.update(after, locator)

    @traceback
    def add(self, kind):
        self.ctx.selected = None
        self.ctx.create_window(kind, WINDOWS[kind])

    @traceback
    def edit(self, name):
        locator = self.ctx.load_locator(name)
        if not locator:
            self.logger.error("No locator with name: %s", name)
            return
        self.ctx.selected = name
        self.ctx.create_window(locator["type"], WINDOWS[locator["type"]])

    @traceback
    def remove(self, name):
        with self.ctx.database.lock:
            self.ctx.database.delete(name)

    @traceback
    def list_supported_locators(self) -> List[str]:  # pylint: disable=no-self-use
        if IS_WINDOWS:
            return [
                SupportedInstances.MANAGER.value,
                SupportedInstances.BROWSER.value,
                SupportedInstances.IMAGE.value,
                SupportedInstances.WEBRECORDER.value,
                SupportedInstances.WINDOWS.value,
            ]
        return [
            SupportedInstances.MANAGER.value,
            SupportedInstances.BROWSER.value,
            SupportedInstances.IMAGE.value,
            SupportedInstances.WEBRECORDER.value,
        ]


class ManagerWindow(Window):
    BRIDGE = ManagerBridge
    DEFAULTS = {
        "title": "Robocorp Inspector Manager",
        "url": "manager.html",
        "width": 450,
        "height": 900,
    }


WINDOWS = {
    "browser": BrowserWindow,
    "image": ImageWindow,
    "manager": ManagerWindow,
    "web-recorder": WebRecorderWindow,
    "windows": IWW,
}
