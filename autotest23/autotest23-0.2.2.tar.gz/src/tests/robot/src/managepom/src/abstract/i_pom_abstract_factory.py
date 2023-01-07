from abc import ABC, abstractmethod
from .... import IoC_Container
from .i_handler import IHandler
from .i_module_generator import IModuleGenerator
from .i_pom_module_handler import IPOMModuleHandler


class IPOMAbstractFactory(ABC):
    """
    This is an abstract class which is a skeleton for working around a 
    super-factory which creates other factories.In a word this is an abstract 
    class which will act as Abstract Factory.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    OPERATIONS_DICT = {
        1: IPOMModuleHandler,
        2: IModuleGenerator,
        3: IModuleGenerator,
    }
    
    @abstractmethod
    def manage_operations(self, operation_type: int):
        """This method is responsible for redirecting Handler type concrete class objects according to user integer input. © BS23"""
        
    def return_factory_demand(self, operation_type: int) -> IHandler:
        """Call this method from manage_operations method. This will take integer 
        as parameter and return IHandler data type object © BS23"""
        ioc_container = IoC_Container.CONTAINER
        ioc_id_interface: IHandler = self.OPERATIONS_DICT[operation_type]
        ioc_obj_ref = ioc_container.resolve(ioc_id_interface)
        return ioc_obj_ref