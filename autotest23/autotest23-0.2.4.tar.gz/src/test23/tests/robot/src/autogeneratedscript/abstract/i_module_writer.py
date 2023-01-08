from abc import ABC, abstractmethod 


class IModuleWriter(ABC):
    """
    This abstract class is a skeleton for writing different codes in the modules. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    @abstractmethod
    def module_code_writer(self, module_path: str, module_code: dict, is_override=None):
        """This public method will take module path (String) and module code and python dictionary
        as parameter and write it in the module ordered by their components from the dictionary keys. ©BS23"""