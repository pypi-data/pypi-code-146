from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Rdv._2007_06.VariantManagement import GetVariabilityInfoResponse
from typing import List
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def getVariabilityInfo(cls, inputs: List[BusinessObject]) -> GetVariabilityInfoResponse:
        """
        Gets the Variability information assigned to the list of object supplied as input to this operation through the
        'inputs' list. The input objects could be any of the following
        -     Product Context :  (Product Item or Item Revision)
        -     Architecture Breakdown :  An object of type Architecture or its subtypes.
        -     Architecture Breakdown Element : Any leaf node or intermediate bomline which is of type Architecture or
        its subtypes. The Architecture Breakdown Element should have a valid generic_component_id which should be
        unique amongst all ABEs of the same type of Architecture.
        
        
        
        The operation would not succeed if any other objects are specified as inputs to this operation.
        
        Use cases:
        The 'getVariabilityInfo' operation is called when user wants to fetch the Variability information on Product
        Context or Architecture Breakdown or Architecture Breakdown Element. User can specify the input as a list of
        Product Context or Architecture Breakdown or Architecture Breakdown Element.
        """
        return cls.execute_soa_method(
            method_name='getVariabilityInfo',
            library='Internal-Rdv',
            service_date='2007_06',
            service_name='VariantManagement',
            params={'inputs': inputs},
            response_cls=GetVariabilityInfoResponse,
        )
