import logging
import os
import signal
import sys
import webview  # type: ignore
import psutil  # type: ignore

from inspector_commons.metric import MetricStart  # type: ignore
from inspector.windows.context import Context
from inspector.windows import WINDOWS

PYWEBVIEW_GUI = ["qt", "gtk", "cef", "mshtml", "edgechromium", "edgehtml"]


class App:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.ctx = Context(self.logger, config)
        self.process = None

    def start(self, root="manager"):
        assert len(self.ctx.windows) == 0, "Application already running"
        self.logger.info("Window will open for: %s", root)

        self.ctx.database.load()
        if self.ctx.database.error:
            self.logger.warning(*self.ctx.database.error)

        factory = WINDOWS.get(root)
        root = self.ctx.create_window(kind=root, factory=factory)
        root.closed += self.stop

        self.ctx.telemetry.send(MetricStart())

        webview.start(self._on_start, debug=self.ctx.is_debug)

    def stop(self):
        # kill all processes as chromedriver hangs
        self._kill_all_child_processes()
        # force exit application as there is nothing to worry about
        # and child processes hang
        os._exit(0)  # pylint: disable=protected-access

    def open(self, kind):
        self.start(kind)

    def edit(self, name):
        locator = self.ctx.load_locator(name)

        if locator is None:
            names = "\n".join(f" - {name}" for name in self.ctx.database.names)
            if names:
                self.logger.info("No locator with name: %s\n", name)
                self.logger.info("Possible options: %s\n", names)
            else:
                self.logger.error("No locators in database")
            sys.exit(1)

        self.ctx.selected = name
        self.start(locator["type"])

    def _on_start(self):
        self.logger.info("Starting root window...")
        if self.ctx.is_debug:
            # Print URL for automation
            root = self.ctx.windows[0]
            self.logger.info(root.get_current_url())

    def _kill_all_child_processes(self):
        self.logger.debug("Stopping all child processes...")
        for child in psutil.Process().children(recursive=True):
            try:
                self.logger.debug("Stopping PROCESS: %s", child.pid)
                os.kill(child.pid, signal.SIGTERM)
                child.kill()
                child.wait()
            except Exception:
                pass
