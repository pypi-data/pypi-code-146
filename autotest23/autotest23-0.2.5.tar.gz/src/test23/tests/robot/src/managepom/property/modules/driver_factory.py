"""
********************Factory Method Design Pattern********************

© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from time import sleep
from threading import Thread
from src.test23.tests.drivercontroller.drivers.abstract.driver import IDriver
#from tests.drivercontroller.drivers.brave import Brave
from src.test23.tests.drivercontroller.drivers.chrome import Chrome
#from tests.drivercontroller.drivers.chromium import Chromium
from src.test23.tests.drivercontroller.drivers.edge import Edge
from src.test23.tests.drivercontroller.drivers.firefox import Firefox
from src.test23.tests.drivercontroller.drivers.opera import Opera

class DriverFactory():
    """
     Driver Factory is responsible for serving WebDriver Object according to the demand. 
     No matther how much WebDrivers are available, consumers dont need to find and configure 
     those manually. DriverFactory will serve those as one stop solution.                                       
     © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    DRIVER_OPTION = {
        1: Chrome(),
        4: Firefox(),
        5: Edge(),
        6: Opera()
    }
    """ If new WebDriver is created please add that in this dictionary. © BS23"""
    
    def choose_browser(self, choice: int = None) -> IDriver:
        if choice is None:
            choice = int(input("Please, choose your browser and press ENTER:"))
        driver_obj = self.DRIVER_OPTION[choice]
        return driver_obj


"""
********************Concurrent Browser Attack R&D********************

© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# https://docs.python.org/3/library/threading.html
# https://www.pythontutorial.net/advanced-python/python-threading/
class DriverFactoryParallel():
    
    def task_one(self):
        driver_obj = Chrome()
        driver_obj.get_browser()
        sleep(5)
        
    def task_two(self):
        driver_obj = Edge()
        driver_obj.get_browser()
        sleep(5)
    
    #Threading vs Multiprocessing
    def concurrent_browser_attack(self):
        # create two new threads
        t1 = Thread(target=self.task_one)
        t2 = Thread(target=self.task_two)
        # start the threads
        t2.start()
        #sleep(0.2)
        t1.start()
        # wait for the threads to complete
        t1.join()
        t2.join()