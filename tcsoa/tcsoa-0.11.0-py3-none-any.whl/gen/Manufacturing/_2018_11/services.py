from __future__ import annotations

from tcsoa.gen.Manufacturing._2018_11.StructureManagement import CopyRecursivelyResponse, PasteDuplicateStructureResponse, PasteDuplicateInput, CopyRecursivelyInputInfo
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def pasteDuplicateStructure(cls, pasteDuplicateInput: List[PasteDuplicateInput], copyRulesKey: str, notifyEvents: bool) -> PasteDuplicateStructureResponse:
        """
        This service operation clones the provided source BOMLine and paste the cloned line under the corresponding
        target BOMLine. Additionally, returns a structure which provides the mapping between the source BOMLine and the
        corresponding new child BOMLine.
        
        Use cases:
        A user can copy a source BOMLine and clone it under a target BOMLine using paste duplicate command.
        Applications like NX, might want to know the mapping between the source BOMLine and corresponding newly created
        BOMLine to check if there is any constraint defined within the source BOMLine which should be added to the
        created BOMLine.
        """
        return cls.execute_soa_method(
            method_name='pasteDuplicateStructure',
            library='Manufacturing',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'pasteDuplicateInput': pasteDuplicateInput, 'copyRulesKey': copyRulesKey, 'notifyEvents': notifyEvents},
            response_cls=PasteDuplicateStructureResponse,
        )

    @classmethod
    def copyRecursively(cls, copyInput: List[CopyRecursivelyInputInfo]) -> CopyRecursivelyResponse:
        """
        This service operation clones the input BOMLine structure. It either creates a new structure or updates the
        same structure by creating the cloned structure under the input target BOMLine.
        
        Use cases:
        Following use cases are supported.
        &bull;    Use Case 1: User can open a structure, launch "From Template" dialog and clone the structure. User
        can also provide the configuration information like variant rule(s), revision rule and also can specify if a
        new structure should be created. Other cloning parameters like "Carry over suppressed lines", "Carry future
        effectivity" can also be specified.
        &bull;    Use Case 2: User can launch the "From Template" dialog, provide the item ID of the structure and
        clone it. Similar to use case 1, user can specify the configuration information.
        """
        return cls.execute_soa_method(
            method_name='copyRecursively',
            library='Manufacturing',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'copyInput': copyInput},
            response_cls=CopyRecursivelyResponse,
        )
