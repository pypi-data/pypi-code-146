from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow, WorkspaceObject
from tcsoa.gen.Internal.StructureManagement._2008_06.Structure import CopyRecursivelyResponse, FindHighestFindNumInExpandInput, FindHighestFindNumberInExpandResponse
from typing import List
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def copyRecursively(cls, objectToClone: WorkspaceObject, copyActionRulesKey: str, templateBOMWindow: BOMWindow, windowOfSelectedLine: BOMWindow, newName: str, newDescription: str, newId: str, newRevId: str, copyFutureEffectivities: bool) -> CopyRecursivelyResponse:
        """
        copyRecursively - perform cloning operation based on the template provide
        """
        return cls.execute_soa_method(
            method_name='copyRecursively',
            library='Internal-StructureManagement',
            service_date='2008_06',
            service_name='Structure',
            params={'objectToClone': objectToClone, 'copyActionRulesKey': copyActionRulesKey, 'templateBOMWindow': templateBOMWindow, 'windowOfSelectedLine': windowOfSelectedLine, 'newName': newName, 'newDescription': newDescription, 'newId': newId, 'newRevId': newRevId, 'copyFutureEffectivities': copyFutureEffectivities},
            response_cls=CopyRecursivelyResponse,
        )

    @classmethod
    def findHighestFindNumberInExpand(cls, input: List[FindHighestFindNumInExpandInput]) -> FindHighestFindNumberInExpandResponse:
        """
        Can be used to find the highest sequence number in the result of an expand, without actually returning all the
        objects in the expand.
        """
        return cls.execute_soa_method(
            method_name='findHighestFindNumberInExpand',
            library='Internal-StructureManagement',
            service_date='2008_06',
            service_name='Structure',
            params={'input': input},
            response_cls=FindHighestFindNumberInExpandResponse,
        )
