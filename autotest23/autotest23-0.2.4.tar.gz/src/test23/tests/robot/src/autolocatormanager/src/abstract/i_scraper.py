import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup 


class IScraper(ABC):
    """
    This is an abstract class which is a skeleton for dealing with web scraping 
    and html parsing.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    URL_VALIDATOR_CHAR = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    """This is a constant for checking string to identify valid URL. © BS23"""
    
    @abstractmethod
    def scraper(self, automation_link = None) -> BeautifulSoup:
        """
        This method is the place where all the web scraping operations will take place. 
        © BS23
        """
    
    @abstractmethod
    def _get_user_tageted_link(self, automation_link = None) -> str:
        """
        This method will take a link/ URL as user input. 
        © BS23
        """
    
    @abstractmethod
    def _request_targeted_link(self, targeted_link: str) -> str:
        """
        This method will take a link/ URL as parameter and will return 
        the http response content from that link/ URL. 
        © BS23
        """
    
    @abstractmethod
    def _html_parser(self, response_content, parser:str) -> BeautifulSoup:
        """
        This method will take response content (HTML) and parser name as parameter and 
        return the content as BeautifulSoup data type. 
        # html.parser is the dafault python parser
        # lxml is 3rd party but faster than the default.
        # html5lib is a parser which the web browser use. (This is very slow but good)
        # xml is also a parser
        # lxml-xml better parser #https://lxml.de/
        © BS23
        """
        
    def _link_validator(self, link: str) -> str:
        """
        This method will take a string as parameter and validate that 
        string is a valid link/ URL or not. 
        © BS23
        """
        if re.match(self.URL_VALIDATOR_CHAR, link) is None:
            raise Exception("""
                            ****************************************
                            |||>>>>>>This URL is not valid!<<<<<<|||
                            ****************************************
                            """)
        return link