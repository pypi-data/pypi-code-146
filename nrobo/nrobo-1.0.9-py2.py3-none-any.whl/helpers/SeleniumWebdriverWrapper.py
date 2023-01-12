from config import nRoboConfig
from helpers import DriverManager as DriverManager
from . import custom_logger as cl

from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import logging
import time
import os
# from configuration import config_v2, config_spherobot, paths, field_constants, apps, runtime_test_configuration
from selenium.webdriver.common.action_chains import ActionChains
from abc import ABC


# from multipledispatch import dispatch


class SeleniumWebdriverWrapper(ABC):
    """
    Description
        Custom wrapper class over standard web-driver class.
        The aim of wrapper class is to wrap web-driver functionality
        per the framework's need.

        Following is a list of advantages achieved:
            1. Wrapper methods are more consistent.
            2. Wrapper methods handles few exceptions in a better way.
            3. Wrapper methods are customized to handle a few exceptional
            application specific behavior
            4. Also have application specific global methods along with
            standard web-driver wrapper methods
            5. Wrapper methods are more consistent than web-driver methods.
            6. Wrapper methods also customized to support additional waits
            to complete an operation
    """

    # logger instance
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        """
        Description
            constructor method.
            Initialize private driver reference to current page
            Sets the global dynamic pause time
        """

        # private driver variable
        self.driver = driver

        # set global pause time in seconds
        # config_v2.wait = 60

        self.wait_for_action_complete()

        self.wait_for_page_load()

    def wait_for_page_load(self):
        print('WaitForPageLoadStart')
        """
        Description
            waits until a page is loaded by checking if document.readyState is complete or something else
        """
        # self.__message_start("Wait for page load.")

        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)

        if nRoboConfig.GlobalLocators.page_loading_complete_indicator_element.value[0] is not None \
                and nRoboConfig.GlobalLocators.page_loading_complete_indicator_element.value[1] is not None:
            self.wait_till_invisibility_of_element_located(
                nRoboConfig.GlobalLocators.page_loading_complete_indicator_element.value)

        self.wait_for_action_complete(nRoboConfig.GlobalLocators.page_loading_complete_indicator_element.value)

        # wait for amount of time that is set in the configurations/config_v2.py file
        WebDriverWait(self.driver, nRoboConfig.Waits.STATIC_WAIT.value).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')

        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)

        # wait for 2 more seconds
        # self.static_wait(2)
        # self.__message_end("Wait for page load.")

    def wait_till_invisibility_of_element_located(self, by: By, locator: str):
        """
        Description
            This method waits until the element defined by locator becomes invisible.
            This method will be used on pages where loader is present,
            And script needs to wait until the loading is complete,
            By continuously checking if the loader is disappeared.
        """
        self.__message_start("\tWait until data is being fetched.")

        # pause for 2 seconds
        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)

        # wait until the locator becomes invisible
        WebDriverWait(self.driver, nRoboConfig.Waits.STATIC_WAIT.value).until(
            EC.invisibility_of_element_located((by, locator)))

        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)
        # self.wait_for_element_invisible(By.XPATH, "//div[@style='display: block;'][contains(.,'Processing...')]")

        self.__message_end("Wait until data is being fetched.")

    def wait_till_process_finished(self, by: By, locator: str):
        """
        Description
            This method waits until the loading is completed
        """
        self.__message_start("Wait until process is finished")

        # pause for 2 seconds
        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)

        # wait until loading is completed
        # WebDriverWait(self.driver, config_v2.wait).until(
        #    EC.invisibility_of_element_located((By.XPATH, "//body[contains(@class,'loading')]")))
        self.wait_for_element_invisible(by, locator)

        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)
        self.__message_end("Wait until process is finished")

    def wait_for_element_invisible(self, by: By, locator: str):
        """
        Description
            wait until element is invisible

        Parameters
            By -> By obj : Locating strategy
            locator -> str obj : Element locator
        """
        WebDriverWait(self.driver, nRoboConfig.Waits.STATIC_WAIT.value).until(
            EC.invisibility_of_element_located((by, locator)))

    def wait_for_element_clickable(self, by: By, locator: str):
        """
        Description
            wait for element and clicks on it

        Parameters
            element -> WebElement obj : Page element
        """
        self.wait_for_page_load()
        # wait for element and click on it
        page_element = WebDriverWait(self.driver, nRoboConfig.Waits.STATIC_WAIT.value).until(
            EC.element_to_be_clickable(by, locator))

        return page_element

    # @dispatch(WebElement)
    # def _is_element_displayed(self, element):
    #     return element.is_displayed()

    def get_text(self, by: By, locator: str):
        """
        Description
            This method returns the text of the element
        """

        # return element text
        return self.get_text_by_element(self.find_by_element(by, locator))

    def get_text_by_element(self, element):
        """
        Description
            This method returns the text of the element
        """

        # return element text
        return str(element.text)

    # @dispatch(By, string)
    def is_element_displayed(self, by: By, locator: str, skip_wait_for_element: bool = False):
        """
        Description
            This method will wait until an element is displayed

        Parameters
            By -> By obj : Locating strategy
            locator -> str obj : Element locator
        """

        # element variable
        element = None

        try:
            # find element
            if skip_wait_for_element:
                element = self.driver.find_element(by, locator)
            else:
                element = self.wait_for_element(by, locator, "", -1, False)

            # check if the element is displayed
            element.is_displayed()

            # if no exception, then the element is displayed and return with True to the caller
            return True

        except Exception as e:
            # if exception, then the element is not displayed due to some reason,
            # and return with False to the caller
            return False

    def is_checkbox_selected(self, by: By, locator: str):
        return self.find_by_element(by, locator).is_selected()

    def select_value_from_dropdown_by_visible_text_contains(self, element, text):
        """
        Description
            This method selects a visible text from the drop down

        Parameters
            element -> WebElement obj : Element locator
            text -> str obj : option text
        """

        # initialize select element
        # select = Select(element)
        element.click()

        try:
            # For outbound truck checkin
            i = 0
            for option in element.find_elements_by_tag_name('option'):
                # self.log.info(">" + option.text + "----" + text)
                old_option_text_value_attribute = option.get_attribute("value")
                # self.log.info("v=" + old_option_text_value_attribute)
                option_text = option.text  # .replace(" ", "")
                # self.log.info("|" + option_text + "|")

                # try:
                #
                #     from re import  search as search_re
                # except Exception as e:
                #     print(e)

                try:
                    if str(text).upper() in str(option_text).upper():
                        # self.log.info("MATCH FOUND["+str(i)+"]")
                        # select = Select(element)
                        # select.select_by_value(old_option_text_value_attribute)
                        # actions = ActionChains(self.driver)
                        # actions.move_to_element(element).click().perform
                        return i
                    else:
                        # self.log.info("MATCH NOT FOUND["+ str(i) +"]")
                        pass

                except Exception as e:
                    self.log.info(e)
                    pass

                i = i + 1
                # self.log.info("i="+ str(i))

        except Exception as e:
            # For inbound truck checkin
            self.log.info("Exception")
            self.log.info(e)

        return -1

    def select_value_from_dropdown_by_visible_text(self, element, text):
        """
        Description
            This method selects a visible text from the drop down

        Parameters
            element -> WebElement obj : Element locator
            text -> str obj : option text
        """

        # initialize select element
        select = Select(element)

        # select an option with visible text
        select.select_by_visible_text(text)

    def get_select_index_by_text(self, locator_xpath, text):
        # For outbound truck checkin
        i = 0
        v = []
        for option in self.driver.find_elements(By.XPATH, locator_xpath):
            v.append(option.text)
            if str(text).upper() in str(option.text).upper():
                return i  # Match found. Return index.
            i = i + 1
        # raise Exception(str(len(v)) + " <> " + str(i))

        return -1  # No match found!

    def select_value_from_dropdown_by_value(self, element, value):
        """
        Description
            This method selects an option from a drop down by value

        Parameters
            element -> WebElement obj : Element locator
            value -> str obj : Value to select form the drop down
        """

        # create select element
        select = Select(element)

        # select an option from the drop down with same value
        select.select_by_value(value)

    def select_value_from_dropdown_by_visible_text(self, element, value):
        """
        Description
            This method selects an option from a drop down by visible text

        Parameters
            element -> WebElement obj : Element locator
            value -> str obj : Value to select form the drop down
        """

        # create select element
        select = Select(element)

        # select an option from the drop down with same value
        select.select_by_visible_text(value)

    def select_value_from_dropdown_by_index(self, element, index):
        """
        Description
            This method selects an option from the drop down by index

        Parameters
            element -> WebElement obj : Element locator
            index -> int obj : Index of the option to select
        """

        # create a drop down element
        select = Select(element)

        # selects an option from the drop down with given index
        select.select_by_index(index)

    def select_value_from_dropdown_by_index(self, element, index):
        """
        Description
            This method selects an option from the drop down by index

        Parameters
            element -> WebElement obj : Element locator
            index -> int obj : Index of the option to select
        """

        # create a drop down element
        select = Select(element)

        # selects an option from the drop down with given index
        select.select_by_index(index)

    # @dispatch(WebElement, WebElement)
    def drag_and_drop(self, source_element, destination_element):
        """
        Description
            This method drags source element and drop over the destination element

        Parameters
            source_element -> WebElement obj : Source element
            destination_element -> WebElement obj : Destination element
        """

        #
        ActionChains(self.driver).drag_and_drop(source_element, destination_element).perform()
        # self.wait_for_action_complete()
        self.wait_for_page_load()

    # @dispatch(WebElement, float, float)
    def drag_and_dropx(self, element, xoffset, yoffset):
        """
        Description
            This method drags and drops an element based on xoffset and yoffset

        Parameters
            element -> WebElement obj : Element that need to be dragged
            xoffset -> int obj : x offset value
            yoffset -> int obj : y offset value
        """

        # mouse over element by given x and y offset
        ActionChains(self.driver).drag_and_drop_by_offset(element, xoffset, yoffset).perform()
        # self.wait_for_action_complete()
        self.wait_for_page_load()

    # @dispatch(WebElement)
    def hover_over_element(self, element):
        """
        Description
            This method hovers over element

        Parameters
            element -> WebElement obj : Page element
        """

        # mouse over element
        ActionChains(self.driver).move_to_element(element).perform()
        self.wait_for_page_load()

    # @dispatch(WebElement, float, float)
    def hover_over_element(self, element, xoffset, yoffset):
        """
        Description
            This method hovers over element

        Parameters
            element -> WebElement obj : Page element
            xoffset -> float obj : X offset
            yoffset -> float obj : Y offset
        """

        # mouse over element by given x and y offset
        ActionChains(self.driver).move_to_element_with_offset(element, xoffset, yoffset).perform()
        self.wait_for_page_load()

    def click_using_js(self, element):
        """
        Description
            This method clicks on the element using javascript execute method
        """

        # click the element using javascript execute
        self.driver.execute_script("arguments[0].click();", element)
        self.wait_for_page_load()

    def type_using_js(self, element, value):
        """
        Description
            This method clicks on the element using javascript execute method
        """

        # click the element using javascript execute

        self.driver.execute_script("arguments[0].value='" + value + "';", element)

    def scroll_to_view(self, element):
        """
        Description
            This method scrolls to the element view
        """

        # scrolls to the element view
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def close_browser(self):
        """
        Description
            This method closes the current browser
        """

        # closes the current browser
        self.driver.close()

    def close_system_dialogue(self):
        """
        Description
            This method closes the system dialogue
        """
        self.driver.get("https://google.com")
        # ActionChains(self.driver).send_keys(Keys.TAB).perform()
        # self._static_wait(1)
        # ActionChains(self.driver).send_keys(Keys.ENTER).perform()

    def get_shadow_root_element(self, element):
        """
        Description
            This method shadows the root element

        Parameters
            element -> WebElement obj : Page element
        """

        ele = self.driver.executeScript("return arguments[0].shadowRoot", element)

        return ele  # return to the caller

    def wait_for_and_switch_to_new_system_dialogue(self):
        """
        Description
            This method waits for a new system dialogue.
        """
        available_windows = []
        available_windows = self.get_available_window_handles(available_windows)
        count = 1
        while len(available_windows) <= 1:
            if count < 60:
                self.static_wait(1)
                available_windows = self.get_available_window_handles(available_windows)
                count += 1
            else:
                break
        self.static_wait(1)
        self.switch_to_specific_window(available_windows[1])
        return available_windows

    def switch_to_new_window(self):
        """
        Description
            This method switches to the new window
        """

        for window_handle in self.driver.window_handles:
            """loop through all window handles"""

            if self.driver.current_window_handle != window_handle:
                """if current window handle is not in available window"""

                # switch to the specified window
                self.driver.switch_to.window(window_handle)

                # return to the caller
                return window_handle

        # return None
        return None

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_to_window_handle(self, to_window_handle):
        for window_handle in self.driver.window_handles:
            """loop through all window handles"""

            if window_handle == to_window_handle:
                """if current window handle is not in available window"""

                # switch to the specified window
                self.driver.switch_to.window(window_handle)

                # return to the caller
                return window_handle

        # return None
        return None

    def switch_to_new_window_except_given_list(self, list_windows):
        """
        Description
            This method switches to the new window
        """

        for window_handle in self.driver.window_handles:
            """loop through all window handles"""

            if self.driver.current_window_handle != window_handle \
                    and window_handle not in list_windows:
                """if current window handle is not in available window"""

                # switch to the specified window
                self.driver.switch_to.window(window_handle)

                # return to the caller
                return window_handle

        # return None
        return None

    def get_available_window_handles(self, available_windows):
        """
        Description
            This method finds and returns all available windows

        This method seems like working same as self.driver.window_handles

        Parameters
            available_windows -> str[] obj : list of available windows
        """

        for window_handle in self.driver.window_handles:
            """loop through window handles"""

            if window_handle not in available_windows:
                """if window handle not in the available windows"""

                # append to the available windows array list
                available_windows.append(window_handle)

        # return updated available windows array to the caller
        return available_windows

    def get_new_window_handle_from_all_open_windows(self, available_windows={}):
        """
        Description
            This method finds and returns all available windows

        Parameters
            available_windows -> str[] obj : list of available windows
        """

        for window_handle in self.driver.window_handles:
            """loop through window handles"""

            not_found = True  # By Default, consider window_handle is not found

            for w in available_windows.values():

                if w == window_handle:
                    """if window handle found in the available windows"""
                    not_found = False
                    break

            if not_found:
                return window_handle  # return with new window handle
            else:
                continue  # test next window handle

        # return updated available windows array to the caller
        return None

    def switch_to_specific_window(self, window_name):
        """
        Description
            This method switches to the specific window with given window name

        Parameters
            window_name -> str obj : Window name
        """

        # wait for 5 seconds
        self.static_wait(5)

        # switch to the given window name
        self.driver.switch_to.window(window_name)

        # wait for page to load
        self.wait_for_page_load()

    def switch_to_default_windows(self):
        """
        Description
            This method switches to the default windows
        """

        # wait for 5 seconds
        self.static_wait(5)

        # switch to the current window handle
        self.driver.switch_to.window(self.driver.current_window_handle)

    def open_new_tab(self, url: str):
        """
        Description
            This method opens a new tab
        """

        # opens a new tab in the current browser
        link = "window.open('" + url + "','_blank');"
        self.driver.execute_script(link)
        self.wait_for_page_load()

    def find_by_element(self, by: By, locator: str, assert_text: str = "", skip: bool = False):
        """
        Description
            This method finds an element on the current page

        Parameters
            By -> By obj : Locating strategy
            value -> str obj : Element locator
            assert_text -> str obj : Customize assert text. Default is blank.
        """

        # element variable
        element = None

        # wait for the element
        element = self.wait_for_element(by, locator, assert_text, -1, skip)

        # return with element to the caller
        return element

    def type(self, by: By, locator: str, text: str, assert_text: str = ""):
        """
        Description
            This method types given value into the text element

        Parameters
            By -> By obj : Locating strategy
            locator -> str obj : Element locator
            assert_text -> str obj : Customize assert text. Default is blank.
        """

        # element variable
        element = None

        # find element on the current page
        element = self.wait_for_element(by, locator, assert_text, -1, False)

        if element is None:
            raise Exception("Element not found. ({},{})".format(str(by), str(locator)))

        try:
            # click on the element
            self.static_wait(.05)
            element.click()
        except Exception as e:
            # click on the element
            # element.click()
            pass

        # clears the element text
        element.clear()

        # types text into the element
        element.send_keys(text)

        # This is required to handle pure number strings.
        # Best example is VDN versions, they are pure numeric.
        string_value = str(text)

        if len(string_value) >= 1 and string_value[len(string_value) - 1] == Keys.ENTER:
            # check if any application specific handling is required
            self.wait_for_page_load()
        else:
            # no need to do special handling
            pass

        if assert_text != "":
            """if assert text is not blank"""
            print()  # self.log.info("- " + str(value))

        # return with element to the caller
        return element

    def get_table_rows(self, by: By = None, locator: str = None):
        """
        Description
            This method return xpath of the table rows
        """

        # return the xpath of the table rows
        if by is None and locator is None:
            return self.driver.find_elements(By.XPATH, "//tbody/tr")
        else:
            return self.driver.find_elements(by, locator)

    def wait_for_table_search_to_completion(self):
        """
        Description
            This methods waits for table search to complete
        """

        for tick in range(nRoboConfig.Waits.STATIC_WAIT.value):
            """ticker until given range"""

            # wait for 1 second
            self.static_wait(1)  # wait for a second

            if len(self.get_table_rows()) == 1:
                """if only one row is found"""

                # 1 row means, search was successful and return to the caller
                return
            else:
                """if there are more than 1 row, it means search is still in progress"""

                # continue to wait
                continue

    # except:
    #     self.log.info("FAIL - Not able to enter " + value + " in textbox.")
    #     self._screenShot()
    #     print_stack()

    def screenShot(self):
        """
        Description
            This method takes a screenshot when it is called of the current page
        """
        fileName = str(round(time.time() * 1000)) + ".png"
        screenshotDirectory = "../screenshots/"
        relativeFileName = screenshotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        destinationDirectory = os.path.join(currentDirectory, screenshotDirectory)

        if not os.path.exists(destinationDirectory):
            os.makedirs(destinationDirectory)
        self.driver.save_screenshot(destinationFile)
        # self.log.error("Exception occurred while taking screenshot")

    def getTitle(self):
        """
        Description
            This method returns the title of the current page
        """

        # return with the title of the current page to the caller
        return self.driver.title

    def delete_all_cookies_from_browser(self):
        """
        Description
            This method deletes all browser cookies from the current page
        """

        # wait for given seconds
        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)

        # delete all browser cookies
        self.driver.delete_all_cookies()

        # refresh the current page
        self.driver.refresh()

        # wait for page to load
        self.wait_for_page_load()

    def page_refresh(self):
        self.driver.refresh()
        self.wait_for_page_load()

    def static_wait(self, pause_time):
        """
        Description
            This method pauses execution for certain amount of time

        Parameters
            pause_time -> int obj : amount of time in seconds to pause execution
        """

        # pause execution for given time
        time.sleep(pause_time)

    def navigate_back(self):
        self.driver.back()
        self.wait_for_page_load()

    def page_refresh(self):
        self.driver.refresh()
        self.wait_for_page_load()

    def find_element_click(self, by: By, locator: str, assert_text: str = "",
                           skip_wait_for_element: bool = False, skip_wait_for_page_load: bool = False):
        """
        Description
            This method finds an element on the current page

        Parameters
            By -> By obj : Locating strategy
            value -> str obj : Element locator
            assert_text -> str obj : Customized assert text. Default is blank.
        """

        # element variable
        element = None

        # if not skip_wait_for_element:
        # self.wait_for_element(By, value)

        # find an element on the current page
        element = self.wait_for_element(by, locator, assert_text, -1, skip_wait_for_element)

        # click on the element
        try:
            self.wait_for_page_load()
            element.click()
            # self.wait_for_action_complete()
            if not skip_wait_for_page_load:
                self.wait_for_page_load()
        except (ElementClickInterceptedException, ElementNotInteractableException) as error:
            self.scroll_to_view(element)
            try:
                self.wait_for_page_load()
                element.click()
                # self.wait_for_action_complete()
                if not skip_wait_for_page_load:
                    self.wait_for_page_load()
            except (ElementClickInterceptedException, ElementNotInteractableException) as error:
                # print(error)
                pass

        # self.log.info("FAIL - Not able to click on the element with locator " + value)
        # print_stack()

    def open_browser_with_url(self, url: str, browser: str):
        # report_configuration = Common.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)
        driver = DriverManager.get_driver(browser)
        driver.get(url)
        driver.maximize_window()
        self.wait_for_page_load()

        return driver

    def is_element_present(self, by: By, locator: str, assert_text: str = "", skip_wait_for_element: bool = False):
        """
        Description
            This method checks if an element is present on the current page

        Parameters
            locator -> By obj : _type of locator
            value -> str obj : element locator
            assert_text -> str obj : custom assert text. Default is blank.
        """

        return self.is_element_displayed(by, locator, skip_wait_for_element)
        print("IsElementPresent start. {}: {}".format(by, locator))
        # try:
        #     # find element
        #     if skip_wait_for_element:
        #         element = self.find_by_element(By, locator, assert_text, skip=True)
        #     else:
        #         #self.static_wait(.10)
        #         element = self.wait_for_element(By, locator, assert_text)
        #     #self.static_wait(1)
        #     # find the element on the current page
        #     #element = self.wait_for_element(locator, value, assert_text)
        #     #print("ELEMENT={}".format(element is not None))
        #     if element is not None:
        #         """if element is found"""
        #
        #         print("IsElementPresent end.")
        #         # return with True to the caller
        #         return True
        #
        #     else:
        #         """if element is not found"""
        #
        #         # return with False to the caller
        #         print("IsElementPresent end.")
        #         return False
        #
        # except Exception as e:
        #     """catch exception"""
        #
        #     print("FAIL - Element not found with locator: " + locator)
        #
        #     # return with False to the caller
        #     print("IsElementPresent end.")
        #     return False

    def wait_for_element(self, by: By, locator: str, assert_text: str = "", timeout: int = -1, skip: bool = False):
        """
        Description
            This method waits for an element for a certain amount time before throwing
            TimeoutException.
            This method also sets the custom assert text to display on the report.
            If an element is found, then method returns with that element to the caller.

        Parameters
            By - By obj
            value - str obj -> locator of web element
            timeout - int obj -> max time in seconds to wait for element.
                Default is set to configurations/config_v2.wait
        """

        print("Wait For Element Displayed start {}{}".format(by, locator))
        self.static_wait(.10)
        if skip:
            # return self.is_element_displayed(By, value, skip_wait_for_element=True)
            timeout = 30

        # initialize element variable
        element = None

        timeout = nRoboConfig.Waits.TIMEOUT.value if timeout == -1 else timeout

        # log
        # self.log.info("Locator value= {0}".format(value))

        try:
            # self.static_wait(config_v2.WAIT_HALF_SEC)
            # wait for element to be located
            # element = WebDriverWait(self.driver, timeout).until(
            # EC.visibility_of_element_located((By, value)))
            # self.wait_for_element_clickable((By, value))
            # self.static_wait(config_v2.WAIT_2_MILI_SEC)
            second = 0
            # print("timeout: {}".format(timeout))
            for second in range(1, int(timeout) * 10 + 1, 1):
                print("Seconds: {}".format(second))
                try:
                    element = self.driver.find_element(by, locator)
                    if element.is_displayed():
                        self.static_wait(.10)
                        break
                except Exception as e:
                    self.static_wait(.10)

            if second > nRoboConfig.Waits.TIMEOUT.value:
                print("Element not found. {}".format(second))
                raise TimeoutException("Max time limit reached!!!")
            else:
                print("Element found. {}".format(second))

            if assert_text != "":
                """if assert text is not blank"""

                # log it
                self.log.info("PASS - " + str(assert_text))

        except TimeoutException as e:
            """catch the exception"""

            if not skip:
                # retry to find element one more time
                try:
                    element = self.driver.find_element(by, locator)
                except Exception as exp:
                    return None
                    pass

            # self.log.info("FAIL - " + assert_text)
            # self._screenShot()

        print("Wait For Element Displayed End")

        # return to the caller with element
        return element

    def double_click(self, element):
        """ double click on element """
        self.static_wait(.05)
        action = ActionChains(self.driver)
        action.double_click(element).perform()
        self.static_wait(.05)
        self.wait_for_action_complete()
        self.wait_for_page_load()

    def is_action_in_progress(self):
        return self.is_element_displayed(nRoboConfig.GlobalLocators.loader.value)

    def wait_for_action_complete(self, by: By = None, locator: str = None):

        print('\t\tWaitForActionCompleteStart')

        if nRoboConfig.GlobalLocators.action_complete_indicator_element.value[0] is not None \
                and nRoboConfig.GlobalLocators.action_complete_indicator_element.value[1] is not None:
            self.wait_till_invisibility_of_element_located(
                nRoboConfig.GlobalLocators.action_complete_indicator_element.value)

        self.static_wait(nRoboConfig.Waits.STATIC_WAIT.value)
        print('\t\tWaitForActionCompleteEnd')

    def ajax_length(self):
        # Get ajax length on the current page using javascript execute
        return self.driver.execute_script("return jQuery.ajax.length;")
        # self.wait_for_page_load()

    def wait_for_ajax_length(self, expected_ajax_length):
        # Not in use
        for counter in range(1, int(nRoboConfig.Waits.SLEEP_TIME.value) * 10 + 1, 1):
            self.static_wait(.10)
            actual_ajax_length = self.ajax_length()
            print("\n\n\n\n\nActual ajax count={}\n\n\n\n".format(actual_ajax_length))
            if actual_ajax_length == expected_ajax_length:
                return
            else:
                continue

    def is_alert_present(self, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(),
                                                      'Timed out waiting for alert popup to appear.')
            return True
        except TimeoutException:
            return False

    def accept_alert(self, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(),
                                                      'Timed out waiting for alert popup to appear.')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

    def dismiss_alert(self, timeout):
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present(),
                                                      'Timed out waiting for alert popup to appear.')
            alert = self.driver.switch_to.alert
            alert.dismiss()
        except TimeoutException:
            pass

    def get(self, url):

        self.static_wait(.10)
        self.driver.get(url)
        self.wait_for_page_load()
