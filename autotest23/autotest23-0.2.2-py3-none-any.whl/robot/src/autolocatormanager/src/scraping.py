import os

from bs4 import BeautifulSoup
from .abstract.i_scraper import IScraper

try:
    from tests.drivercontroller.drivers.chrome import Chrome
# from path.drivercontroller.drivers.chrome import Chrome
except:
    pass

class Scraping(IScraper):
    """
    This class is responsible for dealing with web scraping and HTML content persing.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def scraper(self, automation_link = None) -> BeautifulSoup:
        payload = {
            "base_url": None,
            "html_content": None
        }
        user_targeted_link = self._get_user_tageted_link(automation_link)
        html_data = self._request_targeted_link(user_targeted_link)
        parser_type = "lxml" # https://lxml.de/tutorial.html
        scraper_content = self._html_parser(html_data, parser_type)
        payload["base_url"] = user_targeted_link
        payload["html_content"] = scraper_content
        return payload
    
    def _get_user_tageted_link(self, automation_link = None) -> str:
        user_targeted_link = automation_link
        if automation_link is None:
             user_targeted_link = input("Please, Provide the targeted link and press ENTER: ")
        user_targeted_link = self._link_validator(user_targeted_link)
        return user_targeted_link
    
    def _request_targeted_link(self, targeted_link: str) -> str:
        crome = Chrome()
        driver = crome.get_browser()
        driver.get(targeted_link)
        return driver.page_source
        # html_data = requests.get(targeted_link).text
        # return html_data

    
    def _html_parser(self, response_content, parser: str) -> BeautifulSoup:
        html_content = BeautifulSoup(response_content, parser)
        return html_content
