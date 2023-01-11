from tcsoa.gen.Vendormanagement._2012_09.services import VendorManagementService as imp0
from tcsoa.gen.Vendormanagement._2008_06.services import VendorManagementService as imp1
from tcsoa.gen.Vendormanagement._2007_06.services import VendorManagementService as imp2
from tcsoa.gen.Vendormanagement._2012_02.services import VendorManagementService as imp3
from tcsoa.gen.Vendormanagement._2016_09.services import VendorManagementService as imp4
from tcsoa.base import TcService


class VendorManagementService(TcService):
    addRemoveVendorRoles = imp0.addRemoveVendorRoles
    changeVendor = imp1.changeVendor
    createOrUpdateBidPackages = imp2.createOrUpdateBidPackages
    createOrUpdateLineItems = imp2.createOrUpdateLineItems
    createOrUpdateLineItemsWithType = imp3.createOrUpdateLineItemsWithType
    createOrUpdateVendorParts = imp2.createOrUpdateVendorParts
    createOrUpdateVendors = imp2.createOrUpdateVendors
    createVendorParts = imp4.createVendorParts
    deleteLineItems = imp2.deleteLineItems
    deleteVendorRoles = imp2.deleteVendorRoles
    deleteVendors = imp2.deleteVendors
    getVendorPartsWithSelRule = imp1.getVendorPartsWithSelRule
