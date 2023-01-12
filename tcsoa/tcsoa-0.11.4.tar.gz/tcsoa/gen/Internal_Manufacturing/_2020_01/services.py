from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2020_01.DataManagement import AssociateOrRemoveScopeInput
from typing import List
from tcsoa.gen.Internal.Manufacturing._2020_01.StructureSearch import SearchScopedStructureResponse, SearchScopedStructureInputInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def searchScopedStructure(cls, searchScopedStructureInput: SearchScopedStructureInputInfo) -> SearchScopedStructureResponse:
        """
        This service operation searches for objects in a BOP structure based on the input search criteria. It refers to
        related scope in Bill Of Material structure to obtain the final results. The search criteria consists of object
        type and query type.
        
        Use cases:
        Use Case 1 : A user opens a BOP structure. User selects a process line object from BOP structure and selects
        query "Suggested Product". This query identifies assigned products in process line from BOP structure and then
        calculates unassigned products using scope from BOM structure.
        Use Case 2 : A user opens a BOP structure. User selects a process line object from BOP structure and selects
        query "Suggested Discrete Features". This query Identifies assigned weldpoints in process line, find out the
        parts connected to Welds, which are NOT assigned in the process.
        Use Case 3 : A user opens a BOP structure. User selects a process line object from BOP structure and selects
        query "Suggested Datum Points". This query identifies assigned datumpoints in process line, find out the parts
        connected to datums, which are present in the scope from product.
        """
        return cls.execute_soa_method(
            method_name='searchScopedStructure',
            library='Internal-Manufacturing',
            service_date='2020_01',
            service_name='StructureSearch',
            params={'searchScopedStructureInput': searchScopedStructureInput},
            response_cls=SearchScopedStructureResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def associateOrRemoveScopesForProcess(cls, associateOrRemoveInput: List[AssociateOrRemoveScopeInput]) -> ServiceData:
        """
        This service operation associates the process line object from the BOP structure to either the BOMLine object
        scope or to Mfg0BvrWorkarea object from Bill of Equipment (BOE) structure. It creates Fnd0ProcessScopeRel
        relation between the item revision of process line object and the AbsOccurrence of BOMLine object or
        Mfg0BvrWorkarea object. This operation also removes the already defined association.
        
        Use cases:
        Use Case 1 : A user opens a BOM and a BOP structure. User selects a process line object from BOP structure,
        select one or more objects from BOM structure and associate the BOMLine objects to process line object. A
        Fnd0ProcessScopeRel is created between the item revision of process line object to AbsOccurrence of  selected
        scope line objects.
        Use Case 2 : A user opens a BOE and a BOP structure. User selects a process line object from BOP structure,
        select one or more objects from BOE structure and associate the Mfg0BvrWorkarea objects to process line object.
        A Fnd0ProcessScopeRel is created between the item revision of process line object to AbsOccurrence of  selected
        scope line objects.
        Use Case 3 : A user opens a BOP  structure. From the list of already defined scope lines from BOM or BOE
        structure, user select one or many line objects. The selected objects are disassociated from the process line
        object.
        """
        return cls.execute_soa_method(
            method_name='associateOrRemoveScopesForProcess',
            library='Internal-Manufacturing',
            service_date='2020_01',
            service_name='DataManagement',
            params={'associateOrRemoveInput': associateOrRemoveInput},
            response_cls=ServiceData,
        )
