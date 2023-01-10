from __future__ import annotations

from tcsoa.gen.Classification._2015_03.Classification import GetDependencyKeyLOVsResponse, DependencyAttributeStruct
from typing import List
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def getKeyLOVsForDependentAttributes(cls, dependencyAttributeStruct: List[DependencyAttributeStruct]) -> GetDependencyKeyLOVsResponse:
        """
        This operation returns the Classification KeyLOV (stxt) definitions based on the dependency settings on class
        or view attributes.
        
        Use cases:
        If a user changes the value for any attribute in a dependency chain while working in a class containing
        interdependent KeyLOV (stxt) attributes, the other dependent attributes should get configured KeyLOV structures
        and potential auto populated value.
         
        This operation is used to get the value and the KeyLOV definition for the dependent KeyLOV attributes. 
        Consider a class containing two interdependent KeyLOV attributes 
        Country
            United States
            Canada
        State
            Ohio
            California
            Ontario
            Quebec
        - If a user first selects the value for Country attribute say "United States" the State attribute will only
        show states belonging "United States".
        - If a user first selects the value for State attribute say "Ohio"; value for Country attribute will be auto
        populated to "United States". Now, if a user deselects the value for Country attribute; the value for State
        attribute gets deselected as well. 
        
        """
        return cls.execute_soa_method(
            method_name='getKeyLOVsForDependentAttributes',
            library='Classification',
            service_date='2015_03',
            service_name='Classification',
            params={'dependencyAttributeStruct': dependencyAttributeStruct},
            response_cls=GetDependencyKeyLOVsResponse,
        )
