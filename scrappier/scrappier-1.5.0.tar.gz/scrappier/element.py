from __future__ import annotations
from typing import TYPE_CHECKING
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import scrappier

class Element():
    """
    A class that represents a DOM element
    """

    def __init__(self, element: WebElement, driver: WebDriver):
        self.driver = driver
        self.element = element

    def enter(self):
        self.element.send_keys(Keys.RETURN)

    def type(self, text:str):
        """
        Types an specific text in an input field
        """

        self.element.send_keys(text)

    def text(self) -> str:
        """
        gets the inner text of the element
        """

        return self.element.text

    def html(self) -> str:
        """
        gets the inner html of the element
        """

        return self.element.get_attribute('innerHTML')

    def attribute(self, name:str) -> str:
        """
        gets the attribute's value
        """

        return self.element.get_attribute(name)

    def attributes(self) -> list:
        """
        gets all attributes of the element
        """

        lst = []

        for attribute in self.element.get_property('attributes'):
            lst.append({
                "name": attribute["name"],
                "value": attribute["value"]
            })

        return lst

    def click(self):
        """
        clicks the element
        """

        self.element.click()

    def clear(self):
        """
        clear the input field
        """

        self.element.clear()

    def children(self) -> scrappier.element_collection.ElementCollection:
        """
        gets a collection of the next children elements
        """

        return scrappier.element_collection.ElementCollection(
            self.element.find_elements(By.XPATH,"./child::*"),
            self.driver
        )

    def next_sibling(self):
        """
        gets the next element of the current element
        """

        return scrappier.element_finder.ElementFinder.next_sibling(self.driver, self.element)
        
    def tag(self) -> str:
        """
        retrieves the tag name of the element
        """
        return self.element.tag_name

    def value(self, value = None):
        
        if not value:
            return self.element.get_attribute("value")

        if self.tag() == "select": 
            Select(self.element).select_by_value(value)
            return

        self.type(value)

    def where_tag_name(self, name:str) -> scrappier.element_finder.ElementFinder:
        """
        find a subelement with the tag name specified
        """

        return scrappier.element_finder.ElementFinder.where_tag_name(
            name,
            self.driver,
            self.element
        )

    def where_attribute(self, attribute:str, value:str) -> scrappier.element_finder.ElementFinder:
        """
        find a subelement with the attribute and value specified
        """

        return scrappier.element_finder.ElementFinder.where_xpath(
            f".//*[@{attribute}='{value}']",
            self.driver,
            self.element
        )