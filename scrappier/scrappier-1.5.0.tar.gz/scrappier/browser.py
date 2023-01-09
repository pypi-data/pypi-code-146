from .element import Element

from datetime import datetime

from scrappier.element_collection import ElementCollection
from scrappier.element_finder import ElementFinder

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Browser:
    
    options = [
        '--headless',
        '--disable-gpu',
        '--incognito'
    ]

    driver = None

    service = Service('/usr/bin/chromedriver')

    def __init__(self):
        self.build()
        self.resize(1400, 1000)

    def width(self) -> int:
        return self.driver.get_window_size()["width"]

    def build(self):

        options = Options()

        for option in self.options:
            options.add_argument(option)

        self.driver = webdriver.Chrome(
            service=self.service,
            options=options
        )

        self.driver.delete_all_cookies()

    def resize(self, width:int, height:int):
        if self.driver:
            self.driver.set_window_size(width,height)

    def webdriver(self):
        return self.driver

    def screenshot(self, path:str):
        self.driver.get_screenshot_as_file(f"{path}")

    def snapshot(self):
        path = f"{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.png"

        self.screenshot(path)

    def html(self) -> str:
        return self.driver.page_source

    def url(self) -> str:
        return self.driver.current_url

    def wait(self, seconds:int):
        self.driver.implicitly_wait(seconds)

    def select(input:str, value:str):
        """
        selects an specific value of the given select name
        """

        select = Select(self.driver.find_element_by_name(input))
        select.select_by_value(value)

    def visit(self, url:str, params:dict = {}) -> None:

        params = ['{}={}'.format(param, value) for param, value in params.items()]
        params = '&'.join(params)

        if params:
            url = url+"?"+params

        self.driver.get(url)

    def where_xpath(self, xpath:str) -> 'ElementFinder':
        return ElementFinder(
            locator = (By.XPATH, xpath),
            driver = self.driver
        )

    def where_name(self, name:str) -> 'ElementFinder':
        return ElementFinder(
            (By.NAME, name),
            self.driver
        )

    def where_id(self, id:str) -> 'ElementFinder':
        return ElementFinder(
            (By.ID, id),
            self.driver
        )

    def where_contain_text(self, text:str) -> 'ElementFinder':
        return ElementFinder.where_xpath(
            f"//*[contains(text(), '{text}')]",
            self.driver
        )

    def where_inner_text(self, text:str) -> 'Elementfinder':
        return ElementFinder.where_inner_text(text, self.driver)

    def where_class_name(self, name:str) -> 'ElementFinder':
        return ElementFinder(
            (By.CLASS_NAME, name),
            self.driver
        )

    def where_tag_name(self, name:str) -> 'ElementFinder':
        return ElementFinder(
            (By.TAG_NAME, name),
            self.driver
        )

    def where_attribute(self, attribute, value) -> 'ElementFinder':
        return ElementFinder(
            (By.XPATH, f"//*[@{attribute}='{value}']"),
            self.driver
        )