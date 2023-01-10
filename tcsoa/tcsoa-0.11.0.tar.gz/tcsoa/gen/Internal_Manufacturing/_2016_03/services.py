from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def createSetupSheets(cls, icoIds: List[str]) -> ServiceData:
        """
        This operation creates setup sheets for Manufacturing Resource Manager resources by using the NX
        Graphicsbuilder functionality.  Starting at the class of each classified resource, a search of the
        Classification hierarchy is conducted in an upward direction until a class is found that the multi-value
        preference 'MRMSetupSheetTemplates' associates with a setup sheet template revision ID.  The NX Graphicsbuilder
        is called to create the setup sheet for the given resource, based on the associated setup sheet template.  The
        resulting setup sheet is associated with the resource's ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='createSetupSheets',
            library='Internal-Manufacturing',
            service_date='2016_03',
            service_name='ResourceManagement',
            params={'icoIds': icoIds},
            response_cls=ServiceData,
        )
