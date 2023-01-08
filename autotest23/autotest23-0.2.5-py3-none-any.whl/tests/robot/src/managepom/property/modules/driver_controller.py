"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
# selenium 4
import pytest
import re

from time import perf_counter
from src.test23.tests.constants.common_constants import CommonConstants
from src.test23.tests.drivercontroller.driver_factory import DriverFactory, DriverFactoryParallel
from src.test23.tests.resources.custom_keywords import CustomKeywords

class DriverController(CommonConstants, DriverFactory, DriverFactoryParallel, CustomKeywords):
    """
    DriverController is a service which is responsible for Providing all the 
    Web Driver based services and other commonly used web methodologies. 
    As it inharites CommonConstants & CustomKeywords also it acts more like 
    one stope solution for the Test Scenerio scripts. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    driver = None
    logger = None
    
    # This method is responsible for opening browser window
    # each time when it is called. if there is no argument
    # this method will select default option from the CommonConstants.
    def open_single_browser(self, choice: int = None):
        if choice is None:
            choice = self.DEFAULT_BROWSER_OPTION
        # Choosing browser from the Driver Factory.
        self.driver = self.choose_browser(choice)
        # Opening browser window.
        self.driver = self.driver.get_browser()        
        
    def before_Suite(self):
        if self.BASE_URL is None:
            self.logger.warning("Testing in Localhost.")
            self.driver.get(self.live_server_url)
        elif re.match(self.URL_VALIDATOR_CHAR, self.BASE_URL) is not None:
            self.logger.warning("Testing with Live URL.")
            self.driver.get(self.BASE_URL)
        else: 
            self.logger.warning("Base URL is not valid.")
            raise Exception("""
                            ****************************************
                            |||>>>>>>Base URL is not valid!<<<<<<|||
                            ****************************************
                            """)
    
    def after_suite(self):
        self.driver.close()
        
    @pytest.fixture(scope= "class")
    def suit_setup_and_tear_down(self):
        # Preparing Log file and passing parameter of the Log file location from the CommonConstants. 
        self.log(file_directory= self.LOG_FILE_PATH_LOCATION)
        #Checking the test mode is single or parallel.
        if self.PARALLEL_MODE:
            self.logger.warning("Conducting Test in Parallel Mode.")
            """More R&D Needed! concurrent_browser_attack is not fit for Production"""
            # https://docs.python.org/3/library/threading.html
            self.concurrent_browser_attack()
        else:            
            self.logger.warning("Conducting Test in Single Browser Mode.")  
            self.open_single_browser()
            self.logger.warning(f"browser_name: {self.driver.name}")
            self.logger.warning(f"browser_version: {self.driver.capabilities['browserVersion']}")
            self.before_Suite()
            yield
            self.after_suite()
        # if self.GENERATE_JSON_REPORT:
        #     self.logger.warning(self.json_reporter(self.TARGET_TEST_AREA_LOCATION, self.JSON_REPORT_FILE_PATH))

    # This fixture can be used to identify the execution time of a class.  
    @pytest.fixture(scope= "class")      
    def time_counter(self):
        start_time = perf_counter()
        yield
        end_time = perf_counter()
        print(f'It took {end_time- start_time: 0.2f} second(s) to complete.')

    # @pytest.fixture(scope= "class")
    # def concurrent_suit_setup_and_tear_down(self):
    #      # create two new threads
    #     t1 = Thread(target=self.open_single_browser)
    #     t2 = Thread(target=self.open_single_browser)
    #     # start the threads
    #     t1.start()
    #     t2.start()
    #     self.before_Suite()
    #     yield
    #     self.after_suite()
    #     # wait for the threads to complete
    #     t1.join()
    #     t2.join()
        
        
        
            
            