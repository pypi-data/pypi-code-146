import sys
from typing import List, Optional, Union

from selenium.common.exceptions import (  # type: ignore
    JavascriptException,
    TimeoutException,
)
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from typing_extensions import Literal, TypedDict

from inspector_commons.bridge.bridge_browser import BrowserBridge  # type: ignore
from inspector_commons.bridge.mixin import traceback  # type: ignore


class SelectorType(TypedDict):
    strategy: str
    value: str


class MatchType(TypedDict):
    name: str
    value: str


class Meta(TypedDict):
    source: str
    screenshot: str
    matches: List[MatchType]


class RecordedOperation(TypedDict):
    type: str
    value: Union[None, str, bool]
    path: Optional[str]
    time: Optional[int]
    trigger: Literal["click", "change", "unknown"]
    selectors: List[SelectorType]
    meta: Optional[List[Meta]]


class RecordEvent(TypedDict):
    list: List[RecordedOperation]
    actionType: Literal["exception", "stop", "append"]
    url: Optional[str]


class RecorderBridge(BrowserBridge):
    """Javascript API bridge for the web recorder functionality."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_url: Optional[str] = None
        self._recorded_operation: Union[RecordedOperation, None] = None

    @traceback
    def start_recording(self) -> Union[RecordedOperation, None]:
        self.logger.debug("Starting recording event...")
        self._record()
        self.logger.debug("Recorded event: %s", self._recorded_operation)
        return self._recorded_operation

    @traceback
    def stop_recording(self) -> Union[RecordedOperation, None]:
        self.web_driver.stop_recording()
        self.logger.debug("Recording should stop...")
        return self._recorded_operation

    @traceback
    def show_guide(self):
        self.web_driver.show_guide("recording-guide")

    def _record(self):
        for attempt_number in range(3):
            self.logger.debug("Recording attempt: %s", attempt_number)
            try:
                self._wait_for_page_to_load()
                event: RecordEvent = self.web_driver.record_event()
                self.logger.debug("Raw event: %s", event)
            except JavascriptException as exc:
                self.logger.debug("Ignoring Javascript exception: %s", exc)
                event: RecordEvent = {
                    "actionType": "exception",
                    "list": [],
                    "url": self._current_url,
                }
                continue
            except TimeoutException:
                self.logger.debug("Retrying after script timeout")
                event: RecordEvent = {
                    "actionType": "exception",
                    "list": [],
                    "url": self._current_url,
                }
                continue

            if not event:
                self.logger.error("Received empty event: %s", event)
                continue

            if self._handle_event(event):
                return
        self._handle_stop_event("force stop")

    def _handle_event(self, event: RecordEvent) -> bool:
        self._recorded_operation = None

        event_type = event["actionType"]
        event_url = event["url"]

        if not self._current_url:
            self._current_url = event_url
        elif event_url != self._current_url:
            message: RecordedOperation = {
                "path": None,
                "time": None,
                "meta": [],
                "selectors": [],
                "type": "comment",
                "value": f"Recorder detected that URL changed to {event_url}",
                "trigger": "unknown",
            }
            self._current_url = event_url
            self._recorded_operation = message

        if event_type == "exception":
            self.logger.debug("Event(s) is an exception: %s", event)
        elif event_type == "event":
            self.logger.debug("Received event(s) from page: %s", event["list"])
            self._recorded_operation = self._get_valid_ops(event=event)
        elif event_type == "stop":
            self._handle_stop_event(event_url=event_url)
        else:
            raise ValueError(f"Unknown event type: {event_type}")

        return True

    def _handle_stop_event(self, event_url):
        self.logger.debug("Received stop from page")
        message: RecordedOperation = {
            "path": None,
            "time": None,
            "meta": [],
            "selectors": [],
            "type": "command",
            "value": f"Received stop from: {event_url}",
            "trigger": "stop",
        }
        self.web_driver.stop_recording()
        self._recorded_operation = message

    def _get_valid_ops(self, event: RecordEvent):
        self.logger.debug("Valid operations: %s", event["list"])
        for operation in event["list"]:
            if "selectors" not in operation or len(operation["selectors"]) == 0:
                continue
            valid_selectors = []
            for selector in operation["selectors"]:
                self.logger.debug("Raw event selector: %s", selector)
                if selector is not None:
                    valid_selectors.append(selector)
            operation["selectors"] = valid_selectors
            if len(valid_selectors) > 0:
                return operation
        return None

    def set_window_height(self, height):
        self.logger.debug(
            "Content sizes: %s (height) x %s (width)",
            height,
            self.window.DEFAULTS["width"],
        )
        local_width = self.window.DEFAULTS["width"]
        local_width = local_width + 5 if sys.platform == "win32" else local_width
        local_height = height + 5 if sys.platform == "win32" else height
        self.logger.debug(
            "Setting the window to: %s (height) x %s (width)",
            local_height,
            local_width,
        )
        self.window.resize(local_width, local_height)

    def _wait_for_page_to_load(self):
        try:
            waiter = WebDriverWait(self.web_driver, 10)
            waiter.until(
                lambda x: x.selenium.execute_script("return document.readyState")
                == "complete"
            )
        except Exception as ex:  # pylint: disable=W0703
            self.logger.debug(
                "There was an exception while waiting for page to load: %s", ex
            )
