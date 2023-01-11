import os
import sys
from pathlib import Path

from inspector_commons.context import Context as CommonContext  # type: ignore
from inspector_commons.utils import IS_WINDOWS  # type: ignore

from inspector.windows.base import WindowState  # type: ignore


class Context(CommonContext):
    def create_window(self, kind, factory, **kwargs):
        if kind == "windows" and not IS_WINDOWS:
            raise NotImplementedError(
                "Windows locators are not available on non Windows platforms"
            )

        self.logger.debug("Factory Window type: %s", factory)
        if factory is None:
            raise KeyError(f"Unknown window type: {kind}")

        self.logger.debug("Created instances: %s", self.INSTANCES)
        window = self.INSTANCES[kind]
        if window is not None and window.is_valid:
            self.logger.debug("Restoring window...")
            window.restore()
            return window

        window = factory.create(self, **kwargs)
        self.INSTANCES[kind] = window
        self.logger.debug("Instances: %s", self.INSTANCES)
        self.logger.debug("Created window: %s", window)

        self.windows.append(window)
        return window

    def close_windows(self):
        self.logger.debug("Closing windows: %s", self.windows)
        for window in reversed(self.windows):
            if window.state != WindowState.CLOSED:
                self.logger.debug("Destroying window: %s", window.uid)
                window.destroy()
            else:
                self.logger.debug("Window already closed: %s", window.uid)

    # NOTE: need to overwrite the entrypoint as the Paths from the package
    # will refer to the package itself
    @property
    def entrypoint(self):
        # NOTE: pywebview uses sys.argv[0] as base
        base = Path(sys.argv[0]).resolve().parent
        static = Path(__file__).resolve().parent.parent / "static"
        return os.path.relpath(str(static), str(base))
