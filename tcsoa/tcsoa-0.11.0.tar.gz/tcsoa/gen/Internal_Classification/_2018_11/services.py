from __future__ import annotations

from tcsoa.gen.Classification._2007_01.Classification import ClassificationObject
from typing import List
from tcsoa.gen.Internal.Classification._2018_11.Classification import SaveClassificationObjectsResponse
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def saveClassificationObjects(cls, classificationObjects: List[ClassificationObject]) -> SaveClassificationObjectsResponse:
        """
        Creates or updates one or more classification objects and (optionally) attach them to a WorkspaceObject object,
        thus classifying it. When the Classification objects are not associated with any WorkspaceObject they act as
        standalone classification objects. A classification object is also called an ICO object. This supports
        traditional ICO.
        
        Use cases:
        User wants to classify a Workspace Object or create a standalone classification object (ICO) or update an
        existing classification object, in a traditional class. This operation can be combined with other operations
        like createItems() to create workspace object and then associate the workspace object to the classification
        object. Before creating a classification object, a classification class hierarchy should already be created by
        the classification admin user in Teamcenter. This hierarchy should include a storage class (a class that allows
        instances to be created and associated to it) for which the classification objects need to be created. Values
        of any attributes associated with classification objects can also be populated.
        """
        return cls.execute_soa_method(
            method_name='saveClassificationObjects',
            library='Internal-Classification',
            service_date='2018_11',
            service_name='Classification',
            params={'classificationObjects': classificationObjects},
            response_cls=SaveClassificationObjectsResponse,
        )
