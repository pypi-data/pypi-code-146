from abc import ABC, abstractmethod
from typing import Any 
from .i_module_writer import IModuleWriter


class IModulevariableWriter(IModuleWriter, ABC):
    """
    This abstract class is designed as a skeleton for writing different codes and 
    declaring variables in the modules (.py). 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
        
    @abstractmethod
    def _declare_variables(self, scope: str, variables_access_modifiers: str, \
        indentation: int, variables_collection: dict) -> str:
        """Protected method which will take collection of variables and return 
        the whole structure as a multiline string. In the Parameter: 
        * Scope can be global/local, 
        * variables_access_modifiers can be public (+)/private (-)/protected (#), 
        * indentation will be white space count and 
        * variables_collection will be a dictionary where key will be 
            variable names and the value will be values of those variables 
        ©BS23"""
        
    @abstractmethod
    def _variable_name_converter(self,  variables_access_modifier: str, variable_name: str) -> str:
        """This Protected method will take a string as a parameter and will convert 
        it to variable naming convention. 
        This method will convert data set Key/Heading string into Snake Case (snake_case) 
        variable name according to PEP8 Standard.
        * If the variables_access_modifier is None/Null that will be considered as Public. 
        ©BS23"""
        
    @abstractmethod
    def _declare_single_variable(self, indentation: int, variable_name: str, \
        variable_data_type: Any, variable_value: Any) -> str:
        """This Protected method will operate for single variable. In the perameter section: 
        * Indentation is for maintaining the whitespace count.
        * And the last three parameter will be arranged in the following way 
            variable_name: variable_data_type = variable_value  
        ©BS23"""
        
    @abstractmethod
    def _data_type_identifier_by_value(self, variable_value: Any) -> Any:
        """This method will take variable value as parameter. 
        Then identify its type and return the type. ©BS23"""
    