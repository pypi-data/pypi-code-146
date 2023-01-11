import json
import subprocess
import sys
import time
from pathlib import Path

from inspector_commons.bridge.mixin import DatabaseMixin, traceback  # type: ignore

from inspector.windows.base import Bridge, Window


def _base64_to_image(img):
    # pylint: disable=import-outside-toplevel
    from RPA.recognition import base64_to_image  # type: ignore

    return base64_to_image(img)


class ImageBridge(DatabaseMixin, Bridge):
    """Javascript API bridge for image template locators."""

    @traceback
    def pick(self, confidence=None):
        self.logger.info("Starting interactive picker")
        cmd = [
            sys.executable,
            str(Path(__file__).parent / ".." / "snipping_tool.py"),
        ]

        stdout = subprocess.check_output(cmd)
        if not stdout:
            raise RuntimeError("Picker closed abruptly")

        try:
            result = json.loads(stdout)
        except ValueError as err:
            raise RuntimeError(f"Malformed response from picker: {err}") from err

        if "error" in result:
            raise RuntimeError(result["error"])

        needle = _base64_to_image(result["image"])

        # TODO: No matches found if matching immediately, possibly
        # related to snipping tool closing.
        time.sleep(0.5)
        matches = self._find_matches(needle, confidence)

        return {"image": result["image"], "matches": [str(m) for m in matches]}

    @traceback
    def validate(
        self,
        value,
        confidence=None,
    ):
        needle = _base64_to_image(value)
        matches = self._find_matches(needle, confidence)

        # TODO: Replace with screenshots of matches?
        return {"matches": [str(m) for m in matches]}

    def _find_matches(self, needle, confidence=None):
        # pylint: disable=import-outside-toplevel
        import mss  # type: ignore
        from PIL import Image  # type: ignore
        from RPA.recognition import templates  # type: ignore
        from RPA.recognition.templates import (  # type: ignore
            ImageNotFoundError,
            DEFAULT_CONFIDENCE,
        )

        if confidence is None:
            confidence = DEFAULT_CONFIDENCE

        with mss.mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)
            haystack = Image.frombytes(
                "RGB", screenshot.size, screenshot.bgra, "raw", "BGRX"
            )

        try:
            self.logger.info("Finding template matches (confidence: %s)", confidence)
            matches = templates.find(haystack, needle, confidence=confidence)
        except ImageNotFoundError as err:
            self.logger.debug(str(err))
            matches = []

        self.logger.info(
            "Found %d match%s", len(matches), "" if len(matches) == 1 else "es"
        )

        return matches

    @traceback
    def minimize(self):
        self.logger.debug("Minimizing windows")
        for window in reversed(self.ctx.windows):
            if window.is_valid:
                window.minimize()

    @traceback
    def restore(self):
        self.logger.debug("Restoring windows")
        for window in self.ctx.windows:
            if window.is_valid:
                window.restore()


class ImageWindow(Window):
    BRIDGE = ImageBridge
    DEFAULTS = {
        "title": "Robocorp - Image Locators",
        "url": "image.html",
        "width": 560,
        "height": 720,
    }
