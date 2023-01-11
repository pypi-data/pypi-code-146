from tcsoa.gen.Cad._2008_03.services import StructureManagementService as imp0
from tcsoa.gen.Cad._2013_05.services import StructureManagementService as imp1
from tcsoa.gen.Cad._2007_01.services import StructureManagementService as imp2
from tcsoa.gen.Cad._2016_09.services import StructureManagementService as imp3
from tcsoa.gen.Cad._2019_06.services import StructureManagementService as imp4
from tcsoa.gen.Cad._2007_12.services import StructureManagementService as imp5
from tcsoa.gen.Cad._2008_06.services import StructureManagementService as imp6
from tcsoa.gen.Cad._2007_06.services import StructureManagementService as imp7
from tcsoa.gen.Cad._2016_03.services import DataManagementService as imp8
from tcsoa.gen.Cad._2007_01.services import DataManagementService as imp9
from tcsoa.gen.Cad._2007_12.services import DataManagementService as imp10
from tcsoa.gen.Cad._2008_03.services import DataManagementService as imp11
from tcsoa.gen.Cad._2008_06.services import DataManagementService as imp12
from tcsoa.gen.Cad._2010_09.services import DataManagementService as imp13
from tcsoa.gen.Cad._2012_09.services import DataManagementService as imp14
from tcsoa.gen.Cad._2009_04.services import StructureManagementService as imp15
from tcsoa.gen.Cad._2020_01.services import AppSessionManagementService as imp16
from tcsoa.gen.Cad._2007_09.services import StructureManagementService as imp17
from tcsoa.gen.Cad._2016_03.services import StructureManagementService as imp18
from tcsoa.gen.Cad._2011_06.services import DataManagementService as imp19
from tcsoa.gen.Cad._2014_10.services import DataManagementService as imp20
from tcsoa.gen.Cad._2018_06.services import StructureManagementService as imp21
from tcsoa.base import TcService


class StructureManagementService(TcService):
    askChildPathBOMLines = imp0.askChildPathBOMLines
    askChildPathBOMLines2 = imp1.askChildPathBOMLines2
    closeBOMWindows = imp2.closeBOMWindows
    continueFindModelViews = imp3.continueFindModelViews
    continueReconcilePalette = imp3.continueReconcilePalette
    createBOMWindows = imp2.createBOMWindows
    createBOMWindows2 = imp1.createBOMWindows2
    createOrReConfigureBOMWindows = imp4.createOrReConfigureBOMWindows
    createOrUpdateAbsoluteStructure = imp2.createOrUpdateAbsoluteStructure
    createOrUpdateAbsoluteStructure2 = imp5.createOrUpdateAbsoluteStructure
    createOrUpdateAbsoluteStructure3 = imp6.createOrUpdateAbsoluteStructure
    createOrUpdateClassicOptions = imp7.createOrUpdateClassicOptions
    createOrUpdateRelativeStructure = imp2.createOrUpdateRelativeStructure
    createOrUpdateRelativeStructure2 = imp5.createOrUpdateRelativeStructure
    createOrUpdateRelativeStructure3 = imp6.createOrUpdateRelativeStructure
    createOrUpdateRelativeStructure4 = imp15.createOrUpdateRelativeStructure
    createOrUpdateRelativeStructure5 = imp1.createOrUpdateRelativeStructure
    createOrUpdateVariantConditions = imp7.createOrUpdateVariantConditions
    createOrUpdateVariantConditions2 = imp17.createOrUpdateVariantConditions2
    createVariantRules = imp6.createVariantRules
    deleteAssemblyArrangements = imp2.deleteAssemblyArrangements
    deleteAssemblyArrangements2 = imp5.deleteAssemblyArrangements
    deleteClassicOptions = imp7.deleteClassicOptions
    deleteRelativeStructure = imp2.deleteRelativeStructure
    deleteRelativeStructure2 = imp5.deleteRelativeStructure
    deleteRelativeStructure3 = imp6.deleteRelativeStructure
    deleteVariantConditions = imp7.deleteVariantConditions
    expandPSAllLevels = imp2.expandPSAllLevels
    expandPSAllLevels2 = imp6.expandPSAllLevels
    expandPSOneLevel = imp2.expandPSOneLevel
    expandPSOneLevel2 = imp6.expandPSOneLevel
    findModelViewsInStructure = imp18.findModelViewsInStructure
    getAbsoluteStructureData = imp6.getAbsoluteStructureData
    getConfiguredItemRevision = imp7.getConfiguredItemRevision
    getRevisionRules = imp2.getRevisionRules
    getVariantRules = imp2.getVariantRules
    queryClassicOptions = imp5.queryClassicOptions
    queryVariantConditions = imp5.queryVariantConditions
    reconfigureBOMWindows = imp6.reconfigureBOMWindows
    saveBOMWindows = imp6.saveBOMWindows
    startFindModelViews = imp3.startFindModelViews
    startReconcilePalette = imp3.startReconcilePalette
    writeAssemblyConfigurationDetails = imp21.writeAssemblyConfigurationDetails


class DataManagementService(TcService):
    createOrUpdateModelViewPalette = imp8.createOrUpdateModelViewPalette
    createOrUpdateModelViewProxies = imp8.createOrUpdateModelViewProxies
    createOrUpdateParts = imp9.createOrUpdateParts
    createOrUpdateParts2 = imp10.createOrUpdateParts
    createOrUpdateParts3 = imp11.createOrUpdateParts
    createOrUpdateParts4 = imp12.createOrUpdateParts
    createOrUpdateParts5 = imp13.createOrUpdateParts
    createOrUpdateParts6 = imp14.createOrUpdateParts
    createOrUpdateRelations = imp9.createOrUpdateRelations
    expandFoldersForCAD = imp9.expandFoldersForCAD
    expandFoldersForCAD2 = imp12.expandFoldersForCAD
    expandGRMRelations = imp9.expandGRMRelations
    expandPrimaryObjects = imp9.expandPrimaryObjects
    generateAlternateIds = imp9.generateAlternateIds
    getAllAttrMappings = imp9.getAllAttrMappings
    getAllAttrMappings2 = imp19.getAllAttrMappings2
    getAttrMappings = imp20.getAttrMappings
    getAttrMappingsForDatasetType = imp9.getAttrMappingsForDatasetType
    getAvailableTypes = imp9.getAvailableTypes
    resolveAttrMappings = imp11.resolveAttrMappings
    resolveAttrMappingsForDataset = imp9.resolveAttrMappingsForDataset


class AppSessionManagementService(TcService):
    createOrUpdateSavedSession = imp16.createOrUpdateSavedSession
    openSavedSession = imp16.openSavedSession
