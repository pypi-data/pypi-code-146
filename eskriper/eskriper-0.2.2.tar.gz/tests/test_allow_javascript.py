from ..eskriper.selenium_driver import SeleniumDriver

driver = SeleniumDriver(headless=False)
driver.load('https://envonpetshop.b2b.cin7.com/login', '#EmailAddress')

def test_should_allow_javascript():
    assert driver.find_element('#EmailAddress')

def test_should_get_current_url():
    driver.load('https://www.python.org/')
    assert driver.driver.current_url == 'https://www.python.org/'