import webbrowser

# def selenium_scrapper():
#     # selenium 4
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.firefox.service import Service as FirefoxService
#     from webdriver_manager.firefox import GeckoDriverManager
#
#     driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
#     driver.get(f'https://google.com')
#     title = driver.title
#     print(title)
#     links = driver.find_elements(By.TAG_NAME, "a")
#     for ln in links:
#         print(ln.get_property('href'))
#     print(f'{len(links)} links found')
#     driver.quit()


def open_browser(self):
    # TODO: check installation. Offer installation
    browsers = {
        "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "chromium": "C:\\Program Files (x86)\\chromium-win\\chrome-win\\chrome.exe",
        "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
        "opera": "C:\\Users\\rhleon\\AppData\\Local\\Programs\\Opera\\launcher.exe"
    }
    # To register
    for br_name, br_path in browsers.items():
        webbrowser.register(br_name, None, webbrowser.BackgroundBrowser(br_path))

    # To open
    for browser in browsers:
        webbrowser.get(browser).open('http://www.google.com')
