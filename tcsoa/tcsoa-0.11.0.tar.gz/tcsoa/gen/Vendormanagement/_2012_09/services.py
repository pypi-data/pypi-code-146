from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Vendormanagement._2012_09.VendorManagement import VendorRoleData


class VendorManagementService(TcService):

    @classmethod
    def addRemoveVendorRoles(cls, vendorRoles: List[VendorRoleData], vendorRevRef: BusinessObject) -> ServiceData:
        """
        This operation adds or removes set of roles to/from a VendorRevision. Typically a role can be assigned to a
        VendorRevision by adding a role form with different role specific information. OOTB VendorRevision can be
        assigned with 3 roles namely Distributor, Supplier and Manufacturer. All these role forms contain information
        about the Vendor based on the type of the role. Similarly a role can be revoked from a VendorRevision. When a
        Vendor is revised, the new revision inherits all the assigned roles to the previous VendorRevision.
        """
        return cls.execute_soa_method(
            method_name='addRemoveVendorRoles',
            library='Vendormanagement',
            service_date='2012_09',
            service_name='VendorManagement',
            params={'vendorRoles': vendorRoles, 'vendorRevRef': vendorRevRef},
            response_cls=ServiceData,
        )
