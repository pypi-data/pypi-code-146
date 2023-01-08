from ...constants import Constants
from abc import ABC, abstractmethod 
from .i_get_option_type import IGetOptionType


class IAutomation(IGetOptionType, Constants, ABC):
    """
    This is an abstract class which is a skeleton for Automation operations 
    for generating differant Scripts and modules. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    @abstractmethod
    def auto_generate_modules(self, module_type_number: int, module_names_list: list) -> dict:
        """This method takes module type number for DYNAMIC_COMPONENTS dictionary and 
        module names list as parameter. With these two arguments generates modules. And
        will return a dictionary of new generated file paths (absolute path). © BS23"""
    
    def get_option_name_by_number(self, option_number: int) -> str:
        return self.DYNAMIC_COMPONENTS[option_number]
    
    