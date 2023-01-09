from __future__ import annotations
import random
from .element import Element
from selenium.webdriver.chrome.webdriver import WebDriver
from pycollection import Collection

class ElementCollection(Collection):

    def __init__(self, items, driver:WebDriver):
        super().__init__(items)
        self.driver = driver

    def item(self, item) -> Element:
        return Element(item, self.driver)