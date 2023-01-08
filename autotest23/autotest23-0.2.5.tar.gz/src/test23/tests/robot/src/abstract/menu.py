"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""

from abc import ABC, abstractmethod

class Menu(ABC):
    
    @abstractmethod
    def get_indexed(self):
        """
        ------------------------------------------------------------------------
        Here all the menu and sub-menu will get indexed. So those objects can be 
        re-used without making instance every time. Also, can avoid circular the
        dependency issue. © BRAIN STATION 23 
        ------------------------------------------------------------------------
        """
        pass
    
    @abstractmethod
    def display(self):
        """
        ------------------------------------------------------------------------
        Here all the text will be shown. Such as feature Banner, Menu Options & 
        other messages. © BRAIN STATION 23 
        ------------------------------------------------------------------------
        """
        pass
    

    @abstractmethod
    def get_input(self):
        """
        ------------------------------------------------------------------------
        This method will collect user input and return the input value to the 
        switch_options() method. © BRAIN STATION 23
        ------------------------------------------------------------------------
        """
        option = int(input("Please, provide an integer input and press Enter!:"))
        return option
    
    @abstractmethod
    def switch_options(self,choice: int):
        """
        ------------------------------------------------------------------------
        Here we will switch to the targeted destination according to the return
        value of get_input() method.
        Note: Try to follow Open-Closed principle. © BRAIN STATION 23 
        ------------------------------------------------------------------------
        """
        pass
    
    @abstractmethod
    def menu(self):
        """
        ------------------------------------------------------------------------
        This is the place where all the needed methods will be called for forming
        the menu section. © BRAIN STATION 23
        ------------------------------------------------------------------------
        """
        pass
