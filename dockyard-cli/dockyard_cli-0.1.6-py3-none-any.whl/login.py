import platform
from webdriver_setup import get_webdriver_for
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os

def get_auth_cookie(url):
    """Login to Dockyard"""

    host_type = platform.system()
    if host_type == "Darwin":
        profileDir = os.environ.get("HOME") + "/Library/Application Support/Google/Chrome/Default"
    elif host_type == "Linux":
        profileDir = os.environ.get("HOME") + "/.config/google-chrome/default"
    else:
        profileDir = os.environ.get("APPDATA") + "\\Google\\Chrome\\User Data\\Default"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + profileDir)
    driver = get_webdriver_for("chrome", options=options)
    driver.get(url)
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "dockyard")))
    cookie = driver.get_cookie('_oauth2_proxy')['value']
    driver.quit()

    return cookie

