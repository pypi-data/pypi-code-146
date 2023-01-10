from tcsoa.gen.GlobalMultiSite._2007_06.services import SiteReservationService as imp0
from tcsoa.gen.GlobalMultiSite._2011_06.services import ImportExportService as imp1
from tcsoa.gen.GlobalMultiSite._2007_06.services import ImportExportService as imp2
from tcsoa.gen.GlobalMultiSite._2008_06.services import ImportExportService as imp3
from tcsoa.gen.GlobalMultiSite._2010_04.services import ImportExportService as imp4
from tcsoa.gen.GlobalMultiSite._2007_12.services import ImportExportService as imp5
from tcsoa.gen.GlobalMultiSite._2020_04.services import ImportExportService as imp6
from tcsoa.base import TcService


class SiteReservationService(TcService):
    cancelSiteCheckOut = imp0.cancelSiteCheckOut
    siteCheckIn = imp0.siteCheckIn
    siteCheckOut = imp0.siteCheckOut


class ImportExportService(TcService):
    createGSIdentities = imp1.createGSIdentities
    createOrUpdateActionRules = imp2.createOrUpdateActionRules
    createOrUpdateClosureRules = imp2.createOrUpdateClosureRules
    createOrUpdateFilterRules = imp2.createOrUpdateFilterRules
    createOrUpdatePropertySets = imp2.createOrUpdatePropertySets
    createOrUpdateTransferModes = imp2.createOrUpdateTransferModes
    createOrUpdateTransferOptionSets = imp2.createOrUpdateTransferOptionSets
    exportObjectsToOfflinePackage = imp3.exportObjectsToOfflinePackage
    exportObjectsToPLMXML = imp4.exportObjectsToPLMXML
    getActionRules = imp2.getActionRules
    getAllTransferOptionSets = imp2.getAllTransferOptionSets
    getAvailableTransferOptionSets = imp2.getAvailableTransferOptionSets
    getClosureRules = imp2.getClosureRules
    getFilterRules = imp2.getFilterRules
    getHashedUID = imp1.getHashedUID
    getPropertySets = imp2.getPropertySets
    getRemoteSites = imp5.getRemoteSites
    getTransferModes = imp2.getTransferModes
    importObjectsFromOfflinePackage = imp3.importObjectsFromOfflinePackage
    importObjectsFromPLMXML = imp4.importObjectsFromPLMXML
    importObjectsFromPLMXMLWithDSM = imp6.importObjectsFromPLMXMLWithDSM
    requestExportToRemoteSites = imp5.requestExportToRemoteSites
    requestImportFromOfflinePackage = imp2.requestImportFromOfflinePackage
    requestImportFromRemoteSites = imp5.requestImportFromRemoteSites
