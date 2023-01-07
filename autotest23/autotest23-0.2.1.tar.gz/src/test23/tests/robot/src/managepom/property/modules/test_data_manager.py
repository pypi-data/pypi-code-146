"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
import os
import sys
from os.path import dirname as up

two_up = up(up(__file__))
# append the path of the parent directory
sys.path.append(two_up)
#print (os.getcwd())
# from robot.src import ObjMapper
from robot.src.abstract.menu import Menu
from testdata.xl.xl_test_data import XLtestData
from testdata.xl.sample import Sample

class TestDataManager(Menu):
    
    banner = """
    ------------------------------------------------------------------------
    ------------------Data Set Manager (Data Driven Test) ------------------
    ------------------------------------------------------------------------ 
    """
    
    option_menu = '''
    [1] EXCEL 
    [2] CSV
    [3] SQL
    [4] Sample
    '''
    
    #Add the initialized objects here.
    OPTION_TYPES = {
        1: XLtestData(),
        4: Sample()
    }
    
    def get_indexed(self):
        return super().get_indexed()
        
    def display(self):
        print(self.banner)
        print(self.option_menu)       
        
    def get_input(self):
        option = int(input("Please, provide an integer input and press Enter!:"))
        return option
    
    def switch_options(self, choice: int):
        data_set_obj = self.OPTION_TYPES[choice]
        #Open-Closed Principle
        #https://www.pythontutorial.net/python-oop/python-open-closed-principle/
        print(data_set_obj.arrange_data_set("vertical"))
    
    def menu(self):
        self.display()
        choice = self.get_input()
        self.switch_options(choice)