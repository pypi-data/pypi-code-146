from abc import ABC, abstractmethod
from .i_scraper import IScraper
from bs4 import BeautifulSoup 


class IScrapPageByNavRoute(ABC):
    """ This abstract class holds the design of scraping a specific page which will be 
    routed from the Navigation Bar. Here routing locator will be used for this navigation operation.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)"""
    
    def __init__(self, web_scraper: IScraper) -> None:
        self.web_scraper_obj: IScraper = web_scraper
        
    @abstractmethod
    def scrap_targeted_page(self, base_url: str, locators_and_tags: dict) -> dict:
        """This method will take base URL and routing path as a parameter and Web Scrap
        that visited pages and return the HTML body section as BeautifulSoup element.
        For return type the payload will be, 
        Example:
        {
            'Example Page': {
                'page_payload': {
                    'base_url': 'example.com/demo', 
                    'html_content': BeautifulSoup,
                }
            }
        }
        ©BS23"""
        
    @abstractmethod
    def _get_routing_link(self, base_url: str, locators_and_tags: dict) -> str:
        """This method takes a dictionary as a parameter where it will extract values of the 'tag' key
        and then will get the inner routing element (Example: href attribute value) and return it as a String. ©BS23"""