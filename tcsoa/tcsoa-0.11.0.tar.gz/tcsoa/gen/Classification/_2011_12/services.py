from __future__ import annotations

from tcsoa.gen.Classification._2011_12.Classification import ClassificationInfoResponse
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def getClassificationObjectInfo(cls, icoUids: List[str], attributeIds: List[int], getOptimizedValues: bool, fetchDescriptor: bool, locale: str) -> ClassificationInfoResponse:
        """
        Provides detailed information on classification objects based on their unique identifiers (UID). A
        classification object is also called an ICO
        
        Use cases:
        When user needs to get details of a classification object (ICO).  These details include the classification
        class to which ICO belongs, the unit system, ICO ID, various ICO attributes and their values and property
        descriptor for these attributes
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getClassificationObjectInfo',
            library='Classification',
            service_date='2011_12',
            service_name='Classification',
            params={'icoUids': icoUids, 'attributeIds': attributeIds, 'getOptimizedValues': getOptimizedValues, 'fetchDescriptor': fetchDescriptor, 'locale': locale},
            response_cls=ClassificationInfoResponse,
        )
