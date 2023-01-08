from .... import IoC_Container
from abc import ABC, abstractmethod
from .i_user_hander import IUserHandler
from bs4 import BeautifulSoup, NavigableString
from .i_locator_extractor import ILocatorExtractor
from .i_module_locator_writer import IModuleLocatorWriter
from .i_scrap_page_by_nav_route import IScrapPageByNavRoute
from .i_page_locator_operations_core import IPageLocatorOperationsCore


class IAutoNavLocatorHandler(IPageLocatorOperationsCore, IScrapPageByNavRoute, ILocatorExtractor, IUserHandler, ABC):
    """
    This is an abstract class which is a skeleton for dealing with Auto identification 
    and creation of Page-Locator Classes which are mentioned in the Navigation Bar. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        self.module_locator_writer_obj: IModuleLocatorWriter = self.ioc_container.resolve(IModuleLocatorWriter)
        self.user_handler_obj: IUserHandler = self.ioc_container.resolve(IUserHandler)
        self.scrap_page_by_nav_obj: IScrapPageByNavRoute = self.ioc_container.resolve(IScrapPageByNavRoute)
    
    @abstractmethod
    def nav_bar_identifier(self, html_body: BeautifulSoup, baseurl) -> dict:
        """
        This method is responsible for identifying Navigation bar from the html body 
        As there can be different types of Navigation. (created by the frontend engineer)
        This method will check all possible scenario to identy it.
        In return, there will be a dictionary where key will be identified page names and
        value will be also a dictionary which will hold their locators and tags from the NavBar
        © BS23
        """
    
    @abstractmethod
    def get_page_list_from_nav_bar(self, html_chunk: BeautifulSoup, target_list: list) -> dict:
        """
        After a successful identification from the nav_bar_identifier() method this method 
        is responsible for identifying all the possible page list which are hyperlinked or 
        routed in the nav-bar. All those will be enlisted in a dictionary where key will be 
        Page name and value will be the locator (Xpath, id, name etc.)
        © BS23
        """
    
    @abstractmethod
    def generate_page_classes(self, updated_page_list: list) -> str:
        """If the user want to generate Page classes from the identified Strings from Navigation Bar
        This method will take the updated page name list and create page classes and locator classes. © BS23"""
    
    @abstractmethod
    def find_tag_text_as_page_name(self, tag: BeautifulSoup) -> str:
        """This method will follow a specific mechanism which will try to find a specific text.
        That text may represent a meaningful page name. © BS23"""
            
    @abstractmethod
    def show_and_process_idetified_pages(self, nav_page_list: dict) -> dict:
        """
        This method will print all the elements in the list and will receive instructions (input) 
        from the user whether there are any elements to be omitted. User will give an index number
        as input and that element in that index will be removed. A full new updated list will be returned.
        © BS23
        """
    
    def delete_displayed_text(self, element):
        new_children = []
        for child in element.contents:
            if not isinstance(child, NavigableString):
                new_children.append(self.delete_displayed_text(child))
        element.contents = new_children
        return element
    
    
    
    
    
    