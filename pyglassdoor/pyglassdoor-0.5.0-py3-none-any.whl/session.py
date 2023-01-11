from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from typing import Optional

api = "https://www.glassdoor.com/graph"


def get_session_info() -> dict:
    """ Generate header information for request session.

        This step is integrated in data queries and can be skipped.
        But if the user decides to reuse header information for multiple queries (e.g., to save time), then this query
        is to be used.

        :return: session information required for an authorized query
        :rtype: dict
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
    return dict(cookie=cookie, token=token, user_agent=user_agent)


def get_session_headers(session_info: Optional[dict] = None) -> dict:
    """Returns header information for requests

            :param session_info: dictionary that contains active session information
            :type session_info: dict, optional
            :return:
            :rtype: dict

    """
    if not session_info:
        session_info = get_session_info()

    headers = {
        "cookie": session_info['cookie'],
        "authority": "www.glassdoor.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,fa;q=0.8",
        "apollographql-client-name": "reviews",
        "apollographql-client-version": "7.14.12",
        "content-type": "application/json",
        "dnt": "1",
        "gd-csrf-token": session_info['token'],
        "origin": "https://www.glassdoor.com",
        "referer": "https://www.glassdoor.com/",
        "user-agent": session_info['user_agent']
    }

    return headers
