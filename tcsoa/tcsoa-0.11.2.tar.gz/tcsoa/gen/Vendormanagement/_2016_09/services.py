from __future__ import annotations

from tcsoa.gen.Vendormanagement._2007_06.VendorManagement import CreateVendorPartsResponse
from typing import List
from tcsoa.base import TcService
from tcsoa.gen.Vendormanagement._2016_09.VendorManagement import VendorPartProperties2


class VendorManagementService(TcService):

    @classmethod
    def createVendorParts(cls, properties: List[VendorPartProperties2]) -> CreateVendorPartsResponse:
        """
        This operation creates a set of ManufacturerPart objects of given type based on input data.This operation is
        applicable for bulk creation of Vendor Part objects.
        
        Use cases:
        Create Vendor Parts in bulk,when Vendor is already created and CompanyLocation can be available with Vendor.
        """
        return cls.execute_soa_method(
            method_name='createVendorParts',
            library='Vendormanagement',
            service_date='2016_09',
            service_name='VendorManagement',
            params={'properties': properties},
            response_cls=CreateVendorPartsResponse,
        )
