from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def unloadObjects(cls, objsToUnload: List[BusinessObject]) -> ServiceData:
        """
        This operation unloads Business Objects. If input contains one or more Business Objects then it will call
        AOM_unload for each object otherwise it will call unloadAll  to unload all the objects. 
        
        Note that unloadAll will unload both C++ along with POM objects.
        """
        return cls.execute_soa_method(
            method_name='unloadObjects',
            library='Core',
            service_date='2008_05',
            service_name='DataManagement',
            params={'objsToUnload': objsToUnload},
            response_cls=ServiceData,
        )
