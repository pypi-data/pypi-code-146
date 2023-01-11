import atexit
import os
import sys
from pathlib import Path

from inspector_commons.database import Database
from inspector_commons.telemetry import Telemetry


class Context:
    INSTANCES = {
        "manager": None,
        "browser": None,
        "image": None,
        "web-recorder": None,
        "windows": None,
    }

    def __init__(self, logger, config):
        #: Shared console/file logger
        self.logger = logger
        #: Application configuration
        self.config = config
        #: Created pywebview windows
        self.windows = []
        #: Telemetry client
        # TODO: create a property from telemetry, use ABC
        self.telemetry = Telemetry(debug=self.is_debug)
        #: Locators database
        self.database = Database(self.config.get("database", None))
        #: Currently selected locator (for editing)
        self.selected = None
        #: Active webdriver
        self.webdriver = None

        self.telemetry.start_worker()
        atexit.register(self._on_exit)

    def _on_exit(self):
        if self.webdriver is not None:
            self.webdriver.stop()

    @property
    def is_debug(self):
        return self.config.get("debug")

    @property
    def entrypoint(self):
        # note: pywebview uses sys.argv[0] as base
        base = Path(sys.argv[0]).resolve().parent
        static = Path(__file__).resolve().parent / "static"
        return os.path.relpath(str(static), str(base))

    def force_update(self):
        manager = self.INSTANCES["manager"]
        if manager is not None:
            manager.evaluate_js("window.pywebview.state.update()")

    def load_locator(self, name):
        try:
            with self.database.lock:
                self.database.load()
                return self.database.get(name)
        except KeyError:
            return None
