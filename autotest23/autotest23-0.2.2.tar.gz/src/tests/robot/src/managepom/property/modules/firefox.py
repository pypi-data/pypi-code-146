"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""

# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from src.tests.drivercontroller.drivers.abstract.driver import IDriver

class Firefox(IDriver):
    
    def get_browser(self) -> IDriver:
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        return self.driver