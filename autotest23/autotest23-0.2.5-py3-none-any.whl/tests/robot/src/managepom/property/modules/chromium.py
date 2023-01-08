"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from src.test23.tests.drivercontroller.drivers.abstract.driver import IDriver

class Chromium(IDriver):
    
    def get_browser(self) -> IDriver:
        self.driver = webdriver.Chrome(service=Service(\
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        return self.driver