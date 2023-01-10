from __future__ import annotations

from tcsoa.gen.Allocations._2011_06.Allocation import AllocationContextInput2
from tcsoa.gen.Allocations._2007_01.Allocation import GetAllocationWindowResponse
from tcsoa.base import TcService


class AllocationService(TcService):

    @classmethod
    def createAllocationContext2(cls, input: AllocationContextInput2) -> GetAllocationWindowResponse:
        """
        The operation creates an AllocationMap object for the given name, id and attribute map input. This operation
        has Multi field key support for AllocationMap business object creation. The created AllocationMap object is
        saved to Teamcenter. It creates an AllocationWindow with the AllocationMapRevision object as context. It adds
        the input BOMWindow objects as the BOMWindow objects for the AllocationWindow. The created AllocationMap,
        AllocationRevision, AllocationWindow are returned as created objects list in ServiceData Element.
        
        Use cases:
        Create AllocationMap object with Multi field key support
        The AllocationMap object can be created with full Multi field key support using this operation. If the business
        constant of MFK for the AllocationMap object has item_id and any other attribute, then the user can create
        AllocationMap with same item id as well. 
        """
        return cls.execute_soa_method(
            method_name='createAllocationContext2',
            library='Allocations',
            service_date='2011_06',
            service_name='Allocation',
            params={'input': input},
            response_cls=GetAllocationWindowResponse,
        )
