"""
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from .abstract.i_pom_abstract_factory import IPOMAbstractFactory


class PackageManager(IPOMAbstractFactory):
    """
    PackageManager is a composition based service which holds all nacessary objects and 
    its functions which are useful during working in the Page Object Model (POM) Design Pattern.
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """
    
    def manage_operations(self, operation_type: int):
        obj = self.return_factory_demand(operation_type)
        obj.operation(operation_type)
        
    