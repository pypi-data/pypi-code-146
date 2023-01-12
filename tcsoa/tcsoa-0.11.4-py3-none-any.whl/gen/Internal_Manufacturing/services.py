from tcsoa.gen.Internal_Manufacturing._2017_11.services import ResourceManagementService as imp0
from tcsoa.gen.Internal_Manufacturing._2015_03.services import StructureManagementService as imp1
from tcsoa.gen.Internal_Manufacturing._2015_10.services import StructureManagementService as imp2
from tcsoa.gen.Internal_Manufacturing._2020_01.services import DataManagementService as imp3
from tcsoa.gen.Internal_Manufacturing._2018_11.services import ResourceManagementService as imp4
from tcsoa.gen.Internal_Manufacturing._2014_06.services import DataManagementService as imp5
from tcsoa.gen.Internal_Manufacturing._2008_12.services import CoreService as imp6
from tcsoa.gen.Internal_Manufacturing._2014_06.services import IPAManagementService as imp7
from tcsoa.gen.Internal_Manufacturing._2016_09.services import IPAManagementService as imp8
from tcsoa.gen.Internal_Manufacturing._2016_09.services import StructureManagementService as imp9
from tcsoa.gen.Internal_Manufacturing._2017_11.services import StructureManagementService as imp10
from tcsoa.gen.Internal_Manufacturing._2015_03.services import AttachmentsService as imp11
from tcsoa.gen.Internal_Manufacturing._2016_09.services import DataManagementService as imp12
from tcsoa.gen.Internal_Manufacturing._2016_03.services import ResourceManagementService as imp13
from tcsoa.gen.Internal_Manufacturing._2014_12.services import ModelService as imp14
from tcsoa.gen.Internal_Manufacturing._2018_11.services import StructureManagementService as imp15
from tcsoa.gen.Internal_Manufacturing._2017_05.services import ImportExportService as imp16
from tcsoa.gen.Internal_Manufacturing._2016_09.services import ResourceManagementService as imp17
from tcsoa.gen.Internal_Manufacturing._2015_10.services import StructureSearchService as imp18
from tcsoa.gen.Internal_Manufacturing._2016_09.services import StructureSearchService as imp19
from tcsoa.gen.Internal_Manufacturing._2019_06.services import ClosureRuleEditorService as imp20
from tcsoa.gen.Internal_Manufacturing._2017_05.services import DataManagementService as imp21
from tcsoa.gen.Internal_Manufacturing._2019_06.services import ResourceManagementService as imp22
from tcsoa.gen.Internal_Manufacturing._2020_04.services import DataManagementService as imp23
from tcsoa.gen.Internal_Manufacturing._2015_03.services import StructureSearchService as imp24
from tcsoa.gen.Internal_Manufacturing._2014_12.services import ResourceManagementService as imp25
from tcsoa.gen.Internal_Manufacturing._2015_03.services import ResourceManagementService as imp26
from tcsoa.gen.Internal_Manufacturing._2012_09.services import StructureSearchService as imp27
from tcsoa.gen.Internal_Manufacturing._2011_12.services import DataManagementService as imp28
from tcsoa.gen.Internal_Manufacturing._2014_12.services import IPAManagementService as imp29
from tcsoa.gen.Internal_Manufacturing._2019_06.services import StructureSearchService as imp30
from tcsoa.gen.Internal_Manufacturing._2020_01.services import StructureSearchService as imp31
from tcsoa.gen.Internal_Manufacturing._2013_12.services import ResourceManagementService as imp32
from tcsoa.gen.Internal_Manufacturing._2017_05.services import StructureManagementService as imp33
from tcsoa.base import TcService


class ResourceManagementService(TcService):
    addMultiToolCutter = imp0.addMultiToolCutter
    autoPositionComponentByCSYS = imp4.autoPositionComponentByCSYS
    createSetupSheets = imp13.createSetupSheets
    deleteMultiToolCutter = imp0.deleteMultiToolCutter
    extractHolderData = imp17.extractHolderData
    getICOMappingTargets = imp22.getICOMappingTargets
    getStepP21FileCounts2 = imp25.getStepP21FileCounts2
    getVendorCatalogInfo2 = imp25.getVendorCatalogInfo2
    getVendorCatalogInfo3 = imp17.getVendorCatalogInfo3
    importStep3DModels2 = imp26.importStep3DModels2
    importStepP21Files2 = imp25.importStepP21Files2
    importStepP21Files3 = imp26.importStepP21Files3
    mapClassificationObject = imp26.mapClassificationObject
    showCoordinateSystems = imp32.showCoordinateSystems
    showGCSConnectionPoints = imp32.showGCSConnectionPoints
    unzipGtcPackage = imp26.unzipGtcPackage


class StructureManagementService(TcService):
    alignAssemblies = imp1.alignAssemblies
    alignLinesInBOM = imp2.alignLinesInBOM
    completenessCheckPartStructure = imp9.completenessCheckPartStructure
    configureMultipleStructures = imp1.configureMultipleStructures
    createAlternativeScopeForProduct = imp10.createAlternativeScopeForProduct
    createAsyncCollabPlanningContext = imp9.createAsyncCollabPlanningContext
    createOrUpdateDesignPartAlignment = imp9.createOrUpdateDesignPartAlignment
    createReuseAssemblies = imp1.createReuseAssemblies
    evaluateLinks = imp15.evaluateLinks
    findBrokenPartsInProductView = imp15.findBrokenPartsInProductView
    findBrokenProductViews = imp15.findBrokenProductViews
    findRelatedDesignOrPartStructures = imp9.findRelatedDesignOrPartStructures
    getClusterDetails = imp1.getClusterDetails
    getEquivalentPropertyValues = imp2.getEquivalentPropertyValues
    linkOrUnlinkStructures = imp9.linkOrUnlinkStructures
    pasteByRule = imp10.pasteByRule
    pasteOrReplaceAssemblyInContext = imp2.pasteOrReplaceAssemblyInContext
    removeDesignPartAlignment = imp9.removeDesignPartAlignment
    searchForClusters = imp1.searchForClusters
    syncMasterAndAlternative = imp33.syncMasterAndAlternative
    verifyDesignPartAlignment = imp9.verifyDesignPartAlignment


class DataManagementService(TcService):
    associateOrRemoveScopesForProcess = imp3.associateOrRemoveScopesForProcess
    automaticMFGFeaturesAssignment = imp5.automaticMFGFeaturesAssignment
    createBOEfromPlantBOP = imp12.createBOEfromPlantBOP
    getFutureRevisions = imp21.getFutureRevisions
    getProductScopeForProcess = imp23.getProductScopeForProcess
    linkPlantBOPtoBOE = imp12.linkPlantBOPtoBOE
    postAssignIDICMaker = imp28.postAssignIDICMaker
    synchronizePlantBOPAndBOE = imp12.synchronizePlantBOPAndBOE


class CoreService(TcService):
    checkinForProcessSimulate = imp6.checkinForProcessSimulate
    checkoutForProcessSimulate = imp6.checkoutForProcessSimulate


class IPAManagementService(TcService):
    cleanDynamicIPALines = imp7.cleanDynamicIPALines
    cleanDynamicIPALines2 = imp8.cleanDynamicIPALines
    createDynamicIPALines = imp8.createDynamicIPALines
    getDynamicIPALines = imp7.getDynamicIPALines
    saveContentOfDynamicIPALines = imp8.saveContentOfDynamicIPALines
    searchDynamicIPAs = imp29.searchDynamicIPAs
    updateDynamicIPALines = imp8.updateDynamicIPALines


class AttachmentsService(TcService):
    createAttachmentLines = imp11.createAttachmentLines
    getAttachmentLines = imp11.getAttachmentLines


class ModelService(TcService):
    deleteScopeFlows = imp14.deleteScopeFlows
    getUILocations = imp14.getUILocations
    laAsyncResolve = imp14.laAsyncResolve
    saveUILocations = imp14.saveUILocations
    scheduleLAResolve = imp14.scheduleLAResolve


class ImportExportService(TcService):
    exportToBriefcaseAsync = imp16.exportToBriefcaseAsync
    importFromBriefcaseAsync = imp16.importFromBriefcaseAsync


class StructureSearchService(TcService):
    findCollabPlanningContext = imp18.findCollabPlanningContext
    findEquivalentLines = imp18.findEquivalentLines
    getBOEForPlantBOPScope = imp19.getBOEForPlantBOPScope
    getSearchCriteriaFromRecipe = imp24.getSearchCriteriaFromRecipe
    mapSrchCriteriaToLines = imp27.mapSrchCriteriaToLines
    saveOGLinesInSrchCriteria = imp27.saveOGLinesInSrchCriteria
    searchPartsInProximityOfMFGFeatures = imp30.searchPartsInProximityOfMFGFeatures
    searchScopedStructure = imp31.searchScopedStructure


class ClosureRuleEditorService(TcService):
    getClosureRuleTraversalInfo = imp20.getClosureRuleTraversalInfo
    setClosureRuleTraversalInfo = imp20.setClosureRuleTraversalInfo
