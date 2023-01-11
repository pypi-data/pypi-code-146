import base64
import logging
from dataclasses import dataclass
from io import BytesIO
from queue import Empty, Queue
from typing import Dict, List, Optional, Tuple, Union

try:
    import uiautomation as auto  # type: ignore # pylint: disable=import-error, useless-suppression # noqa: E501
    import win32api  # type: ignore # pylint: disable=import-error, useless-suppression
    import win32gui  # type: ignore # pylint: disable=import-error, useless-suppression
    from PIL import ImageGrab  # type: ignore
    from pynput_robocorp.mouse import (  # type: ignore # pylint: disable=import-error, useless-suppression # noqa: E501
        Listener,
    )
    from RPA.core.windows import (  # type: ignore
        ElementInspector,
        RecordElement,
        WindowsElements,
    )
    from RPA.core.windows.context import ElementNotFound  # type: ignore
except Exception as exc:  # type: ignore # pylint: disable=broad-except, useless-suppression # noqa: E501
    print("Importing the WIN32 packages failed. Will continue. Exception: %s", exc)

from RPA.core.geometry import Region  # type: ignore

LOCATOR_VERSION = 1.0

PICK_TIMEOUT = 120

WindowsLocatorProperties = Dict[str, str]
WindowsLocator = Dict[str, WindowsLocatorProperties]
MatchedWindowsLocator = Dict[str, Union[str, float]]
MatchedWindowsLocators = Dict[str, List[MatchedWindowsLocator]]
OpenWindow = Dict[str, str]
OpenWindows = List[OpenWindow]


@dataclass
class Rectangle(Region):
    @classmethod
    def from_element(cls, element):
        left = int(element.xcenter - (element.width / 2))
        right = int(element.xcenter + (element.width / 2))
        bottom = int(element.ycenter + (element.height / 2))
        top = int(element.ycenter - (element.height / 2))
        return cls(left, top, right, bottom)

    @classmethod
    def from_control(cls, control):
        left = int(control.BoundingRectangle.left)
        top = int(control.BoundingRectangle.top)
        right = int(control.BoundingRectangle.right)
        bottom = int(control.BoundingRectangle.bottom)
        return cls(left, top, right, bottom)

    def get_screenshot(self) -> str:
        image = ImageGrab.grab(self.as_tuple())
        jpeg_image_buffer = BytesIO()
        image.save(jpeg_image_buffer, format="JPEG")
        return base64.b64encode(jpeg_image_buffer.getvalue()).decode("utf-8")

    def get_borders(self, thickness: int) -> List[Tuple[int, int, int, int]]:
        """Get one pixel rectangles as tuples from rectangle coordinates"""
        rect = self.as_tuple()
        return [
            (rect[0] + i, rect[1] + i, rect[2] - i, rect[3] - i)
            for i in range(thickness)
        ]


class WindowMismatch(Exception):
    pass


class WindowsDriver:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._windows_elements = WindowsElements()
        self._active_window = ""
        self.queue = Queue()

    def _construct_locator(
        self,
        element,
    ) -> List[WindowsLocator]:
        properties_list = []
        locator_path: str = element["locator"]
        control: auto.Control = element["control"]
        window_name: str = element["top"]
        if window_name != self._active_window:
            raise WindowMismatch("Non active window clicked")

        name = control.Name or "WindowsLocator"

        locator_paths = [
            part
            for part in locator_path.split(" and ")
            for prop in ["name:", "id:"]
            if part.lower().startswith(prop)
        ]

        for loc in locator_paths:
            properties = {
                "window": self._active_window,
                "strategy": "WindowsLocator",
                "value": loc,
                "version": LOCATOR_VERSION,
                "name": name,
                "type": "windows",
                "kind": "locator",
            }

            self.logger.info("Add properties to list=%s", properties)

            if hasattr(control, "BoundingRectangle"):
                try:
                    properties["screenshot"] = Rectangle.from_control(
                        control
                    ).get_screenshot()
                except AttributeError as err:
                    self.logger.error("Failed to get locator screenshot=%r", err)
            properties_list.append(properties)
        return properties_list

    def _on_click(
        self,
        x_coord: int,
        y_coord: int,
        mouse_button,
        pressed: bool,
    ) -> None:
        self.logger.debug(
            "Element clicked (%s) with button=%s at=%s,%s",
            pressed,
            mouse_button,
            x_coord,
            y_coord,
        )

        try:
            elements: List[RecordElement] = []
            ElementInspector.inspect_element(
                action="", recording=elements, verbose=True
            )
            locators = self._construct_locator(elements[0])
        except (ValueError, IndexError) as err:
            self.logger.error(err)
            return
        except WindowMismatch as err:
            self.logger.error(err)
            return
        self.queue.put(locators, block=False, timeout=PICK_TIMEOUT)

    @classmethod
    def _find_all_top_level_window(cls) -> List:
        return auto.GetRootControl().GetChildren()

    def _focus_active_window(self, active_window: str) -> None:
        self._active_window = active_window
        windows = self._find_all_top_level_window()
        for window in windows:
            if hasattr(window, "Name") and window.Name == self._active_window:
                if hasattr(window, "SwitchToThisWindow"):
                    window.SwitchToThisWindow()
                if hasattr(window, "SetFocus"):
                    window.SetFocus()
                break
        else:
            self.logger.error("Could not focus window=%s", active_window)

    def get_window_control(self, window: str) -> Optional[auto.Control]:
        windows = self._find_all_top_level_window()
        for win in windows:
            if hasattr(win, "Name") and win.Name == window:
                return win
        self.logger.error("Could not get window=%s", window)
        return None

    def listen(self, active_window: str) -> List[WindowsLocator]:
        with auto.UIAutomationInitializerInThread(debug=True):
            self.logger.info(
                "Start listening for mouse click in window=%s", active_window
            )
            self._focus_active_window(active_window)
            locators: List[WindowsLocator] = []
            listener = Listener(on_click=self._on_click)
            try:
                listener.start()
                locators = self.queue.get(block=True, timeout=PICK_TIMEOUT)
            except Empty:
                self.logger.info("Locator selection timeout")
            finally:
                listener.stop()
        return locators

    def validate(self, window: str, value: str) -> MatchedWindowsLocators:
        self.logger.info("Validate=%s, %s", window, value)
        locators: MatchedWindowsLocators = {"matches": []}
        try:
            with auto.UIAutomationInitializerInThread(debug=True):
                self._focus_active_window(window)
                root = self._windows_elements.get_element(f"name:{window}")
                element = self._windows_elements.get_element(value, 8, root)
                if element and hasattr(element, "name") and hasattr(element, "locator"):
                    locators["matches"].append(
                        {
                            "window": window,
                            "name": element.name,
                            "value": element.locator,
                            "version": LOCATOR_VERSION,
                            "screenshot": Rectangle.from_element(
                                element
                            ).get_screenshot(),
                        }
                    )
        except ElementNotFound as err:
            self.logger.error("Could not validate locator=%s", err)
        return locators

    def list_windows(self, exclude_titles=None) -> OpenWindows:
        self.logger.info("Get window info")
        with auto.UIAutomationInitializerInThread(debug=True):
            exclude_titles = exclude_titles or []
            windows = []
            try:
                windows = self._windows_elements.list_windows(icons=True)
            except (TypeError, ElementNotFound) as err:
                # If windows is closed while listing the windows library
                # will raise an exception.
                # The fix need to be done in the windows library side,
                # but will add this catch here until the fix is done
                self.logger.error("Failed to list windows: %s", str(err))
            returned_windows = []
            for window in windows:
                win = {"title": window["title"]}
                if window["icon"]:
                    win["icon"] = window["icon"]
                if win["title"] and win["title"] not in exclude_titles:
                    returned_windows.append(win)
        return returned_windows

    def _draw_borders(
        self, rect: Rectangle, color, thickness: int = 5
    ):  # pylint: disable=c-extension-no-member, useless-suppression
        try:
            full_screen_context = win32gui.GetDC(0)
            brush = win32gui.CreateSolidBrush(color)
            win32gui.SelectObject(full_screen_context, brush)
            frames = rect.get_borders(thickness)
            for frame in frames:
                win32gui.FrameRect(full_screen_context, frame, brush)
        except AttributeError as error:
            self.logger.error("Could not draw border=%s", error)

    def focus(self, window: str, locator: str) -> None:
        self.logger.info("Focus element=%s in window=%s", locator, window)
        element_found = False
        col_red = (
            win32api.RGB(  # pylint: disable=c-extension-no-member, useless-suppression
                255, 0, 0
            )
        )
        try:
            with auto.UIAutomationInitializerInThread(debug=True):
                self._focus_active_window(window)
                root = self._windows_elements.get_element(f"name:{window}")
                element = self._windows_elements.get_element(locator, 8, root)
                rect = Rectangle.from_element(element)

                self._draw_borders(rect, col_red)
                element_found = True
        except ElementNotFound as err:
            self.logger.error("Could not focus on locator=%s with err=%s", locator, err)
        if not element_found:
            raise ElementNotFound(f"Could not focus on locator: {locator}")
