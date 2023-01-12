from __future__ import annotations

from tcsoa.gen.Classification._2015_10.Classification import GetClassDefinitionsResponse
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def getClassDefinitions(cls, classIDs: List[str]) -> GetClassDefinitionsResponse:
        """
        This operation returns Classification class definition, its attribute definitions including the details of
        associated Classification KeyLOV (Stxt) objects.
        
        Use cases:
        User wants to get details of classification class along with all associated class attributes. This operation is
        combination of getClassDescriptions and getAttributesForClasses2, but provides information in a different
        format to cater additional information like extended properties, attribute dependency and KeyLOVs (Stxt) 
        associated to class attributes.
        """
        return cls.execute_soa_method(
            method_name='getClassDefinitions',
            library='Classification',
            service_date='2015_10',
            service_name='Classification',
            params={'classIDs': classIDs},
            response_cls=GetClassDefinitionsResponse,
        )
