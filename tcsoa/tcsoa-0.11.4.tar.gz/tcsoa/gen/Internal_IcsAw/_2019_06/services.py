from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.IcsAw._2019_06.Classification import ClassifyCommandVisibilityInfoResp
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def getClassificationCmdVisibilityInfo(cls, theWSOs: List[BusinessObject]) -> ClassifyCommandVisibilityInfoResp:
        """
        Finds classification command visibility information for traditional and Classification Standard Taxonomy (CST)
        for the list of workspace objects.
        If a given WorkspaceObject type is or dependent type is not present in ICS_classifiable_types preference or the
        user does not have permission to classify the workspace object then this operation returns false for the
        corresponding workspace object in the response.
        If a given workspace object type is or dependent type is present in ICS_classifiable_types and the user has the
        permission to classify the workspace object then this operation returns true for the corresponding workspace
        object in the response.
        
        Use cases:
        This operation could be used when user needs to find classification command visibility information, for given
        workspace objects in both traditional and Classification Standard Taxonomy (CST). 
        Each time a workspace object is selected for classify operation, this operation will evaluate the "Add" command
        visibility button in the classification tab based on workspace object type and user&rsquo;s privileges to
        classify the given WorkspaceObject.
        """
        return cls.execute_soa_method(
            method_name='getClassificationCmdVisibilityInfo',
            library='Internal-IcsAw',
            service_date='2019_06',
            service_name='Classification',
            params={'theWSOs': theWSOs},
            response_cls=ClassifyCommandVisibilityInfoResp,
        )
