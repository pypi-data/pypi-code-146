"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""

# selenium 3 & 4
from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager

from src.tests.drivercontroller.drivers.abstract.driver import IDriver

class Opera(IDriver):
    
    def get_browser(self) -> IDriver:
        self.driver = webdriver.Opera(executable_path=OperaDriverManager().install())
        return self.driver