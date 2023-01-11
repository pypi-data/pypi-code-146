# pylint: disable=import-error
""""thatscraper's module to handle actions via Selenium's webdriver"""

import os
import sys

# import polling2
from typing import Union
from typing import Callable
from selenium import webdriver

# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

# error handling
# from selenium.common.exceptions import NoSuchElementException

# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from .data import Cleaner
from .common.logger import log
from .common.exceptions import CrawlerError


# typing
WebElement = webdriver.remote.webelement.WebElement
WebElements = list[WebElement]
WebDriver = Union[webdriver.Firefox, webdriver.Chrome, webdriver.Safari, webdriver.Edge]
Number = Union[float, int]


# lower casing
class Key(Keys):  # pylint: disable=too-few-public-methods
    """ "keys to use in send functions"""

    enter = Keys.RETURN
    esc = Keys.ESCAPE
    delete = Keys.DELETE
    down = Keys.ARROW_DOWN
    up = Keys.ARROW_UP
    tab = Keys.TAB
    backspace = Keys.BACK_SPACE


# to run scripts
def document_query_selector(selector: str):
    """ "String to parse javascript code."""
    return f'document.querySelector("{selector}")'


# used in arguments of WeElement selectors
ATTR_SELECTOR = {
    "id": By.ID,
    "name": By.NAME,
    "xpath": By.XPATH,
    "tag name": By.TAG_NAME,
    "link text": By.LINK_TEXT,
    "class name": By.CLASS_NAME,
    "css selector": By.CSS_SELECTOR,
    "partial link text": By.PARTIAL_LINK_TEXT,
}

# wedrivers suported by selenium
# see https://selenium-python.readthedocs.io/installation.html#drivers
webdrivers = {
    "firefox": {
        "webdriver": webdriver.Firefox,
        "options": webdriver.firefox.options.Options(),
        # "profile": firefox_profile,
        "url": "https://github.com/mozilla/geckodriver/releases",
    },
    "chrome": {
        "webdriver": webdriver.Chrome,
        "options": webdriver.chrome.options.Options(),
        "url": "https://chromedriver.chromium.org/downloads",
    },
    "safari": {
        "driver": webdriver.Safari,
        "options": webdriver.safari.options.Options(),
        "url": "https://webkit.org/blog/6900/webdriver-support-in-safari-10/",
    },
    "edge": {
        "driver": webdriver.Edge,
        "options": webdriver.edge.options.Options(),
        "url": "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/",  # noqa E501
    },
}


class Crawler:  # pylint: disable=too-many-public-methods
    """
     A selenium.webdriver adapter.

    An instance of Window calss cam perform a series of automated
    actions on webpages. Designed to handle sites with heavy use of
    javascript.
    """

    def __init__(
        self,
        browser: str = "firefox",
        headless: bool = False,
        quit_on_failure: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        browser : str, optional
            Browser of you webdriver, by default 'firefox'
        headless : bool, optional
            If True, driver will work without the
            GUI's browser, by default False
        """
        if browser not in webdrivers:
            message = f"Unsuported browser '{browser}'."
            message += " List of suported ones: "
            message += ", ".join(list(webdrivers.keys())) + "."
            raise CrawlerError(message)
        self.__browser = browser
        self.__driver = None
        self.__options = None
        self.__logger = log(self.__class__.__name__)
        self.timeout = 50
        self.quit_on_failure = quit_on_failure
        try:
            self.__options = webdrivers[browser]["options"]
            self.__download_dir(os.getcwd())
            if headless:
                self.__options.headless = True
            driver = webdrivers[browser]["webdriver"]
            self.__driver = driver(options=self.__options)
        except WebDriverException as err:
            message = "You need to add the driver"
            message += f" for {browser} to your environment variables."
            message += f" You can download {browser}'s driver at: "
            message += webdrivers[browser]["url"]
            message += ". See more in"
            message += " https://selenium-python.readthedocs.io/"
            message += "installation.html#drivers"
            self.logger.error(str(err))
            self.logger.error(message)
            sys.exit(1)

    def quitdriver(method: Callable) -> Callable:  # pylint: disable=E0213
        """ "safe quit webdriver to avoid memory leakages"""
        def inner(self, *args, **kwargs) -> Callable:
            try:
                # pylint: disable=not-callable
                return method(self, *args, **kwargs)
            except Exception as err:
                # which is better? 1 or 2
                # traceback.print_exc()  # 1
                # print(err)
                if self.quit_on_failure:
                    print("quitting driver...")
                    self.quit()
                raise err  # 2

        return inner

    def __download_dir(self, path):
        if self.__browser == "firefox":
            self.__options.set_preference("browser.download.folderList", 2)
            self.__options.set_preference("browser.download.dir", rf"{path}")
        elif self.__browser == "chrome":
            self.__options.add_experimental_option(
                "prefs", {"download.default_directory": rf"{path}"}
            )

    @property
    def driver(
        self,
    ):
        """ "selenium webdriver"""
        return self.__driver

    @property
    def logger(
        self,
    ):
        """logger"""
        return self.__logger

    @quitdriver
    def goto(self, url: str):
        """open window at url"""
        self.driver.get(url)
        return self

    @quitdriver
    def half_left_window(
        self,
    ):
        """
        half_left_window

        Resize and shifts window to the left.
        """
        self.driver.set_window_rect(x=0, y=0, width=960, height=960)

    @quitdriver
    def element(self, value: str, by_attribue: str = "id") -> list:
        """
        element method.

        Selects an element by type of attribute defined with 'by',
        with 'value', from current page. See `thatscraper.ATTR_SELECTOR`
        for a list of attributes types.

        If elements are na availiable yet,
        the there will be an attempt every 'step' seconds, unitl excceed the
        total time 'timeout' (in seconds).

        Parameters
        ----------
        value : str
            attribute's value
        by_attribute : str, optional
            attribute type., by default "id"

        Returns
        -------
        WebElement
            Element retrieved.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        element = wait.until(
            EC.presence_of_element_located((ATTR_SELECTOR[by_attribue], value))
        )
        return element

    @quitdriver
    def element_id(self, value: str) -> WebElement:
        """
        element_id

        Retrieve element from current page by it's id value.

        Parameters
        ----------
        value : str
            id's value.

        Returns
        -------
        WebElement
            Element retrieved.
        """
        return self.element(value, "id")

    @quitdriver
    def elements(self, value: str, by_attribute: str = "id") -> WebElements:
        """
        elements

        Selects elements by type of attribute defined with 'by',
        with 'value', from current page. See `thatscraper.ATTR_SELECTOR`
        for a list of attributes names.

        If elements are na availiable yet,
        the there will be an attempt every 'step' seconds, unitl excceed the
        total time 'timeout' (in seconds).

        Parameters
        ----------
        value : str
            attribute's value
        by_attribute : str, optional
            attribute type, by default "id"

        Returns
        -------
        WebElements
            List with all elements selected.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        elements = wait.until(
            EC.presence_of_all_elements_located((ATTR_SELECTOR[by_attribute], value))
        )
        return elements

    @quitdriver
    def child_of(
        self, element: WebDriver, value: str, by_attribute: str = "id"
    ) -> WebElement:
        """Selects child of `element`.

        Parameters
        ----------
        element : WebDriver
            parent
        value : str
            Child's attribute's value.
        by_attribute : str, optional
            Attribute.

        Returns
        -------
        WebElement
            Child element.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        child = wait.until(
            lambda elem: element.find_element(ATTR_SELECTOR[by_attribute], value)
        )
        return child

    @quitdriver
    def children_of(self, element, value, by_attribute="id") -> WebElements:
        """Selects children of `element`.

        Parameters
        ----------
        element : WebDriver
            parent
        value : str
            Children's attribute's value.
        by_attribute : str, optional
            Attribute.

        Returns
        -------
        list[WebElement] = WebElements
            Child element.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        children = wait.until(
            lambda eleme: element.find_elements(ATTR_SELECTOR[by_attribute], value)
        )
        return children

    @quitdriver
    def click_element(self, element: WebElement) -> WebElement:
        """
        click_element

        Click a selected element.

        Parameters
        ----------
        element : WebElement
            Clickable (previously selected) element. If element
            is not clickable, selenium raises InvalidSelectorException.

        Returns
        -------
        WebElement
            Clicked element (selenium web element).
        """
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(EC.element_to_be_clickable(element)).click()
        return element

    @quitdriver
    def click(self, value: str, by_attribute: str = "id") -> WebElement:
        """ "click on element"""
        elem = self.element(value, by_attribute)
        self.click_element(elem)
        return elem

    @quitdriver
    def click_id(self, id_value) -> WebElement:
        """ "quit element by id"""
        return self.click(id_value, "id")

    @quitdriver
    def send_to_element(self, element: WebElement, key, enter=False):
        """
        send_key similar to Window.send

        Send 'key' to WebElement 'element'

        Parameters
        ----------
        element : WebElement
            Valid WebElement from selenium.
        key : Valid Selenium key or text.

        Returns
        -------
        WebElement
            Element which key was sent to.
        """
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(EC.element_to_be_clickable(element)).send_keys(key)
        if enter:
            element.send_keys(Key.enter)
        return element

    @quitdriver
    def send(self, key, value: str, by_attribute="id", enter=False):
        """
        send

        Send a valid 'key' to element with selector 'by' and
        corresponding 'value'.

        Parameters
        ----------
        key : Valid Selenium key or text.
        value : str
            _description_
        by : str, optional
            _description_, by default 'name'
        step : float, optional
            timeout step, by default 0.5
        timeout : int, optional
            timeout until throw error, by default 10

        Returns
        -------
        WebElement
            Element which key was sent to.
        """
        elem = self.element(value, by_attribute)
        return self.send_to_element(elem, key, enter)

    @quitdriver
    def arrow_down_element(self, element, n_times: int = 1, enter=False):
        """
        arrow_down

        Press keyboard arrow down n_times at
        element.

        Parameters
        ----------
        element : WebElement
            Valid WebElement from selenium
        n_times : int, optional
            Number of times pressing down key, by default 1
        """
        wait = WebDriverWait(self.driver, self.timeout)
        for _ in range(n_times):
            wait.until(EC.element_to_be_clickable(element)).send_keys(Key.down)
        if enter:
            wait = WebDriverWait(self.driver, self.timeout)
            wait.until(EC.element_to_be_clickable(element)).send_keys(Key.enter)
        return element

    @quitdriver
    def arrow_down(
        self,
        value: str,
        by_attribute="id",
        n_times: int = 1,
        enter=False,
    ):
        """
        arrow_down

        Select element by given selector 'by' and
        corresponding value, then send keyboard
        arrow down n_times.

        Parameters
        ----------
        value : str
            value of the selected attributes
        by : str, optional
            attribute, by default "name"
        step : float, optional
            timeout setp, by default 0.5
        timeout : int, optional
            timeout, by default 10
        n_times : int, optional
            times of pressing arrow up, by default 1
        enter : bool, optional
            If True, 'enter' key is sent to element, by default False
        """
        element = self.element(value, by_attribute)
        return self.arrow_down_element(element, n_times, enter)

    @quitdriver
    def arrow_up_element(self, element, n_times: int = 1, enter=False):
        """
        arrow_down

        Presse keyboard arrow up n_times

        Parameters
        ----------
        element : WebElement
            Valid WebElement from selenium
        n_times : int, optional
            Number of times pressing down key, by default 1
        """
        wait = WebDriverWait(self.driver, self.timeout)
        for _ in range(n_times):
            wait.until(EC.element_to_be_clickable(element)).send_keys(Key.up)
        if enter:
            wait = WebDriverWait(self.driver, self.timeout)
            wait.until(EC.element_to_be_clickable(element)).send_keys(Key.enter)

    @quitdriver
    def arrow_up(
        self,
        value: str,
        by_attribute="id",
        n_times: int = 1,
        enter=False,
    ):
        """
        arrow_up

        Select element by given selector 'by' and
        corresponding value, then send keyboard
        arrow up n_times.

        Parameters
        ----------
        value : str
            value of the selected attributes
        by : str, optional
            attribute, by default "name"
        step : float, optional
            timeout setp, by default 0.5
        timeout : int, optional
            timeout, by default 10
        n_times : int, optional
            times of pressing arrow up, by default 1
        enter : bool, optional
            If True, 'enter' key is sent to element, by default False
        """
        element = self.element(value, by_attribute)
        self.arrow_up_element(element, n_times, enter)

    @quitdriver
    def items_of(self, parent: WebElement, click=True) -> WebElements:
        """
        items_of

        Select li elements nested within 'parent'. Syntax:
        ```html
        <parent>
            <ul>
                <li></li>
                <li></li>
                ...
                <li></li>
            </ul>
        </parent>
        ```
        Parameters
        ----------
        parent : WebElement
            parent of ul element.
        step : float, optional
            Time between trial calls, by default 0.5
        timeout : int, optional
            Total Timeout, by default 10
        click : bool, optional
            Whether to click parent before and after, by default True

        Returns
        -------
        WebElements
            List of li elements.
        """
        if click:
            self.click_element(parent)
        ul_element = self.child_of(parent, "ul", "tag name")
        li_element = self.children_of(ul_element, "li", "tag name")
        if click:
            self.click_element(parent)
        return li_element

    def run_script(self, script: str):
        """
        run_script

        Execute Javascript code given a string.

        When interacting with log in forms or register,
        prefer this method instead of `Crawler.send` or
        `Crawler.send_to_element`.

        Parameters
        ----------
        script : str
            Javascript code.

        Returns
        -------
        unknown
            Whatever JavaScript code returns.
        """
        wait = WebDriverWait(self.driver, self.timeout)

        def run():
            return self.driver.execute_script(script)

        result = wait.until(run)
        return result

    def query_selector(self, selector: str):
        """run document.querySelector()"""
        script = document_query_selector(selector)
        return self.run_script(script)

    def value_to_selector(self, selector: str, value: str):
        """
        value_to_selector

        Assing 'value' to value attribute of the
        first element found with 'selector'.

        When interacting with log in forms or register,
        prefer this method instead of `Crawler.send` or
        `Crawler.send_to_element`.

        Parameters
        ----------
        selector : str
            Element selector.
        value : str
            Element's value. Equivalent to:
                document.querySelector(selector).value=value
            in JavaScript.

        Returns
        -------
        unkown
            Whatever JavaScript returns.
        """
        script = document_query_selector(selector)
        script += f'.value="{value}"'
        return self.run_script(script)

    def to_selector(self, selector: str, attribute: str, value: str):
        """
        value_to_selector

        Assing 'value' to 'attribute' of the
        first element found with 'selector'.

        When interacting with log in forms or register,
        prefer this method instead of `Crawler.send` or
        `Crawler.send_to_element`.

        Parameters
        ----------
        selector : str
            Element selector.
        value : str
            Element's value. Equivalent to:
                document.querySelector(selector).value=value
            in JavaScript.

        Returns
        -------
        unkown
            Whatever JavaScript returns.
        """
        script = document_query_selector(selector)
        script += f'.{attribute}="{value}";'
        return self.run_script(script)

    @quitdriver
    def scroll_page(
        self,
    ):
        """scroll page 1 vh"""
        body = self.element("body", "tag name")
        self.send_to_element(body, Keys.PAGE_DOWN)

    @quitdriver
    def google(self, query):
        """select anchors from Google search page"""
        self.goto("https://google.com")
        search_bar = self.element("q", "name")
        search_bar.send_keys(query)
        search_bar.send_keys(Key.enter)
        # time.sleep(3)
        results = self.element("rso", "id")
        return results.find_elements(By.TAG_NAME, "a")

    @quitdriver
    def source(
        self,
    ) -> str:
        """ "source page"""
        return self.driver.page_source

    def close(
        self,
    ) -> None:
        """Closes the current window."""
        self.driver.close()

    def quit(self, clean=False):
        """Quits the driver and close every associated window."""
        self.driver.quit()
        if clean:
            try:
                print("cleaning browser's data...")
                cleaner = Cleaner[self.__browser]()
                cleaner.clear_data()
                self.logger.info("Browser's data cleared.")
                print("Done!")
            except Exception as err:  # pylint: disable=broad-except
                print(err, "Couldn't clean browser's data.")
