from tcsoa.gen.ChangeManagement._2008_06.services import ChangeManagementService as imp0
from tcsoa.gen.ChangeManagement._2015_10.services import ChangeManagementService as imp1
from tcsoa.gen.ChangeManagement._2020_01.services import ChangeManagementService as imp2
from tcsoa.gen.ChangeManagement._2009_06.services import ChangeManagementService as imp3
from tcsoa.base import TcService


class ChangeManagementService(TcService):
    configureChangeSearches = imp0.configureChangeSearches
    createBOMEdits = imp0.createBOMEdits
    createChangeItems = imp0.createChangeItems
    createChangeLineage = imp1.createChangeLineage
    createSupercedures = imp0.createSupercedures
    deleteChangeLineage = imp1.deleteChangeLineage
    deleteSupercedures = imp0.deleteSupercedures
    deriveChangeItems = imp2.deriveChangeItems
    findContextData = imp0.findContextData
    findSupersedure = imp0.findSupersedure
    getAllChangeHomeFolders = imp0.getAllChangeHomeFolders
    getBOMEdits = imp0.getBOMEdits
    getNoteVariantChanges = imp3.getNoteVariantChanges
    updateChangeItems = imp0.updateChangeItems
    updateSupercedures = imp0.updateSupercedures
