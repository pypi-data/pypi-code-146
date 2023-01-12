from __future__ import annotations

from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AttributeExchangeService(TcService):

    @classmethod
    def updateDocumentProperties(cls, inputObjects: List[ItemRevision], checkConfiguration: bool) -> ServiceData:
        """
        Update the document properties of the ItemRevision object&rsquo;s related Dataset named reference&rsquo;s file
        using Logical Object attribute exchange.
        
        Use cases:
        Update ItemRevision&rsquo;s related Dataset named reference&rsquo;s file:
        If there is Logical Object attribute exchange is configured on the related Dataset object, this operation can
        be invoked to perform the attributre exchange on the Dataset named reference&rsquo;s file.
        """
        return cls.execute_soa_method(
            method_name='updateDocumentProperties',
            library='DocumentManagement',
            service_date='2018_06',
            service_name='AttributeExchange',
            params={'inputObjects': inputObjects, 'checkConfiguration': checkConfiguration},
            response_cls=ServiceData,
        )
