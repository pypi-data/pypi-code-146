import time

from config import nRoboConfig
from selenium import webdriver
import random
from abc import ABC

from helpers.DriverManager import DriverManager


class TestBase(ABC):
    """
    Description
        This is a base class of all Test classes in the framework.
        Every Test class should inherit it in order to leverage
        benifits of couple of advanced features available in the
        TestBase class.

        Please go through its class methods for more details.
    """

    def open_additional_browser(self, window_name: str, url: str, browser: str) -> webdriver:
        """
        Description
            Creates a new driver instance, sets its unique name , opens url
            in the new driver instance

        Returns
            new driver instance -> webdriver obj
        """
        # get new driver instance, set its name and save it in
        # additional_drivers dictionary
        self.drivers_by_window_name[window_name] = DriverManager.get_driver(browser)

        # reset driver reference
        self.driver = self.drivers_by_window_name[window_name]

        # reset current driver in focus
        self.drivers_by_status[nRoboConfig.WebDriverStatuses.CURRENT_DRIVER.value] = self.driver

        # open new url
        self.driver.get(url)

        # maximize browser window
        self.driver.maximize_window()

        # add random pause
        random.randint(
            nRoboConfig.TimeLimits.TIME_MIN_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value,
            nRoboConfig.TimeLimits.TIME_MAX_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value
        )

        return self.driver

    def switch_to_window_by_name(self, window_name):
        """
        Description
            Switches to the given window name

        Returns
            driver reference to the new window -> webdriver obj ref
        """
        print("\n Start: Switching window {}".format(window_name))
        time.sleep(.30)
        # reset driver reference
        self.driver = self.drivers_by_window_name[window_name]

        # reset current driver in focus
        self.drivers_by_status[nRoboConfig.WebDriverStatuses.CURRENT_DRIVER.value] = self.driver

        # now, add random pause between tests-backup
        random.randint(
            nRoboConfig.TimeLimits.TIME_MIN_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value,
            nRoboConfig.TimeLimits.TIME_MAX_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value
        )
        print("\n End: Switching window")
