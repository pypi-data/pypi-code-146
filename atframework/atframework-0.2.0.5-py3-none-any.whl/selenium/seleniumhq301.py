"""
Created on Mar 02, 2021

@author: Siro

"""

import os
import time
import platform

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import \
    expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support.ui import Select

from atframework.selenium.taiji import Taiji
from atframework.drivers.drivers_settings import DriversSettings
from atframework.tools.log.config import logger
from atframework.utils.utils import Utils

class Seleniumhq301(Taiji):
    """
    Set environment information while creating instance
    """
    utils = Utils()

    def __init__(self):
        logger.info('[AtLog] ----- init Seleniumhq301')
        self.browser = None

    def __del__(self):
        pass

    def is_linux_system(self):
        return 'Linux' in platform.system()

    def is_windows_system(self):
        return 'Windows' in platform.system()

    def is_mac_system(self):
        return 'Darwin' in platform.system()

    '''
    At first: Open browser, default open browser via firefox.
    '''

    def _open_browser(self, browser_name):
        self.browser = None
        if 'safari' == browser_name:
            browser = webdriver.Safari()
        elif 'chrome' == browser_name:
            if self.is_mac_system() is True:
                # print("current is Mac system")
                # Local testing will use following codes at sometimes.
                # browser = webdriver.Chrome(
                #     executable_path=os.path.abspath(os.path.join(os.getcwd(), "../..")) + DriversSettings.LOCAL_MAC_CHROME_DRIVER)
                browser = webdriver.Chrome(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_MAC_CHROME_DRIVER)
            elif self.is_windows_system() is True:
                # print("current is Windows system")
                browser = webdriver.Chrome(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_WINDOWS_CHROME_DRIVER)
            else:
                browser = webdriver.Remote(
                    options=webdriver.ChromeOptions(),
                    command_executor=DriversSettings.REMOTE_CHROME_DRIVER)
                # ,
                # desired_capabilities=DesiredCapabilities.CHROME)
        else:
            if self.is_mac_system() is True:
                browser = webdriver.Firefox(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_MAC_FIREFOX_DRIVER)
            elif self.is_windows_system() is True:
                # print("current is Windows system")
                browser = webdriver.Firefox(
                    executable_path=os.path.dirname(os.__file__) +
                    DriversSettings.LOCAL_WINDOWS_FIREFOX_DRIVER)
            else:
                browser = webdriver.Remote(
                    options=webdriver.FirefoxOptions(),
                    command_executor=DriversSettings.REMOTE_FIREFOX_DRIVER)
                # ,
                # desired_capabilities=DesiredCapabilities.FIREFOX)

        self.browser = browser
        return self.browser

    '''
    Finally: Close browser
    '''

    def _close_browser(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
            #             __instance = None
            logger.info('[AtLog] ----- set the browser and instance to None')
        else:
            logger.info('[AtLog] ----- the browser is None')

    '''
    scroll browser to target id
    '''

    def _scroll_browser_to_id(self, link_id):
        target = self.browser.find_element_by_id(link_id)
        self.browser.execute_script("arguments[0].scrollIntoView();", target)

    '''
    scroll browser to target element by css
    '''

    def _scroll_browser_to_element_by_css(self, css_selector):
        target = self.browser.find_element_by_css_selector(css_selector)
        self.browser.execute_script("arguments[0].scrollIntoView();", target)

    '''
    scroll browser to target element by xpath
    '''

    def _scroll_browser_to_element_by_xpath(self, xpath):
        target = self.browser.find_element_by_xpath(xpath)
        self.browser.execute_script("arguments[0].scrollIntoView();", target)

    '''
    click DOEN from css element
    '''

    def _scroll_down_by_key_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).send_keys(Keys.DOWN)

    '''
    click UP from css element
    '''

    def _scroll_up_by_key_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).send_keys(Keys.UP)

    '''
    refresh the current page.
    '''

    def _refresh_page(self):
        # self.browser.execute_script("location.reload()")
        self.browser.refresh()

    '''
    click Specific Link By css_selector
    '''

    def _click_link_by_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    click Specific Link By xpath
    '''

    def _click_link_by_xpath(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    '''
    access website
    '''
    def _access_website(self, site_address):
        self.browser.get(site_address)

    '''
    access website until loading time
    '''

    def _access_website_till_one_time(self, site_address):
        self.browser.implicitly_wait(15)  # seconds
        self.browser.get(site_address)

    '''
    click Text Field By CSS
    '''

    def _type_in_text_field_by_css(self, field_css, input_text):
        elem = self.browser.find_element_by_css_selector(field_css)
        elem.send_keys(input_text)

    '''
    click Text Field By xpath
    @param element - css_selector
    '''
    def _type_in_text_field_by_xpath(self, xpath, input_text):
        elem = self.browser.find_element_by_xpath(xpath)
        elem.send_keys(input_text)

    '''
    click Specific button by CSS and javascript
    @param element - css_selector
    '''

    def _click_element_by_css_script(self, css_selector):
        element = self.browser.find_element_by_css_selector(css_selector)
        self.browser.execute_script("arguments[0].click()", element)

    '''
    click element by locator
    @param element - text, locator
    '''

    def _click_element_by_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    find Specific Link By css
    '''

    def _find_link_by_css(self, css_selector):
        try:
            if self.browser.find_element_by_css_selector(
                    css_selector).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    Click Element By XPath
    @param element - XPath
    '''

    def _click_element_by_xpath(self, xpath):
        self.browser.find_element_by_xpath(xpath).click()

    '''
    Click Element By link_text
    @param element - link_text
    '''

    def _click_element_by_link_text(self, link_text):
        self.browser.find_element_by_link_text(link_text).click()

    '''
    Click Element By partial_link_text
    @param element - partial_link_text
    '''

    def _click_element_by_partial_link_text(self, partial_link_text):
        self.browser.find_element_by_partial_link_text(partial_link_text).click()


    '''
    If there are some same element on the page, click Specific Button By index (index start form 1)
    @param element - css_selector
    '''
    def _click_element_in_list_via_css(self, css_selector, index):
        elements_list = self.browser.find_elements_by_css_selector(css_selector)
        elements_list[index].click()

    '''
    If there are some same element on the page, click Specific Button By index (index start form 1)
    @param element - xpath
    '''
    def _click_element_in_list_via_xpath(self, xpath, index):
        elements_list = self.browser.find_elements_by_xpath(xpath)
        elements_list[index].click()

    '''
    wait for id shown and sleep 2s.
    @param element - id_name, wait_time, sleep_time
    '''

    def _wait_for_id_shown_and_sleep_2s(self,
                                        id_name,
                                        wait_time=60,
                                        sleep_time=2):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.ID, id_name)))
        time.sleep(sleep_time)

    '''
    pause by time.sleep method
    @param - wait_seconds
    '''

    def _pause(self, wait_seconds):
        time.sleep(wait_seconds)

    '''
    wait for css shown and sleep default 5s.
    @param element - css_selector, wait_time, sleep_time
    '''

    def _wait_for_css_shown_and_sleep(self,
                                      css_selector,
                                      wait_time=60,
                                      sleep_time=5):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        time.sleep(sleep_time)

    '''
    Wait for xpath shown and sleep default 5s.
    @param element - xpath, wait_time, sleep_time
    '''

    def _wait_for_xpath_shown_and_sleep(self,
                                        xpath,
                                        wait_time=60,
                                        sleep_time=5):
        WebDriverWait(self.browser, wait_time).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(sleep_time)

    '''
    Wait 2 mins for xpath shown and sleep default 2s.
    @param element - xpath, wait_time, sleep_time
    '''

    def _wait_for_xpath_shown2_and_sleep(self,
                                         xpath,
                                         wait_time=120,
                                         sleep_time=2):
        # WebDriverWait(self.browser, wait_time).until(lambda x: x.find_element_by_xpath(xpath))
        element = WebDriverWait(
            self.browser,
            wait_time).until(lambda x: x.find_element_by_xpath(xpath))
        time.sleep(sleep_time)
        if element:
            return True
        else:
            return False

    '''
    Wait for CSS shown and click.
    @param element -  wait_time, CSS
    '''

    def _wait_for_css_shown_and_click(self, css_selector, wait_time=60):
        self.browser.implicitly_wait(wait_time)
        self.browser.find_element_by_css_selector(css_selector).click()

    '''
    Get elements's URL By Text
    @param element - link_text
    '''

    def _get_element_url_by_text(self, link_text):
        return self.browser.find_element_by_link_text(link_text).get_attribute(
            "href")

    '''
    Get Text By CSS
    @param element - css locator
    '''

    def _get_text_by_css(self, css_selector):
        return self.browser.find_element_by_css_selector(css_selector).text

    '''
    Get Text By XPath
    @param element - XPath
    '''

    def _get_text_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath).text

    '''
    find Specific Link By Text
    '''

    def _find_link_by_text(self, link_text):
        try:
            if self.browser.find_element_by_link_text(
                    link_text).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    find Specific Link By css
    '''
    def _find_element_by_css(self, css_selector):
        try:
            if self.browser.find_element_by_css_selector(css_selector).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    find element by partial link text
    '''

    def _find_element_by_partial_link_text(self, partial_link_text):
        try:
            if self.browser.find_element_by_partial_link_text(
                    partial_link_text).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    find Specific element By xpath
    '''

    def _find_element_by_xpath(self, xpath):
        try:
            if self.browser.find_element_by_xpath(
                    xpath).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    find Specific Link By xpath
    '''

    def _find_link_by_xpath(self, xpath):
        try:
            if self.browser.find_element_by_xpath(
                    xpath).is_displayed():
                return True
            else:
                return False
        except NoSuchElementException:
            return False

    '''
    click Text Field By XPath and click Enter on keyborad
    '''

    def _type_in_text_field_by_xpath_and_click_enter(self, field_xpath,
                                                     input_text):
        elem = self.browser.find_element_by_xpath(field_xpath)
        elem.send_keys(input_text, Keys.ENTER)

    '''
    Select Element by value in DropMenu
    @param element - xpath/css_selector, value
    '''

    def _select_dropdown_menu_element_by_value(self, locator, value):
        if self.utils.is_xpath(locator) is True:
            elem = self.browser.find_element_by_xpath(locator)
            Select(elem).select_by_value(value)
        else:
            elem = self.browser.find_element_by_css_selector(locator)
            Select(elem).select_by_value(value)

    '''
    Select Element by text in DropMenu
    @param element - locator, text
    '''

    def _select_dropdown_menu_element_by_text(self, locator, text):
        if self.utils.is_xpath(locator) is True:
            elem = self.browser.find_element_by_xpath(locator)
            Select(elem).select_by_visible_text(text)
        else:
            elem = self.browser.find_element_by_css_selector(locator)
            Select(elem).select_by_visible_text(text)

    '''
    Return The first selected option in this select tag (or the currently selected option in a normal select)
    @param element - locator
    '''

    def _get_first_or_current_selected_dropdown_menu_option_text(self, locator):
        if self.utils.is_xpath(locator) is True:
            elem = self.browser.find_element_by_xpath(locator)
            return Select(elem).first_selected_option.text
        else:
            elem = self.browser.find_element_by_css_selector(locator)
            return Select(elem).first_selected_option.text

    '''
    If there are some same elements on the page, find whether has expected text on these elements.
    @param element - expected_text
    '''
    def _is_expected_text_in_elements(self, expected_text):
        elements_list = self.browser.find_elements_by_xpath('//*[contains(text(),"'+expected_text+'")]')
        #elements_list = self.browser.find_elements_by_xpath('//h5[contains(.,"'+expected_text+'")]')
        if len(elements_list) > 0:
            return True
        else:
            return False

    '''
    Get Value By XPath
    @param element - XPath
    '''
    def _get_value_by_xpath(self, xpath):
        return self.browser.find_element_by_xpath(xpath).get_attribute('value')


    '''
    Clear text by xpath in text field
    @param element - xpath
    '''
    def _clear_text_field_by_xpath(self, xpath):
        self.browser.find_element_by_xpath(xpath).clear()

    '''
    Clear text by css_selector in text field
    @param element - locator
    '''
    def _clear_text_field_by_css(self, css_selector):
        self.browser.find_element_by_css_selector(css_selector).clear()

    '''
     Clear text by xpath in text field and send Enter
     @param element - xpath
     '''
    def _clear_text_field_by_xpath_and_enter(self, xpath):
        elem = self.browser.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(Keys.ENTER)

    '''
    Delete all cookies
    '''

    def _delete_all_cookies(self):
        self.browser.delete_all_cookies()

    '''
    Get cookies
    '''

    def _get_cookies(self):
        self.browser.get_cookies()

    '''
    Add cookies
    @param element - cookie_dict
    '''

    def _add_cookie(self, cookie_dict):
        self.browser.add_cookie(cookie_dict)

