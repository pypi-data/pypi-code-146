from __future__ import annotations

from tcsoa.gen.Internal.Classification._2020_04.Classification import FindClassificationInfoRequest, FindClassificationInfoResponse
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def findClassificationInfo(cls, request: List[FindClassificationInfoRequest], options: int) -> FindClassificationInfoResponse:
        """
        Finds classification information based on the input criteria.
        
        This operation finds and returns all the classification objects for the given WorkspaceObject and
        classification class definition, its attribute definitions including the details of associated Classification
        KeyLOV (stxt).
        Return information such as class information, class images, relations can be optionally restricted using option
        parameter.
        
        Use cases:
        This operation could be used when user needs to find classification objects, based on workspace objects. Each
        time a WorkspaceObject is classified in a classification class a classification object is created. The
        operation findClassificationInfo can be used to get detailed information about the classification objects where
        these classification objects belong. After getting information about classification objects the user can choose
        to modify or delete the objects using saveClassificationObjects or deleteClassificationObjects service
        operations. 
        
        The operation findClassificationInfo can also be used when a user wants to find details of classification class
        definition, its attribute definitions including the details of associated classification KeyLOV (stxt) objects.
        This information can help user decide whether to classify a WorkspaceObject in particular classification
        classes.
        
        This operation also provides the option for user to exclude certain information such as class information,
        class images, relations that is not required for the use case.
        """
        return cls.execute_soa_method(
            method_name='findClassificationInfo',
            library='Internal-Classification',
            service_date='2020_04',
            service_name='Classification',
            params={'request': request, 'options': options},
            response_cls=FindClassificationInfoResponse,
        )
