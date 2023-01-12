from __future__ import annotations

from tcsoa.gen.Internal.VendorManagementAW._2020_05.VendorManagement import AssignPartnerContractInput2, RemovePartnerContractInput2
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Internal.VendorManagementAW._2019_12.VendorManagement import ViewModelRowsResponse


class VendorManagementService(TcService):

    @classmethod
    def assignPartnerContractToObject2(cls, input: AssignPartnerContractInput2) -> ServiceData:
        """
        This operation assigns the partner contract to the given WorkspaceObject object as specified in the input. The
        selected partner contract will be assigned to the given context information.
        """
        return cls.execute_soa_method(
            method_name='assignPartnerContractToObject2',
            library='Internal-VendorManagementAW',
            service_date='2020_05',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getAssignedProductsOfContract(cls, input: ItemRevision) -> ViewModelRowsResponse:
        """
        This operation returns the information of the assigned products of a given partner contract revision.
        """
        return cls.execute_soa_method(
            method_name='getAssignedProductsOfContract',
            library='Internal-VendorManagementAW',
            service_date='2020_05',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ViewModelRowsResponse,
        )

    @classmethod
    def removePartnerContractFromObject2(cls, input: List[RemovePartnerContractInput2]) -> ServiceData:
        """
        This operation removes the partner contract from the given WorkspaceObject object as specified in the input.
        The partner contract will beis removed from the structure configuration of selected object. The selected object
        could be a ConfigurationContext or unconfigured ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='removePartnerContractFromObject2',
            library='Internal-VendorManagementAW',
            service_date='2020_05',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )
