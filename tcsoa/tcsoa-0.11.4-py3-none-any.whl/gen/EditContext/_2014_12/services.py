from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0EditContext, POM_object
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def setEditContext(cls, context: Fnd0EditContext, objects: List[POM_object]) -> ServiceData:
        """
        If input parameter "context" is not null, the SOA response will contain the input Business Objects configured
        with the configuration parameter belonging to the input context. If any of the input Business Objects are not
        POM Revisable, they will be returned without configuration parameter. The Business Objects will be added to the
        Plain Objects array in ServiceData.
        If input parameter "context" is null, the input Business Objects will be configured for Public edits and
        returned in the SOA response.
        
        Use cases:
        This operation will enable the user to enter or exit edit mode and subsequently save the edits as Private Edits.
        """
        return cls.execute_soa_method(
            method_name='setEditContext',
            library='EditContext',
            service_date='2014_12',
            service_name='DataManagement',
            params={'context': context, 'objects': objects},
            response_cls=ServiceData,
        )
