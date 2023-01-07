from abc import ABC, abstractmethod
from .i_handler import IHandler
from .i_pom_structure import IPOMStructure
from .... import IoC_Container


class IPOMModuleHandler(IHandler, ABC):
    """
    This is an abstract class which is a skeleton for placing scripts and modules accroding to the
    Page Object Model design pattern to their dedicated packages. 
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def __init__(self, pom_structure_interface_obj: IPOMStructure) -> None:
        self.ioc_container = IoC_Container.CONTAINER
        self.package_handler_obj = self.ioc_container.resolve(pom_structure_interface_obj)
        # As Scripts and Modules can not be placed before the full Page Object Model (POM) Structure gets created. 
        # So Dependency Injection is used here to serve that purpose before ModuleHandler starts its operation. 
    
    def operation(self, option_number: int = 0):
        self.package_handler_obj.operation()
        self.generate_page_object_model()
         
    @abstractmethod
    def create_pom_modules(self, pom_map_path: str, pom_module_map_path: str,custom_module_path: str, pom_root_base_path: str):
        """This method place all the Modules in the packages according to the POM map from pom.xml file. © BS23"""
        
    def generate_page_object_model(self):
        """This method create Packages and Directories according to POM Design Pattern and 
        place Modules in the packages. © BS23"""
        try:
            self.create_pom_modules(self.POM_TEMPLATE_FILE_PATH, self.POM_MODULE_TEMPLATE_FILE_PATH, \
                self.POM_CUSTOM_MODULE_PATH, self.POM_ROOT_BASE_PATH)
            print(self.POM_PLACEMENT_SUCCESS_MESSAGE)
        except Exception as error:
            print(self.ERROR_UNKNOWN_MESSAGE)
            print("ERROR: ", error)