from __future__ import annotations

from typing import List
from tcsoa.gen.EditContext._2015_07.DataManagement import ReferencerEditContextsResponse
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class DataManagementService(TcService):

    @classmethod
    def getReferencerEditContexts(cls, inputObjects: List[WorkspaceObject]) -> ReferencerEditContextsResponse:
        """
        This operation will return the list of context (Fnd0EditContext) objects that reference the input
        WorkspaceObjects.
        
        Use cases:
        This operation enables the following use case.
        Use Case 1: User wants to provide a list of edit contexts that can be used to configure a business object to
        enable editing in a particular context.
        - User provides the business object as the input to this operation.
        - A list of edit contexts that reference the business object are returned. Any of these edit contexts can be
        used for configuring the business object for editing in that particular context.
        
        """
        return cls.execute_soa_method(
            method_name='getReferencerEditContexts',
            library='EditContext',
            service_date='2015_07',
            service_name='DataManagement',
            params={'inputObjects': inputObjects},
            response_cls=ReferencerEditContextsResponse,
        )
