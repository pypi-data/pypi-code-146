"""
Created on Mar 02, 2021

@author: Siro

"""


class DriversSettings(object):
    """
    some settings for driver
    """
    LOCAL_LINUX_CHROME_DRIVER = '/site-packages/atframework/drivers/chromedriver-linux64'
    LOCAL_MAC_CHROME_DRIVER = '/site-packages/atframework/drivers/chromedriver'
    # local testing will use the following codes at sometimes.
    # LOCAL_MAC_CHROME_DRIVER = '/atwork/atframework/drivers/chromedriver'
    LOCAL_WINDOWS_CHROME_DRIVER = '/site-packages/atframework/drivers/chromedriver.exe'
    LOCAL_MAC_FIREFOX_DRIVER = '/site-packages/atframework/drivers/geckodriver'
    LOCAL_LINUX_FIREFOX_DRIVER = '/site-packages/atframework/drivers/geckodriver-linux64'
    LOCAL_WINDOWS_FIREFOX_DRIVER = '/site-packages/atframework/drivers/geckodriver.exe'
    REMOTE_CHROME_DRIVER = 'http://selenium__standalone-chrome:4444/wd/hub'
    REMOTE_FIREFOX_DRIVER = 'http://selenium__standalone-firefox:4444/wd/hub'
