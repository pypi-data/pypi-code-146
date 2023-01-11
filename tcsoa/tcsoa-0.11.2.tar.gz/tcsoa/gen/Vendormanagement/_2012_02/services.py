from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Vendormanagement._2012_02.VendorManagement import LineItemPropertiesWithType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VendorManagementService(TcService):

    @classmethod
    def createOrUpdateLineItemsWithType(cls, properties: List[LineItemPropertiesWithType], bidPackage: BusinessObject) -> ServiceData:
        """
        This service operation creates or updates a group of BidPackageLineItem objects and any subtype of it in the
        context of the mentioned BidPackage. This operation allows the user to find or create a set of
        BidPackageLineItem objects based on the input data. It first tries to find the existence of the specified
        BidPackageLineItem for the specified BidPackage. If the specified BidPackageLineItem is found, then the its
        data will be updated. Otherwise, it will create the specified BidPackageLineItem and associate it to the
        specified BidPackageRevision. If the specified BidPackageLineItem objects exist and any of the input attribute
        values differ from those already set, they will be updated.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateLineItemsWithType',
            library='Vendormanagement',
            service_date='2012_02',
            service_name='VendorManagement',
            params={'properties': properties, 'bidPackage': bidPackage},
            response_cls=ServiceData,
        )
