from inspector_commons.bridge.bridge_browser import BrowserBridge  # type: ignore
from inspector.windows.base import Window


class BrowserWindow(Window):
    BRIDGE = BrowserBridge
    DEFAULTS = {
        "title": "Robocorp - Web Locators",
        "url": "browser.html",
        "width": 480,
        "height": 0,
        "on_top": True,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._force_closing = False

    def on_closing(self):
        super().on_closing()

        driver = self._context.webdriver
        if driver is not None and driver.is_running:
            try:
                driver.stop()
            except Exception as exc:  # pylint: disable=broad-except
                self.logger.debug("Failed to clear webdriver: %s", exc)

        return True
