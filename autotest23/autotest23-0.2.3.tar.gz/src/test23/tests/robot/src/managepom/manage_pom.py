"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from ..abstract.menu import Menu
from .. import ObjMapper
from .. import IoC_Container
from .src.abstract.i_pom_abstract_factory import IPOMAbstractFactory


class ManagePOM(Menu):
    """
    ManagePOM is a manager which is responisble for providing the services 
    of Page Object Model (POM) Design pattern according to the user request.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    banner = '''
    ------------------------------------------------------------------------
    -------------------- (POM) Page Object Model Manager--------------------
    ------------------------------------------------------------------------ 
    '''
    option_menu = '''
    [1] Create POM Structure
    [2] Create PageObject 
    [3] Create Test Scenario (Example: test_scenario_001.py) 
    [0] Exit
    '''
    
    def __init__(self) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        # Composition
        self.package_manager_obj = self.ioc_container.resolve(IPOMAbstractFactory)
    
    def get_indexed(self):
        ObjMapper.OBJ_MAP['pom_manager'] = ObjMapper.remember(self) 
        
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
            self.package_manager_obj.manage_operations(choice)
        # After a Successful operation getting back to current Menu for further actions
        self.menu()
    
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)
    
    
        