from __future__ import annotations

from tcsoa.gen.Cad._2007_09.StructureManagement import CreateOrUpdateVariantCondInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def createOrUpdateVariantConditions2(cls, inputObjects: List[CreateOrUpdateVariantCondInput]) -> ServiceData:
        """
        This operation is to 'create' or 'update' (depending on the Operation) a variantCondition ( which is variant
        expression of type load if) for a BOMLine object.
        
        Use cases:
        This operation will be used when user wants to create a new or update an existing classic variant condition for
        a given BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateVariantConditions2',
            library='Cad',
            service_date='2007_09',
            service_name='StructureManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )
