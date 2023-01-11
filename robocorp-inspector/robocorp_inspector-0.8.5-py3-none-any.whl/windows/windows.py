from inspector_commons.bridge.bridge_windows import WindowsBridge  # type: ignore
from inspector.windows.base import Window


class WindowsWindow(Window):
    BRIDGE = WindowsBridge
    DEFAULTS = {
        "title": "Robocorp - Windows Application Locators",
        "url": "windows.html",
        "width": 560,
        "height": 0,
        "on_top": True,
    }
