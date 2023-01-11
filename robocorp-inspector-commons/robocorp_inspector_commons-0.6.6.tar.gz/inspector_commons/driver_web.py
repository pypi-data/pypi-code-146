import base64
import logging
import os
import platform
import signal
import traceback
from pathlib import Path, WindowsPath
from typing import Dict, Union
from urllib.parse import urlparse

import psutil  # type: ignore
from RPA.core import webdriver  # type: ignore
from selenium.common.exceptions import (  # type: ignore
    InvalidSessionIdException,
    JavascriptException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ChromeOptions, Remote  # type: ignore
from selenium.webdriver.common.by import By


def load_resource(filename):
    path = Path(__file__).parent / "static" / "resources" / str(filename)
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def chrome_options():
    opts = ChromeOptions()

    preferences = {
        "safebrowsing.enabled": True,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }

    opts.add_argument("--no-sandbox")
    opts.add_argument("--allow-running-insecure-content")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-web-security")
    opts.add_experimental_option("prefs", preferences)
    opts.add_experimental_option(
        "excludeSwitches", ["enable-logging", "enable-automation"]
    )

    return opts


def friendly_name(element):
    tag = element.tag_name.lower()

    if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "a"):
        return element.text

    if tag == "img":
        alt = element.get_attribute("alt")
        if alt.strip():
            return alt

        url = element.get_attribute("src")
        name = os.path.basename(urlparse(url).path)
        if not url.startswith("data:image") and name.strip():
            return name

        return "Image"

    # TODO: Add div logic
    # TODO: Add input type and title logic

    # Human-friendly names for non-descriptive tags,
    # expand as necessary
    names = {
        # Navigation
        "nav": "Navigation",
        "input": "Input",
        # Text
        "b": "Bold",
        "i": "Italic",
        "br": "Line Break",
        "p": "Paragraph",
        "pre": "Preformatted Text",
        "samp": "Sample Text",
        # Lists
        "li": "List Item",
        "ol": "Ordered List",
        "ul": "Unordered List",
        # Tables
        "tbody": "Table Rows",
        "th": "Table Header",
        "thead": "Table Header",
        "tfoot": "Table Footer",
        "tr": "Table Row",
        "col": "Table Column",
        "td": "Table Cell",
        "hgroup": "Heading Group",
        "colgroup": "Column Group",
        # Misc
        "hr": "Horizontal Line",
    }

    if tag in names:
        return names[tag]

    return tag


class WebDriverError(Exception):
    """Common exception for all webdriver errors."""


class WebDriver:
    SCRIPT_TIMEOUT = 120.0  # seconds

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.selenium = None
        self.resources = {}
        self.is_remote = False
        self._load_resources()
        self._is_recording: bool = False

    @classmethod
    def from_remote(cls, executor_url, session_id, handle):
        # Override new session command to prevent spawning windows
        execute = Remote.execute

        def _execute_patched(self, driver_command, params=None):
            if driver_command == "newSession":
                return {"success": 0, "value": None, "sessionId": session_id}
            else:
                return execute(self, driver_command, params)

        try:
            Remote.execute = _execute_patched
            driver = Remote(
                command_executor=executor_url,
                desired_capabilities={},
            )
            driver.session_id = session_id
            driver.switch_to.window(handle)
        finally:
            Remote.execute = execute

        instance = cls()
        instance.selenium = driver
        instance.is_remote = True

        return instance

    @property
    def is_running(self):
        if not self.selenium:
            return False

        try:
            try:
                # Mock interaction to check if webdriver is still available
                _ = self.selenium.current_window_handle
            except NoSuchWindowException:
                # Handle tabs closed by user
                handles = self.selenium.window_handles
                self.selenium.switch_to_window(handles[-1])
            return True
        except Exception:  # pylint: disable=broad-except
            self.selenium = None
            return False

    @property
    def title(self):
        if not self.selenium:
            return None

        return self.selenium.title

    @property
    def url(self):
        if not self.selenium:
            return None

        return self.selenium.current_url

    def _load_resources(self):
        self.resources = {
            "style": load_resource("inspector.css"),
            "inspector": load_resource("inspector.js"),
            "inspect-guide": load_resource("guide.html"),
            "recording-guide": load_resource("browser-recording-guide.html"),
        }
        self.logger.debug("Resources loaded!")

    def _exec_resources(self):
        try:
            self.selenium.find_element(by=By.ID, value="inspector-style")
        except Exception as ex:  # pylint: disable=broad-except
            self.logger.debug("Inspector was not injected. Exception: %s", ex)
            self.logger.debug("Injecting resources to web page...")
            self.selenium.execute_script(self.resources["inspector"])
            self.logger.debug("[DONE] Inspector code injected!")
            self.selenium.execute_script(
                'var style = document.getElementById("inspector-style");'
                f'var content = document.createTextNode(`{self.resources["style"]}`);'
                "style.appendChild(content);"
            )
            self.logger.debug("[DONE] Inspector style injected!")
        else:
            self.logger.error(
                "Inspector already injected or did not manage to inject code!"
            )

    def _exec_driver(self, func, *args, **kwargs):
        def error(msg, *error_args):
            self.logger.warning(msg, error_args)
            raise WebDriverError(msg)

        if not self.selenium:
            error("No available webdriver")

        try:
            self._exec_resources()
            return func(*args, **kwargs)
        except TimeoutException:
            error("Timeout while running script")
        except JavascriptException as exc:
            error("Error while running script: %s", exc)
        except WebDriverError as exc:
            error("Webdriver error: %s", exc)
        except (InvalidSessionIdException, NoSuchWindowException) as exc:
            self.selenium = None
            error(exc)

    def _exec_script(self, script, *args, **kwargs):
        return self._exec_driver(self.selenium.execute_script, script, *args, **kwargs)

    def _exec_async_script(self, script, *args, **kwargs):
        return self._exec_driver(
            self.selenium.execute_async_script, script, *args, **kwargs
        )

    def _init_driver(self):  # noqa: C901
        browsers = webdriver.DRIVER_PREFERENCE[platform.system()]
        for browser in browsers:
            if browser == "Chrome":
                kwargs = {"chrome_options": chrome_options()}
            else:
                kwargs = {}

            def _create_driver(path=None):
                # pylint: disable=cell-var-from-loop
                if path is not None:
                    if isinstance(path, WindowsPath):
                        path = str(path.resolve())
                    return webdriver.start(browser, executable_path=path, **kwargs)
                else:
                    return webdriver.start(browser, **kwargs)

            try:
                # Try to download webdriver
                download = webdriver.download(browser)
                if download:
                    return _create_driver(download)

                # No webdriver required
                return _create_driver()
            except WebDriverException as exc:
                self.logger.warning("Failed to start '%s': %s", browser, exc)
            except Exception:  # pylint: disable=broad-except
                self.logger.error("Unhandled exception:\n%s", traceback.format_exc())

        raise ValueError("No valid browser found")

    def _to_finder(self, strategy):
        strategy = str(strategy).lower()
        finder = {
            "class": By.CLASS_NAME,
            "css": By.CSS_SELECTOR,
            "id": By.ID,
            "link": By.LINK_TEXT,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "xpath": By.XPATH,
        }[strategy]

        if not finder:
            raise ValueError(f"Unknown search strategy: {strategy}")

        return lambda val: self.selenium.find_elements(by=finder, value=val)

    def start(self):
        if self.selenium:
            self.logger.warning("Webdriver already running")

        self.logger.debug("Starting browser")
        self.selenium = self._init_driver()
        self.logger.debug("Selenium driver: %s", self.selenium)
        self.selenium.set_script_timeout(self.SCRIPT_TIMEOUT)

    def stop(self):
        self.logger.debug("Trying to stop driver...")
        if not self.selenium:
            self.logger.debug("Skipping close as no selenium present")
            return

        if self.is_remote:
            self.logger.debug("Skipping close for remote browser")
            return

        try:
            if not self._is_recording:
                self.logger.debug("[DEFAULT] Stopping browser")
                self.selenium.close()
                self.selenium.quit()
                self.logger.debug("[DEFAULT] Browser stopped!")
            else:
                self.logger.debug("[DEFAULT] Skipped normally stopping browser. ")

            if self.selenium:
                self.logger.debug(
                    "[FORCE] Stopping browser: %s", self.selenium.service.process.pid
                )
                browser_proc = psutil.Process(self.selenium.service.process.pid)
                for child in browser_proc.children(recursive=True):
                    try:
                        self.logger.debug("[FORCE] Stopping process: %s", child.pid)
                        os.kill(child.pid, signal.SIGTERM)
                        child.kill()
                        child.wait()
                    except Exception:  # pylint: disable=W0703
                        pass
                self.logger.debug("[FORCE] Browser stopped!")
            else:
                self.logger.debug("[FORCE] Skipped force stopping browser.")

        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an error while stopping driver: %s", ex)

        self.selenium = None

    def show_guide(self, guide_resources: str):
        guide = self.resources[guide_resources].encode("utf-8")
        payload = base64.b64encode(guide).decode("utf-8")
        self.selenium.get(f"data:text/html;base64,{payload}")

    def navigate(self, url):
        self.logger.debug("Navigating to: %s", url)
        self.selenium.get(url)

    def pick(self):
        def picker():
            locators = self.selenium.execute_async_script(
                "var callback = arguments[arguments.length - 1];"
                "Inspector.startPicker(callback);"
            )

            if not locators:
                return {}

            options = {}
            elements = set()
            for name, value in locators:
                strategy = name.split(":", 1)[0]
                finder = self._to_finder(strategy)
                matches = finder(value)

                if len(matches) == 1:
                    options[name] = {"strategy": strategy, "value": value}
                    elements.add(matches[0])

            if len(elements) > 1:
                # TODO: Inform user somehow? How to test?
                self.logger.error("Picker options matching multiple elements")

            return options

        self.logger.debug("Starting interactive picker")
        return self._exec_driver(picker)

    def find(self, strategy, value):
        self.logger.debug("Finding elements: %s:%s", strategy, value)
        finder = self._to_finder(strategy)
        return self._exec_driver(finder, value)

    def highlight(self, elements, hide=False):
        try:
            self.logger.debug(
                "Highlighting %d element(s)"
                if not hide
                else "Will NOT highlight %d element(s)",
                len(elements),
            )
            names = [friendly_name(element) for element in elements]
            highlights = "Inspector.highlightElements(elements);" if not hide else ""
            script = f"""
var callback = arguments[arguments.length - 1];
var elements = arguments[0];
var tags = Inspector.describeElements(elements);
{highlights}
callback(tags);
            """
            values = self._exec_async_script(
                script,
                elements,
            )
            return list(zip(names, values))
        except StaleElementReferenceException as exc:
            self.logger.warning(exc)
            return []

    def focus(self, element):
        try:
            self._exec_script(
                "var element = arguments[0]; Inspector.focusElement(element);",
                element,
            )
        except StaleElementReferenceException as exc:
            self.logger.warning(exc)

    def clear(self):
        self.logger.debug("Clearing highlights")
        return self._exec_script("Inspector.removeHighlights();")

    def cancel_pick(self):
        self.logger.debug("Canceling picking and clearing highlights")
        return self._exec_script("Inspector.cancelPick();")

    def record_event(self) -> Union[Dict, None]:
        try:
            self._is_recording = True
            self._exec_resources()

            result = self._exec_async_script(
                "var callback = arguments[arguments.length - 1];"
                "Inspector.recordEvent(callback);"
            )
            self.logger.debug(
                "Selenium execute async script finished, result: %s", result
            )
            self._is_recording = False
            return result
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an exception while recording event: %s", ex)
            return None

    def stop_recording(self) -> None:
        try:
            if self._is_recording:
                self._exec_async_script("Inspector.stopRecording();")
        except Exception as ex:  # pylint: disable=W0703
            self.logger.error("There was an exception while recording event: %s", ex)
        self._is_recording = False
