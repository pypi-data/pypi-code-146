from __future__ import annotations

from tcsoa.gen.Internal.VendorManagementAW._2019_12.VendorManagement import ColumnInfoResponse, RemovePartnerContractInput, AssignPartnerContractInput, ColumnInfoInput, ViewModelRowsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class VendorManagementService(TcService):

    @classmethod
    def assignPartnerContractToObject(cls, input: AssignPartnerContractInput) -> ServiceData:
        """
        This operation assigns the partner contract to the given WorkspaceObject object as specified in the input. The
        selected partner contract will be assigned to the given context information.
        """
        return cls.execute_soa_method(
            method_name='assignPartnerContractToObject',
            library='Internal-VendorManagementAW',
            service_date='2019_12',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getColumnInfo(cls, input: ColumnInfoInput) -> ColumnInfoResponse:
        """
        This operation returns the information of the columns for a given type of table to render a business object.
        
        The column information returned as part of this operation includes display name, internal name, object type, 
        width and a flag to indicate if the column needs to be displayed or not.
        """
        return cls.execute_soa_method(
            method_name='getColumnInfo',
            library='Internal-VendorManagementAW',
            service_date='2019_12',
            service_name='VendorManagement',
            params={'input': input},
            response_cls=ColumnInfoResponse,
        )

    @classmethod
    def getPartnerContractsOfSelectedObject(cls, inputObject: WorkspaceObject) -> ViewModelRowsResponse:
        """
        This operation returns the information of the partner contracts of the selected object.
        """
        return cls.execute_soa_method(
            method_name='getPartnerContractsOfSelectedObject',
            library='Internal-VendorManagementAW',
            service_date='2019_12',
            service_name='VendorManagement',
            params={'inputObject': inputObject},
            response_cls=ViewModelRowsResponse,
        )

    @classmethod
    def removePartnerContractFromObject(cls, removePartnerContractInput: RemovePartnerContractInput) -> ServiceData:
        """
        This operation removes the partner contract from the given WorkspaceObject object as specified in the input.
        The selected partner contract will be removed from the given context information.
        """
        return cls.execute_soa_method(
            method_name='removePartnerContractFromObject',
            library='Internal-VendorManagementAW',
            service_date='2019_12',
            service_name='VendorManagement',
            params={'removePartnerContractInput': removePartnerContractInput},
            response_cls=ServiceData,
        )
