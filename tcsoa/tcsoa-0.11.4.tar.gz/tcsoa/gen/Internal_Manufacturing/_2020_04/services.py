from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Manufacturing._2020_04.DataManagement import GetProductScopeForProcessResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getProductScopeForProcess(cls, processLine: List[BusinessObject]) -> GetProductScopeForProcessResponse:
        """
        This service returns a list of product line from BOM (Bill of Material) structure which are related to process
        line with "Fnd0ProcessToScopeRel" relation.
        
        Use cases:
        User selects a process line from the Bill of Proces (BOP) structure and selects "Set/Edit Scope" from context
        menu. The "Set Product Bucket" dialog lists all the product BOMLines related to selected process line.
        """
        return cls.execute_soa_method(
            method_name='getProductScopeForProcess',
            library='Internal-Manufacturing',
            service_date='2020_04',
            service_name='DataManagement',
            params={'processLine': processLine},
            response_cls=GetProductScopeForProcessResponse,
        )
