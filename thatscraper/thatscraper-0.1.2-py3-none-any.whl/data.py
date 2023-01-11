from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# for typing
WebElement = webdriver.remote.webelement.WebElement


class BrowserCleaner:
    """
     Browser cache and history cleaner

    Base class for a browser cleaning
    """
    def __init__(self, headless=True) -> None:
        self.headless = headless

    def get_shadow(self, element: WebElement):
        root = self.driver.execute_script(
            'return arguments[0].shadowRoot.children',
            element
        )
        return root


class FirefoxCleaner(BrowserCleaner):
    def __init__(self,
                 headless=True,
                 settings="about:preferences#privacy") -> None:
        super().__init__(headless)
        options = webdriver.firefox.options.Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)
        self.settings = settings

    def clear_data(self, timeout=10):
        self.driver.get(self.settings)
        button = self.driver.find_element(
            By.ID,
            "clearSiteDataButton"
        )
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.element_to_be_clickable(button)).click()
        wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.CLASS_NAME, "dialogFrame")
        ))
        dialog = self.driver.find_element(By.TAG_NAME, "dialog")
        shadow_root = self.get_shadow(dialog)
        clear_button = shadow_root[3].find_element(
            By.CSS_SELECTOR,
            '.dialog-button-box > button:nth-child(7)'
        )
        wait.until(
            EC.element_to_be_clickable(clear_button)
        ).click()
        wait.until(EC.alert_is_present())
        alert = Alert(self.driver)
        alert.accept()
        self.driver.quit()


# to be implemented
class ChromeCleaner(BrowserCleaner):
    def __init__(self,
                 headless=True,
                 settings="chrome://settings/privacy") -> None:
        super().__init__(headless)
        # options = webdriver.chrome.options.Options()
        # options.headless = headless
        # self.driver = webdriver.Chrome(options=options)
        # self.settings = settings

    # def clear_data(self, timeout=10):
    #     self.driver.get(self.settings)
    #     # button = self.driver.find_element(
    #     #     By.ID,
    #     #     "clearSiteDataButton"
    #     # )
    #     # wait = WebDriverWait(self.driver, timeout)
    #     # wait.until(EC.element_to_be_clickable(button)).click()
    #     # wait.until(EC.frame_to_be_available_and_switch_to_it(
    #     #     (By.ID, "dialogFrame")
    #     # ))
    #     # dialog = self.driver.find_element(By.TAG_NAME, "dialog")
    #     # shadow_root = self.get_shadow(dialog)
    #     # clear_button = shadow_root[3].find_element(
    #     #     By.CSS_SELECTOR,
    #     #     '.dialog-button-box > button:nth-child(7)'
    #     # )
    #     # wait.until(
    #     #     EC.element_to_be_clickable(clear_button)
    #     # ).click()
    #     # wait.until(EC.alert_is_present())
    #     # alert = Alert(self.driver)
    #     # alert.accept()
    #     self.driver.quit()


# to be implemented
class EdgeCleaner(BrowserCleaner):
    def __init__(self,
                 headless=True,
                 settings="chrome://settings/privacy") -> None:
        super().__init__(headless)


# to be implemented
class SafariCleaner(BrowserCleaner):
    def __init__(self,
                 headless=True,
                 settings="chrome://settings/privacy") -> None:
        super().__init__(headless)


Cleaner = {
    'firefox': FirefoxCleaner,
    'chrome': ChromeCleaner,
    'Egde': EdgeCleaner,
    'Safari': SafariCleaner
}
