import os, subprocess, requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

class setup_shortcuts:
    '''Shortcut functions for Selenium'''
    def __init__(self, port=9222, wait_for=10, browser='chrome', executable_path='chromedriver'):
        try: # Check if Chrome is already started
            response = requests.get(f'http://localhost:{port}/json')
        except requests.exceptions.ConnectionError: # Otherwise, start Chrome
            system_drive = os.environ.get('SYSTEMDRIVE') # 'C:\'
            folders_chrome_could_be_installed_to = [
                os.environ.get('PROGRAMFILES'),
                os.environ.get('PROGRAMFILES(X86)'),
                os.environ.get('LOCALAPPDATA')
                ]
            possible_chrome_locations = []
            for folder in folders_chrome_could_be_installed_to:
                possible_chrome_locations.append(f'{folder}/Google/Chrome/Application/chrome.exe')
                possible_chrome_locations.append(f'{folder}/Chromium/Application/chrome.exe')

            for candidate in possible_chrome_locations:
                if os.path.exists(candidate):
                    subprocess.Popen([candidate, f'--remote-debugging-port={port}', f'--user-data-dir={os.getcwd()}/profile', '--start-maximized'])
                    sleep(1)
        
        options = uc.ChromeOptions()
        options.debugger_address = f'127.0.0.1:{port}' # Must be 127.0.0.1, not localhost
        if browser == 'uc':
            driver = uc.Chrome(options=options)
            os.kill(driver.browser_pid, 15) # undetected-chromedriver connects to the existing browser then starts a browser on a random port, this closes the random browser
        else:
            driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(wait_for) # Wait X seconds for element to load before raising error
        self.driver = driver
        self.wait_for = wait_for
        
    def find(self, css_selector, attribute=None, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        if attribute:
            attribute = element.get_attribute(attribute)
            return element, attribute
        return element

    def finds(self, css_selector, parent=None, wait_for=None):
        if not parent:
            parent = self.driver
        if wait_for:
            self.driver.implicitly_wait(wait_for)
        elements = parent.find_elements(By.CSS_SELECTOR, css_selector)
        if wait_for:
            self.driver.implicitly_wait(self.wait_for)
        return elements

    def click(self, css_selector, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        element.click()

    def text(self, css_selector, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        return element.text

    def send(self, css_selector, text, clear=False, parent=None):
        if not parent:
            parent = self.driver
        element = parent.find_element(By.CSS_SELECTOR, css_selector)
        if clear:
            element.clear()
        element.send_keys(text)
    
    def get(self, url, check_current_url=True, parent=None):
        if not parent:
            parent = self.driver
        if not check_current_url or parent.current_url != url:
            parent.get(url)

    def check(self, css_selector, parent=None):
        if not parent:
            parent = self.driver
        self.driver.implicitly_wait(1)
        elements = parent.find_elements(By.CSS_SELECTOR, css_selector)
        self.driver.implicitly_wait(self.wait_for)
        if elements and elements[0].is_displayed():
            return elements
        else:
            return None