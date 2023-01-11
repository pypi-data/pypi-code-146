from __future__ import annotations

from tcsoa.gen.ConfigFilterCriteria._2011_06.EffectivityManagement import ConfigExpression, EffectivityTablesResponse
from tcsoa.gen.ConfigFilterCriteria._2017_05.EffectivityManagement import EffectivityConditionInfo, EffectivityConditionSource
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivityManagementService(TcService):

    @classmethod
    def setEffectivityConditionSubsets(cls, productName: str, productNamespace: str, subsetCriteria: ConfigExpression, actionCode: int, effectivityConditions: List[EffectivityConditionInfo]) -> ServiceData:
        """
        This operation sets the effectivity expression on the input business objects. The subsetCriteria parameter
        provides the effectivity subset for which the new input expression should be combined with the existing
        effectivity on the target object. Additionally the actionCode parameter controls how this should be done. If
        the subsetCriteria parameter is not provided then the operation assumes the complete effectivity expression of
        the input object should be considered.
        
        Use cases:
        Use case 1: User adding effectivity on the object having no existing effectivity. User does not provide
        subsetCriteria. The actionCode provided is 1 (Overwrite). 
        Input:
        Target Object existing effectivity:  None  
        Expression:  Unit = 3..9 &amp; Intent = Design
        Resultant Effectivity set on the object:   Unit = 3..9 &amp; Intent = Design
        
        Use case 2: User adding Effectivity on object with existing effectivity expression. User does not provide
        subsetCriteria. The actionCode provided is 1 (Overwrite).
        Input:
        Target Object existing effectivity:  Unit = 1..5 &amp; Intent = Design  
        Expression:  Unit = 3..9 &amp; Intent = Design
        Resultant Effectivity set on the object:   Unit = 3..9 &amp; Intent = Design
        
        Use case 3: User adding Effectivity on object with existing effectivity expression. User provides a
        subsetCriteria value. The actionCode provided is 1 (Overwrite).
        Input:
        Target Object existing effectivity:  Unit = 1...15 &amp; Intent = Design  
        Expression:  Unit = 3..9 &amp; Intent = Design
        Subset Criteria: Unit = 3..12 &amp; Intent = Design
        Resultant Effectivity set on the object:   Unit = 1..9  &amp; Intent = Design | Unit = 13..15 &amp; Intent =
        Design
        
        Use case 4: User adding Effectivity on object with existing effectivity expression. User provides a
        subsetCriteria value. The actionCode provided is 1 (Overwrite).
        Input:
        Target Object existing effectivity:  Unit = 1..15 &amp; Intent = Design | Unit = 5..10 &amp; Intent =
        Engineering
        Expression:  Unit = 3..9 &amp; Intent = Design
        Subset Criteria: Unit = 3..12 &amp; Intent = Design
        Resultant Effectivity set on the object:   Unit = 1..9  &amp; Intent = Design | Unit = 13..15 &amp; Intent =
        Design | Unit = 5..10 &amp; Intent = Engineering
        
        Use case 5: User adding Effectivity on object with existing effectivity expression. User provides a discrete
        subsetCriteria value. The actionCode provided is 1 (Overwrite).
        Input:
        Target Object existing effectivity:  Unit = 1..15 &amp; Intent = Design &amp; Unit = 5..10 &amp; Intent =
        Engineering
        Expression:  Unit = 3..6 &amp; Intent = Design
        Subset Criteria: Unit = 3..8 | Unit = 15..20 
        Resultant Effectivity set on the object:   Unit = 1..6 &amp; Intent = Design | Unit = 9..14 &amp; Intent =
        Design | Unit = 9..10 &amp; Intent = Engineering
        """
        return cls.execute_soa_method(
            method_name='setEffectivityConditionSubsets',
            library='ConfigFilterCriteria',
            service_date='2017_05',
            service_name='EffectivityManagement',
            params={'productName': productName, 'productNamespace': productNamespace, 'subsetCriteria': subsetCriteria, 'actionCode': actionCode, 'effectivityConditions': effectivityConditions},
            response_cls=ServiceData,
        )

    @classmethod
    def getEffectivitySubsetTables(cls, productName: str, productNamespace: str, subsetCriteria: ConfigExpression, effectivityConditions: List[EffectivityConditionSource]) -> EffectivityTablesResponse:
        """
        This operation retrieves the effectivity expression in the EffectivityTable form for the input business objects
        or ConfigExpression as input. If subset criteria are provided the operation only returns the subset that
        matches the subset criteria.
        
        Use cases:
        Use case 1.  User wants to retrieve the effectivity from the input object. The subsetCriteria is not provided.
               Input object effectivity: Unit = 1..5 &amp; Intent = Design
               Subset Criteria: None
        Operation Response:  
             Object Effectivity:  Unit =  1..5 &amp; Intent = Design
        
        Use case 2.  User wants to retrieve the effectivity from the input object. The subsetCriteria is provided with
        some value. The effectivity of the input object is a superset of the subsetCriteria.
                Input object effectivity: Unit = 1..15 &amp; Intent = Design
                Subset Criteria: Unit = 3..6 &amp; Intent = Design
        Operation Response:  
              Object Effectivity:  Unit = 3..6 &amp; Intent = Design
        
        Use case 3.  User wants to retrieve the effectivity from the input object. The subsetCriteria is provided with
        some value. The effectivity of the input object partially overlaps with the subsetCriteria.
                Input object effectivity: Unit = 1..15 &amp; Intent = Design
               Subset Criteria: Unit = 13..26 &amp; Intent = Design
        Operation Response:  
             Object Effectivity:  Unit = 13..15 &amp; Intent = Design
        
        Use case 4. User wants to retrieve the effectivity from the input object. The subsetCriteria is provided with
        some value. The effectivity of the input object does not overlap with the subsetCriteria.
                 Input object effectivity: Unit = 1..9 &amp; Intent = Design | Unit = 16..25 &amp; Intent = Engineering
                Subset Criteria: Unit = 10..15 
        Operation Response:  
           Object Effectivity:  None
        
        Use case 5.  User wants to retrieve the effectivity from the input object. The subsetCriteria is provided with
        some value. The effectivity of the input object partially overlaps with the subsetCriteria.
                Input object effectivity: Unit = 1..10 &amp; Intent = Design | Unit = 15..25 &amp; Intent = Engineering
                Subset Criteria: Unit = 3..18 &amp; Intent = Design | Unit = 10..20 &amp; Intent = Engineering
        Operation Response:  
           Object Effectivity:  Unit = 3..10 &amp; Intent = Design | Unit = 15..20 &amp; Intent = Engineering
        """
        return cls.execute_soa_method(
            method_name='getEffectivitySubsetTables',
            library='ConfigFilterCriteria',
            service_date='2017_05',
            service_name='EffectivityManagement',
            params={'productName': productName, 'productNamespace': productNamespace, 'subsetCriteria': subsetCriteria, 'effectivityConditions': effectivityConditions},
            response_cls=EffectivityTablesResponse,
        )
