import os
from tests.robot.src import ObjMapper
from tests.robot.src.abstract.menu import Menu
from tests.robot.src.manager import RoboManager
# from tests.testdata.test_data_manager import TestDataManager

import logging

flag = False
try:
    from tests.testdata.test_data_manager import TestDataManager
    flag = True
except:
    logging.warning("POM Structure Not created, Please create pom structure first")


class Test23(Menu):
    """
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    #Add the initialized objects here.
    MANAGER_OPTIONS = {
        1: RoboManager(),
        2: TestDataManager() if flag else None,
    }
    
    banner = """
    -----------------------------------------------------------------------
    --------------------------------TEST-23--------------------------------
    -----------------------------------------------------------------------
    """
    
    option_menu = f"""
            [1] Robot
            [2] Data Manager
            [3] Exit
    """ if flag else """
            [1] Robot
            [3] Exit
    """

    def __init__(self):
        self.get_indexed()
        
    def get_indexed(self):
        ObjMapper.OBJ_MAP['root_manager'] = ObjMapper.remember(self) 
        
    def display(self):
        print(self.banner)
        print(self.option_menu)  
    
    def get_input(self):
        return super().get_input() 
    
    def switch_options(self, choice: int):
        if (choice == 0):
            print("=======================END=======================")
        else:
            manager = self.MANAGER_OPTIONS[choice]
            manager.menu()
            
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)

def main():
    print(os.path.dirname(__file__))
    try:
        test23 = Test23()
        test23.menu()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print(__package__)
    main()