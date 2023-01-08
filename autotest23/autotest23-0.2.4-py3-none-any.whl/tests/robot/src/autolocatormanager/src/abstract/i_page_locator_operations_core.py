from abc import ABC


class IPageLocatorOperationsCore(ABC):
    """
    This is an abstract class which is a skeleton for dealing with Auto identification 
    of a page elements and their locators. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """

    def page_element_identifier_and_writer(self, payload: dict):
        """
        This method is responsible for managing all the operations on the html body, 
        which will be received as parameter. This method will check all possible 
        scenario to identy the locators of most commonly used html elements.
        * In the parameter this method will receive a payload.
        * Payload structure will be:
            {
                "base_url": "www.example.com",
                "html_content": BeautifulSoup=>Element,
            } 
        © BS23
        """