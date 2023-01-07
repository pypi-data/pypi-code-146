from abc import ABC, abstractmethod
from .i_handler import IHandler
from .i_get_option_type import IGetOptionType
from .i_pom_module_handler import IPOMModuleHandler
from .... import IoC_Container


class IModuleGenerator(IHandler, IGetOptionType, ABC):
    """
    This is an abstract class which is a skeleton for generating scripts and modules followed by
    their naming conventions and placing them accroding to the Page Object Model design pattern 
    to their dedicated packages. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self, module_interface_obj: IPOMModuleHandler) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        self.module_handler_obj = self.ioc_container.resolve(module_interface_obj)
    
    def operation(self, option_number: int = 0):
        self.generate_test_scenario(option_number)
    
    @abstractmethod
    def generate_module(self, module_name: str, pom_map_path: str, pom_module_map_path: str, root_path: str):
        """This method will take module sample name, POM map xml file path, POM module's map xml file path and Root base path of the Project.
        Then Auto generate script/ module files and write the source code also. © BS23"""
        
    def generate_test_scenario(self, option_number:int):
        """This method generates a test scenario class and the file name and class name will follow a specific order sequence (auto). © BS23"""
        try:
            option_type = self.get_option_name_by_number(option_number)
            self.generate_module(option_type, self.POM_TEMPLATE_FILE_PATH, self.POM_MODULE_TEMPLATE_FILE_PATH, self.POM_ROOT_BASE_PATH)
            print(self.TEST_SCENARIO_GENERATE_SUCCESS_MESSAGE)
        except Exception as error:
            print(self.ERROR_UNKNOWN_MESSAGE)
            print("ERROR: ", error)
            
    def get_option_name_by_number(self, option_number: int):
        return self.DYNAMIC_COMPONENTS[option_number]
