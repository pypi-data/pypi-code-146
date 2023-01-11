from __future__ import annotations

from tcsoa.gen.Classification._2016_09.Classification import FindValuesResponse, FindValueInput
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def findValues(cls, findValueInputs: List[FindValueInput]) -> FindValuesResponse:
        """
        This operation returns all values available for an attribute in the context of where it is called.
        For example, it returns all the values of a particular attribute in a given class or in the entire database. 
        Some examples are:
        - Find all the available length values in the Sheet Metal Screw class. It will return responses such as 5mm,
        6mm, 7.5 mm, etc.
        - Find all the values for the Supplier attribute. It will return all values in all classes providing a list of
        all used suppliers stored in the classification.
        
        
        
        The operation can take other attribute values into consideration to narrow the results, for example:
        - Find all the available length values in the Sheet Metal Screw class where the diameter is 4mm. It will return
        responses such as 5mm, 6mm, etc.
        
        
        
        Use cases:
        Teamcenter Classification displays the List of Values dialog box containing a list of attribute values stored
        for the input attribute, their count and unit system in which those values are stored. This operation helps
        user to search for such stored values for multiple input attributes.
        The search can be constrained by setting other attribute values, the operations returns only the attribute
        values that are valid given the current search criteria (helping the user to efficiently narrow down the search
        and choose valid values that will find classified objects).
        """
        return cls.execute_soa_method(
            method_name='findValues',
            library='Classification',
            service_date='2016_09',
            service_name='Classification',
            params={'findValueInputs': findValueInputs},
            response_cls=FindValuesResponse,
        )
