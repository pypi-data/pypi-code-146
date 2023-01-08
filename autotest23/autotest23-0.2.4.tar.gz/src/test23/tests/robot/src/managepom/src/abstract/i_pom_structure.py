from abc import ABC, abstractmethod
from .i_handler import IHandler

class IPOMStructure(IHandler, ABC):
    """
    This is an abstract class which is a skeleton for creating project architecture 
    accroding to Page Object Model design pattern. This will cover the Repository Structure only.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def operation(self, option_number: int = 0):
        self.generate_page_object_model()
        
    @abstractmethod
    def create_pom_structure(self, file_path: str, pom_root_base_path: str):
        """This method create Packages and Directories according to POM Design Pattern. © BS23"""
        
    def generate_page_object_model(self):
        """This method create Packages and Directories according to POM Design Pattern and 
        place Modules in the packages. © BS23"""
        try:
            self.create_pom_structure(self.POM_TEMPLATE_FILE_PATH, self.POM_ROOT_BASE_PATH)
            print(self.POM_GENERATE_SUCCESS_MESSAGE)
        except Exception as error:
            print(self.ERROR_UNKNOWN_MESSAGE)
            print("ERROR: ", error)