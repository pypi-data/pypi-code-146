"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from src.tests.drivercontroller.drivers.abstract.driver import IDriver

class Edge(IDriver):
    
    def get_browser(self)  -> IDriver:
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        return self.driver