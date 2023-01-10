from __future__ import annotations

from tcsoa.gen.Internal.Vendormanagement._2008_06.VendorManagement import GetVPSRConditionsResponse
from tcsoa.base import TcService


class VendorManagementService(TcService):

    @classmethod
    def getVPSRConditions(cls) -> GetVPSRConditionsResponse:
        """
        This internal service operation gets a list of conditions to use for VendorPart Selection Rule. The Response
        structure returned contains a list of condition names and their expressions.
        
        Use cases:
        In a typical use case, there is a dialogue to be displayed which will let user select one of the VendorPart
        Selection Rule conditions.
        Once the dialogue is created, it may be populated using this operation.
        """
        return cls.execute_soa_method(
            method_name='getVPSRConditions',
            library='Internal-Vendormanagement',
            service_date='2008_06',
            service_name='VendorManagement',
            params={},
            response_cls=GetVPSRConditionsResponse,
        )
