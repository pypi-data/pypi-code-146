from __future__ import annotations

from tcsoa.gen.Internal.Classification._2009_10.Classification import GetClassificationHierarchiesResponse, GetClassificationPropertiesResponse
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class ClassificationService(TcService):

    @classmethod
    def getClassificationHierarchies(cls, wsos: List[WorkspaceObject]) -> GetClassificationHierarchiesResponse:
        """
        Finds information on classification class hierarchies corresponding to all the classification classes where the
        specified workspace object(s) is classified. For each classification class hierarchy, the name & ID of classes
        in it are retrieved
        
        Use cases:
        User wants to retrieve information about class hierarchy of the classification class in which a workspace
        object (WSO) is classified. This operation is similar to 'getClassificationProperties' operation which provides
        additional details from classification object as well. This operation only provides classification class
        hierarchy details.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception. In all other cases
        failures will be returned with the WorkspaceObject ID mapped to the error message in the 'ServiceData' list of
        partial errors of the returned 'GetClassificationHierarchiesResponse' structure
        """
        return cls.execute_soa_method(
            method_name='getClassificationHierarchies',
            library='Internal-Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'wsos': wsos},
            response_cls=GetClassificationHierarchiesResponse,
        )

    @classmethod
    def getClassificationProperties(cls, wsos: List[WorkspaceObject]) -> GetClassificationPropertiesResponse:
        """
        Gets information about classification objects based on workspace objects. A classification object is also
        called an ICO. ICO property values along with the underlying class hierarchy information can be retrieved. The
        hierarchy information provides details on the hierarchical structure of the classification class where the
        workspace object is classified.
        
        Use cases:
        User needs information about a classification object related to a workspace object. Information may be limited
        to the classification properties associated with the classification object and their values. Or it may include
        information on the underlying classification class structure for the classification object
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getClassificationProperties',
            library='Internal-Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'wsos': wsos},
            response_cls=GetClassificationPropertiesResponse,
        )
