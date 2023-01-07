"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.test23.tests.drivercontroller.drivers.abstract.driver import IDriver

class Chrome(IDriver):
    
    def get_browser(self) -> IDriver:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return self.driver
    
