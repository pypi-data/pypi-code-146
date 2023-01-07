"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""

from .abstract.menu import Menu
from .passwordmanager.password_manager import PasswordManager
from .managepom.manage_pom import ManagePOM
from .autolocatormanager.auto_locator_manager import AutoLocatorManager
from . import ObjMapper


class RoboManager(Menu):
    
    banner = """
    ------------------------------------------------------------------------
    ----------------------Django Automation-QA Manager----------------------
    ------------------------------------------------------------------------ 
    """
    
    option_menu = '''
    [1] POM Manager
    [2] Tester Account (Password Manager)
    [3] Auto Generated Page and locator classes from a Base URL
    [4] Design Automation Test Report
    [5] Run Automation (pytest.ini) 
    [6] View Basic Standards
    [7] Run pytest by marker (pytest -m maker_name)
    [0] Back
    '''
    
    #Add the initialized objects here.
    MANAGER_OPTIONS = {
        1: ManagePOM(),
        2: PasswordManager(),
        3: AutoLocatorManager()
    }
    
    def __init__(self):
        self.get_indexed()
    
    def get_indexed(self):
        ObjMapper.OBJ_MAP['robo_manager'] = ObjMapper.remember(self) 
        
    def display(self):
        print(self.banner)
        print(self.option_menu)       
        
    def get_input(self):
        return super().get_input()
    
    def switch_options(self, choice: int):
        if (choice == 0):
            id = ObjMapper.OBJ_MAP['root_manager']
            route = ObjMapper.id2obj(id)
            route.menu()
            return None
        else:
            #Getting sub menu object by option number. 
            sub_menu_obj: Menu = self.MANAGER_OPTIONS[choice]
            #Open-Closed Principle
            #https://www.pythontutorial.net/python-oop/python-open-closed-principle/
            sub_menu_obj.menu()
    
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)
        