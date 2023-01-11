from .bypass import bypass
from .recaptcha import Recapthca

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

def ouo():
    _, bypassed = bypass(Recapthca(), input('Enter url (https://ouo.io/...): '))
    if bypassed is not None:

        options = webdriver.FirefoxOptions()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(bypassed)

        driver.implicitly_wait(10)

        id_url = driver.find_element(By.XPATH, '//*[@id="idurl"]').get_attribute('value')
        id_filename = driver.find_element(By.XPATH, '//*[@id="idfilename"]').get_attribute('value')
        id_filesize = driver.find_element(By.XPATH, '//*[@id="idfilesize"]').get_attribute('value')

        driver.quit()

        conv_idurl = quote(id_url)
        conv_idfilename = quote(id_filename).replace(' ', '+')
        conv_idfilesize = id_filesize.replace(' ', '+')

        final_url = f'\033[92mhttps://download.megaup.net/?idurl={conv_idurl}&idfilename={conv_idfilename}&idfilesize={conv_idfilesize}\033[0m'
        print(final_url)
    else:
        print('Bypassed link could not be found.')