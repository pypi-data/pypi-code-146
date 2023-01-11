from inspector_commons.bridge.bridge_recorder import RecorderBridge  # type: ignore
from inspector.windows.browser import BrowserWindow


class WebRecorderWindow(BrowserWindow):
    BRIDGE = RecorderBridge
    DEFAULTS = {
        "title": "Robocorp - Web Recorder",
        "url": "webrecorder.html",
        "width": 480,
        "height": 0,
        "on_top": True,
    }
