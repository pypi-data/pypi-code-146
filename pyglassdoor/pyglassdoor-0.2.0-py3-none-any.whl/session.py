from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver


api = "https://www.glassdoor.com/graph"


def get_session_info() -> list[str]:
    """
    Generate header information for request session.
    This step is integrated in data queries and can be skipped.
    But if the user decides to reuse header information for multiple queries (e.g., to save time), then this query
    is to be used.

    :return: list: [cookie, token, user-agent]
    """
    cookie: str = ''
    token: str = ''
    user_agent: str = ''
    browser_options = webdriver.ChromeOptions()
    browser_options.add_argument('--headless')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=browser_options)

    browser.get('https://www.glassdoor.com/Reviews/Glassdoor-Reviews-E100431.htm')

    for request in browser.requests:
        if request.url == api:
            if request.headers.get('apollographql-client-name') == 'reviews':
                cookie = request.headers.get('cookie')
                token = request.headers.get('gd-csrf-token')
                user_agent = request.headers.get('user-agent')

    browser.close()
    return [cookie, token, user_agent]
