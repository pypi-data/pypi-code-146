from tcsoa.gen.Internal_Vendormanagement._2008_05.services import VendorManagementService as imp0
from tcsoa.gen.Internal_Vendormanagement._2008_06.services import VendorManagementService as imp1
from tcsoa.base import TcService


class VendorManagementService(TcService):
    createOrUpdateLineItems = imp0.createOrUpdateLineItems
    getItemIDwithContext = imp0.getItemIDwithContext
    getVPSRConditions = imp1.getVPSRConditions
