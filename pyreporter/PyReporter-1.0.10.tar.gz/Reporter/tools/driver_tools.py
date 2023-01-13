from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import asyncio, time
from typing import Dict


MAX_WAIT_TIME = 600
DEFAULT_PAGE_LOAD_TIME = 3


class DriverTools():
    def __init__(self, driver: webdriver):
        self._driver = driver


    # click(element): clicks on 'element' that is covered
    #   by another element (elements that are not button tags but act like buttons)
    def click(self, element: WebElement):
        self._driver.execute_script("arguments[0].click();", element)


    # wait_refresh(unique_element_name, unique_element_type):
    #   Waits for a refresh of the current page
    async def wait_refresh(self, unique_element_name: str, unique_element_type: By = By.CLASS_NAME):
        try:
            WebDriverWait(self._driver, MAX_WAIT_TIME).until(EC.presence_of_element_located((unique_element_type, unique_element_name)))
        except:
            self._driver.quit()
            print("timed out")


    # wait_disappear(unique_element_name, unique_element_type):
    #   Waits for an element to disappear
    async def wait_disappear(self, unique_element_name: str, unique_element_type: By = By.CLASS_NAME):
        try:
            WebDriverWait(self._driver, MAX_WAIT_TIME).until(EC.invisibility_of_element_located((unique_element_type, unique_element_name)))
        except:
            self._driver.quit()
            print("timed out")


    # get_window_size(): shortcut to retrieve the window size (width and height)
    def get_window_size(self) -> Dict[str, int]:
        return self._driver.get_window_size()


    # get_window_height(): Retrieves the window's height
    def get_window_height(self) -> int:
        return self.get_window_size()["height"]


    # get_window_width(): Retrieves the window's width
    def get_window_width(self) -> int:
        return self.get_window_size()["width"]


    # scroll_to_view(element): scrolls until 'element' becomes just visible
    #   on the screen
    def scroll_to_view(self, element: WebElement):
        self._driver.execute_script("arguments[0].scrollIntoView();", element)


    # scroll_to(pixel): scrolls to some 'pixel' level of the screen
    def scroll_to(self, pixel: int):
        self._driver.execute_script(f"window.scrollTo(0, {pixel})")


    # wait_page_load(wait_time): Waits for page to load certain elements
    async def wait_page_load(self, wait_time: int = DEFAULT_PAGE_LOAD_TIME):
        await asyncio.sleep(wait_time)
