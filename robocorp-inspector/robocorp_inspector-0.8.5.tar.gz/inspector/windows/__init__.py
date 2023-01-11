from inspector_commons.utils import IS_WINDOWS  # type: ignore
from .web_recorder import WebRecorderWindow
from .base import WindowState
from .browser import BrowserWindow
from .manager import ManagerWindow
from .image import ImageWindow

WINDOWS = {
    "browser": BrowserWindow,
    "image": ImageWindow,
    "manager": ManagerWindow,
    "web-recorder": WebRecorderWindow,
}

if IS_WINDOWS:
    from .windows import WindowsWindow

    WINDOWS["windows"] = WindowsWindow
