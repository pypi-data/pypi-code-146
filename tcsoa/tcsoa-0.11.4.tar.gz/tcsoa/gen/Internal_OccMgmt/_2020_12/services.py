from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.OccMgmt._2020_12.EffectivityManagement import GetEffectivityResponse, EffectivityInfoInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivityManagementService(TcService):

    @classmethod
    def setEffectivity(cls, effectivityDataInput: EffectivityInfoInput) -> ServiceData:
        """
        This operation sets effectivity on ItemRevision or Awb0Element objects. When input is ItemRevision the
        effectivity is set on ItemRevision. For Awb0Element, the effectivity is set on PSOccurrence associated with
        Awb0Element.
        End Item can be specified while setting the date and/or unit effectivity. If unit ranges are specified,
        effectivity end Item must be provided. A list of effectivity options can also be specified optionally along
        with date and unit ranges.
        
        Use cases:
        Use case 1: User adding effectivity on the object having no existing effectivity. 
        
        Input:
        Target Object existing effectivity: None 
        New Effectivity: Unit In = 3 &amp; Unit Out = 9 &amp; Intent = Design
        Resultant Effectivity set on the object: Unit In = 3 &amp; Unit Out = 9 &amp; Intent = Design
        
        Use case 2: User adding effectivity on the object having existing effectivity. 
        
        Input:
        Target Object existing effectivity: Unit In = 3 &amp; Unit Out = 9 &amp; Intent = Design
        New Effectivity: Unit In = 15 &amp; Unit Out = 20 &amp; Intent = Design
        Resultant Effectivity set on the object: ( Unit In = 3 &amp; Unit Out = 9 &amp; Intent = Design ) OR ( Unit In
        = 15 &amp; Unit Out = 20 &amp; Intent = Design )
        
        Use case 3: User adding effectivity on the object having existing effectivity. The new effectivity is
        overlapping with existing effectivity values.
        
        Input:
        Target Object existing effectivity: Unit In = 3 &amp; Unit Out = 9 &amp; Intent = Design
        New Effectivity: Unit In = 5 &amp; Unit Out = 20 &amp; Intent = Design
        Resultant Effectivity set on the object: Unit In = 5 &amp; Unit Out = 20 &amp; Intent = Design
        """
        return cls.execute_soa_method(
            method_name='setEffectivity',
            library='Internal-OccMgmt',
            service_date='2020_12',
            service_name='EffectivityManagement',
            params={'effectivityDataInput': effectivityDataInput},
            response_cls=ServiceData,
        )

    @classmethod
    def getEffectivity(cls, inputObjects: List[BusinessObject]) -> GetEffectivityResponse:
        """
        This operation retrieves the effectivity for the BusinessObjects of type ItemRevision or Awb0Element.
        """
        return cls.execute_soa_method(
            method_name='getEffectivity',
            library='Internal-OccMgmt',
            service_date='2020_12',
            service_name='EffectivityManagement',
            params={'inputObjects': inputObjects},
            response_cls=GetEffectivityResponse,
        )
