from __future__ import annotations

from tcsoa.gen.Internal.ChangeManagement._2012_10.ChangeManagement import ContextDataInput, CreatableChangeTypesResponse
from typing import List
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def getCreatableChangeTypes(cls, inputs: List[ContextDataInput]) -> CreatableChangeTypesResponse:
        """
        This operation provides the list of ChangeItem types that are allowed to be created by the logged-in user.
        
        Use cases:
        Create Change in context
        User wants to create a Change (ProblemReport, ChangeRequest, ChangeNotice etc.) in context of one or more
        business objects. Based on context data and the Change creatable conditions defined in BMIDE allowed Change
        types will be returned.
        """
        return cls.execute_soa_method(
            method_name='getCreatableChangeTypes',
            library='Internal-ChangeManagement',
            service_date='2012_10',
            service_name='ChangeManagement',
            params={'inputs': inputs},
            response_cls=CreatableChangeTypesResponse,
        )
