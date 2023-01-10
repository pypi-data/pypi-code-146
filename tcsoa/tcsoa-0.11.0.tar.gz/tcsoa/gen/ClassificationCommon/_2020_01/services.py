from __future__ import annotations

from tcsoa.gen.ClassificationCommon._2020_01.Classification import ClassificationObjectResponse
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def deleteClassificationObjects(cls, jsonRequest: str) -> ClassificationObjectResponse:
        """
        Deletes one or more classification objects permanently. A classification object is also called ICO. The
        classified workspace object associated with the ICO will not be deleted.
        
        Use cases:
        User needs to delete classification objects. It is typically called when after creating or searching the
        classification objects, user decides that the returned objects are not needed anymore.
        """
        return cls.execute_soa_method(
            method_name='deleteClassificationObjects',
            library='ClassificationCommon',
            service_date='2020_01',
            service_name='Classification',
            params={'jsonRequest': jsonRequest},
            response_cls=ClassificationObjectResponse,
        )

    @classmethod
    def getClassificationObjects(cls, jsonRequest: str) -> ClassificationObjectResponse:
        """
        Looks for specified classification objects. If they are found, then detailed information about those objects is
        provided.
        
        Use cases:
        This operation can be utilized when user needs to find an existing classification object(s) to either view or
        update its details. It can be followed by operations like saveClassificationObjects() or
        deleteClassificationObjects() to update or delete the classification objects.
        This operation, getClassificationObjects() is used to get detailed information about the specified
        classification objects.
        """
        return cls.execute_soa_method(
            method_name='getClassificationObjects',
            library='ClassificationCommon',
            service_date='2020_01',
            service_name='Classification',
            params={'jsonRequest': jsonRequest},
            response_cls=ClassificationObjectResponse,
        )

    @classmethod
    def saveClassificationObjects(cls, jsonRequest: str) -> ClassificationObjectResponse:
        """
        Creates one or more classification objects and (optionally) attaches them to a workspace object, thus
        classifying it. If the Classification objects are not associated with any workspace object, they would act as
        standalone Classification objects. A classification object is also called ICO.
        
        Use cases:
        User wants to classify a workspace object or create a standalone classification object (ICO) in Teamcenter.
        This operation expects a json string and supports various options such as associating the classification object
        with a workspace object, populating values of any attributes associated with classification objects and so on. 
        Before creating classification objects, a classification class hierarchy should already be created by the
        classification admin user in Teamcenter. This hierarchy should include a storage class (a class that allows
        instances to be created and associated to it) for which the classification objects need to be created.
        """
        return cls.execute_soa_method(
            method_name='saveClassificationObjects',
            library='ClassificationCommon',
            service_date='2020_01',
            service_name='Classification',
            params={'jsonRequest': jsonRequest},
            response_cls=ClassificationObjectResponse,
        )
