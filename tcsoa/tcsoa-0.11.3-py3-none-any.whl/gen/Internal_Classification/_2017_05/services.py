from __future__ import annotations

from tcsoa.gen.Internal.Classification._2017_05.Classification import GetClassDefinitionsResponseNX
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def getClassDefinitionsNX(cls, classIDs: List[str]) -> GetClassDefinitionsResponseNX:
        """
        This operation returns Classification class definition, its attribute definitions including the details of
        associated Classification KeyLOV (stxt) objects.
        In comparison to 'getClassDefinitons' it contains additionally the NX Unit ID for each Classification attribute.
        
        Use cases:
        User wants to get details of classification class along with all associated class attributes. This operation is
        combination of getClassDescriptions and getAttributesForClasses2, but provides information in a different
        format to cater additional information like extended properties, attribute dependency, KeyLOVs (stxt) and also
        the NX Unit ID associated to class attributes.
        """
        return cls.execute_soa_method(
            method_name='getClassDefinitionsNX',
            library='Internal-Classification',
            service_date='2017_05',
            service_name='Classification',
            params={'classIDs': classIDs},
            response_cls=GetClassDefinitionsResponseNX,
        )
