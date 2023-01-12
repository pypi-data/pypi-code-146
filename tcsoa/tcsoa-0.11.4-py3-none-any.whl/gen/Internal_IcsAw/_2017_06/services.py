from __future__ import annotations

from tcsoa.gen.Internal.IcsAw._2017_06.Author import ClassificationObject, CreateOrUpdateClsObjectsResponse
from typing import List
from tcsoa.base import TcService


class AuthorService(TcService):

    @classmethod
    def createOrUpdateClassificationObjects(cls, classificationObjects: List[ClassificationObject]) -> CreateOrUpdateClsObjectsResponse:
        """
        Creates or updates one or more classification objects and (optionally) attach them to a WorkspaceObject, thus
        classifying it. When the Classification objects are not associated with any WorkspaceObject, they would act as
        standalone classification objects. A classification object is also called ICO.
        
        Use cases:
        User wants to classify a workspace object or create a standalone classification object (ICO) or update an
        existing classification object in Active Workspace. This operation can be combined with other operations like
        createItems() to create workspace object and then associate the workspace object to the classification object.
        Before creating a classification object, a classification class hierarchy should already be created by the
        classification admin user in Teamcenter. This hierarchy should include a storage class (a class that allows
        instances to be created and associated to it) for which the classification objects need to be created. Values
        of any attributes associated with classification objects can also be populated.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateClassificationObjects',
            library='Internal-IcsAw',
            service_date='2017_06',
            service_name='Author',
            params={'classificationObjects': classificationObjects},
            response_cls=CreateOrUpdateClsObjectsResponse,
        )
