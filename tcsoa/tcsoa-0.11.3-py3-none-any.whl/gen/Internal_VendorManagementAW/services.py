from tcsoa.gen.Internal_VendorManagementAW._2019_12.services import VendorManagementService as imp0
from tcsoa.gen.Internal_VendorManagementAW._2020_05.services import VendorManagementService as imp1
from tcsoa.gen.Internal_VendorManagementAW._2020_12.services import VendorManagementService as imp2
from tcsoa.base import TcService


class VendorManagementService(TcService):
    assignPartnerContractToObject = imp0.assignPartnerContractToObject
    assignPartnerContractToObject2 = imp1.assignPartnerContractToObject2
    getAssignedProductsOfContract = imp1.getAssignedProductsOfContract
    getColumnInfo = imp0.getColumnInfo
    getPartnerContractsOfSelectedObject = imp0.getPartnerContractsOfSelectedObject
    removePartnerContractFromObject = imp0.removePartnerContractFromObject
    removePartnerContractFromObject2 = imp1.removePartnerContractFromObject2
    sortAndFilterViewModelRows = imp2.sortAndFilterViewModelRows
