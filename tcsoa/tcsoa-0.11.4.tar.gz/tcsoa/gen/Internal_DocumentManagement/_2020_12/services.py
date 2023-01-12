from __future__ import annotations

from tcsoa.gen.Internal.DocumentManagement._2020_12.AttributeExchange import ProcessAttrExchangeConfigInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AttributeExchangeService(TcService):

    @classmethod
    def processAttrExchangeConfigurations(cls, processAttrExchConfInputInfo: ProcessAttrExchangeConfigInput) -> ServiceData:
        """
        This operation adds, update or delete  Fnd0AttrExchangeConfig objects that are referenced by
        Fnd0LogicalObjectType.
        
        Use cases:
        This operation is invoked in the Exchange Configuration tab on an existing Logical Object Type.
        """
        return cls.execute_soa_method(
            method_name='processAttrExchangeConfigurations',
            library='Internal-DocumentManagement',
            service_date='2020_12',
            service_name='AttributeExchange',
            params={'processAttrExchConfInputInfo': processAttrExchConfInputInfo},
            response_cls=ServiceData,
        )
