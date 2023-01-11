from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.Vendormanagement._2008_05.VendorManagement import LineItemPropsWithType, ItemIDInput, ItemIDResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VendorManagementService(TcService):

    @classmethod
    def getItemIDwithContext(cls, input: List[ItemIDInput]) -> ItemIDResponse:
        """
        This service operation concatenates external object id and context id with hyphen to generate a new item id,
        provided length of concatenated id is less than the desired item id length. This operation also returns
        existing Item objects that have the generated IDs.
        The intent of this operation is to support import of Item objects from external systems. This service operation
        concatenates external object id and context id with hyphen to generate a new item id, provided length of
        concatenated id is less than the desired item id length. This operation also returns existing Item objects that
        have the generated IDs.
        The intent of this operation is to support import of Item objects from external systems.
        """
        return cls.execute_soa_method(
            method_name='getItemIDwithContext',
            library='Internal-Vendormanagement',
            service_date='2008_05',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ItemIDResponse,
        )

    @classmethod
    def createOrUpdateLineItems(cls, properties: List[LineItemPropsWithType], bidPackage: BusinessObject) -> ServiceData:
        """
        This service operation creates or updates a group of BidPackageLineItem objects in the context of the mentioned
        BidPackage. This operation allows the user to find or create a set of BidPackageLineItem objects based on the
        input data. It first tries to find the existence of the specified BidPackageLineItem for the specified
        BidPackage. If the specified BidPackageLineItem is found, then the BidPackageLineItem data will be updated.
        Otherwise, it will create the specified BidPackageLineItem and associate it to the specified
        BidPackageRevision. If the specified BidPackageLineItem objects exist and any of the input attribute values
        differ from those already set, the BidPackageLineItem objects will be updated.
        The operation is now deprecated. It is now replaced by
        'Teamcenter::Soa::Vendormanagement::VendorManagement::createOrUpdateLineItemsWithType.'
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateLineItems',
            library='Internal-Vendormanagement',
            service_date='2008_05',
            service_name='VendorManagement',
            params={'properties': properties, 'bidPackage': bidPackage},
            response_cls=ServiceData,
        )
