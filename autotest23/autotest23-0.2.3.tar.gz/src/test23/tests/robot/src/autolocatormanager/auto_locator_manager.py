from .. import ObjMapper
from .. import IoC_Container
from ..abstract.menu import Menu
from .src.abstract.i_scraper import IScraper
from .src.abstract.i_auto_nav_locator_handler import IAutoNavLocatorHandler
from .src.abstract.i_page_locator_operations_core import IPageLocatorOperationsCore

class AutoLocatorManager(Menu):
    
    banner = """
    ------------------------------------------------------------------------
    ----------------------------Auto Locator Manager----------------------------
    ------------------------------------------------------------------------ 
    """
    
    option_menu = """
    [1] Analyze Navigation Bar and identify Pages
    [2] Find locators for a single page 
    [0] Back
    """
    
    LOCATOR_MANAGER_OPTIONS = {
        1: IAutoNavLocatorHandler,
        2: IAutoNavLocatorHandler
    }
    """This constant dictionary holds all the needed Abstract classes as Container Referance.
    After user input IoC Container will help to create the instance of the following class."""
    
    def get_indexed(self):
        ObjMapper.OBJ_MAP['locator_manager'] = ObjMapper.remember(self) 
        
    def display(self):
        print(self.banner)
        print(self.option_menu)       
        
    def get_input(self):
        return super().get_input()
    
    def switch_options(self, choice: int):
        if choice == 0:
            id = ObjMapper.OBJ_MAP['robo_manager']
            route = ObjMapper.id2obj(id)
            route.menu()
            return None
        else:
            # Getting IoC Container
            ioc_container = IoC_Container.CONTAINER
            # Creating Scraper class instance
            web_scrapping: IScraper = ioc_container.resolve(IScraper)
            # Getting user defined Class as Scraper Option
            container_referance = self.LOCATOR_MANAGER_OPTIONS[choice]
            # Creating user defined Class's instance
            page_locator: IPageLocatorOperationsCore = ioc_container.resolve(container_referance)
            # Getting HTML Content from the Scraper instance methods
            payload = web_scrapping.scraper()
            # Proceeding to Auto Locator identification operations from the HTML content
            if choice == 1:
                page_locator.page_element_identifier_and_writer(payload=payload)

            else:
                page_locator.single_page_element_identifier(payload=payload)
        # After a Successful operation getting back to current Menu for further actions
        self.menu()
        
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)