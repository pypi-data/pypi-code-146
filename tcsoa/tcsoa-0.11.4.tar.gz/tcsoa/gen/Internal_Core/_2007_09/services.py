from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.Internal.Core._2007_09.DataManagement import WhereUsedResponseOccGroup


class DataManagementService(TcService):

    @classmethod
    def whereUsedOccGroup(cls, objects: List[BusinessObject], numLevels: int, whereUsedPrecise: bool, rule: BusinessObject) -> WhereUsedResponseOccGroup:
        """
        Finds the assemblies that a given Occurrence Group is used (unpublished for the case of Occurrence Group).
        """
        return cls.execute_soa_method(
            method_name='whereUsedOccGroup',
            library='Internal-Core',
            service_date='2007_09',
            service_name='DataManagement',
            params={'objects': objects, 'numLevels': numLevels, 'whereUsedPrecise': whereUsedPrecise, 'rule': rule},
            response_cls=WhereUsedResponseOccGroup,
        )
