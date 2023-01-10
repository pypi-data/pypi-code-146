from tcsoa.gen.Manufacturing._2012_02.services import DataManagementService as imp0
from tcsoa.gen.Manufacturing._2014_06.services import DataManagementService as imp1
from tcsoa.gen.Manufacturing._2008_06.services import TimeManagementService as imp2
from tcsoa.gen.Manufacturing._2012_09.services import DataManagementService as imp3
from tcsoa.gen.Manufacturing._2009_10.services import ModelService as imp4
from tcsoa.gen.Manufacturing._2010_09.services import TimeManagementService as imp5
from tcsoa.gen.Manufacturing._2014_06.services import ResourceManagementService as imp6
from tcsoa.gen.Manufacturing._2013_05.services import IPAManagementService as imp7
from tcsoa.gen.Manufacturing._2009_06.services import StructureManagementService as imp8
from tcsoa.gen.Manufacturing._2011_06.services import DataManagementService as imp9
from tcsoa.gen.Manufacturing._2009_10.services import MFGPropertyCollectorService as imp10
from tcsoa.gen.Manufacturing._2013_12.services import ModelService as imp11
from tcsoa.gen.Manufacturing._2009_10.services import StructureManagementService as imp12
from tcsoa.gen.Manufacturing._2018_11.services import StructureManagementService as imp13
from tcsoa.gen.Manufacturing._2013_05.services import DataManagementService as imp14
from tcsoa.gen.Manufacturing._2015_10.services import StructureManagementService as imp15
from tcsoa.gen.Manufacturing._2009_10.services import DataManagementService as imp16
from tcsoa.gen.Manufacturing._2014_12.services import StructureSearchService as imp17
from tcsoa.gen.Manufacturing._2008_06.services import DataManagementService as imp18
from tcsoa.gen.Manufacturing._2012_02.services import IPAManagementService as imp19
from tcsoa.gen.Manufacturing._2008_12.services import IPAManagementService as imp20
from tcsoa.gen.Manufacturing._2012_09.services import ValidationService as imp21
from tcsoa.gen.Manufacturing._2016_03.services import ImportExportService as imp22
from tcsoa.gen.Manufacturing._2013_05.services import StructureManagementService as imp23
from tcsoa.gen.Manufacturing._2014_12.services import IPAManagementService as imp24
from tcsoa.gen.Manufacturing._2008_06.services import CoreService as imp25
from tcsoa.gen.Manufacturing._2010_09.services import CoreService as imp26
from tcsoa.gen.Manufacturing._2013_05.services import CoreService as imp27
from tcsoa.gen.Manufacturing._2013_05.services import StructureSearchService as imp28
from tcsoa.gen.Manufacturing._2017_05.services import ValidationService as imp29
from tcsoa.gen.Manufacturing._2012_02.services import ModelService as imp30
from tcsoa.gen.Manufacturing._2017_11.services import DataManagementService as imp31
from tcsoa.gen.Manufacturing._2009_10.services import ModelDefinitionsService as imp32
from tcsoa.gen.Manufacturing._2014_12.services import ValidationService as imp33
from tcsoa.gen.Manufacturing._2018_06.services import DataManagementService as imp34
from tcsoa.gen.Manufacturing._2012_02.services import ConstraintsService as imp35
from tcsoa.gen.Manufacturing._2011_06.services import StructureManagementService as imp36
from tcsoa.gen.Manufacturing._2013_12.services import ResourceManagementService as imp37
from tcsoa.gen.Manufacturing._2013_05.services import TimeWayPlanService as imp38
from tcsoa.gen.Manufacturing._2017_05.services import ImportExportService as imp39
from tcsoa.gen.Manufacturing._2013_05.services import ImportExportService as imp40
from tcsoa.gen.Manufacturing._2015_10.services import ImportExportService as imp41
from tcsoa.gen.Manufacturing._2010_09.services import ImportExportService as imp42
from tcsoa.gen.Manufacturing._2015_03.services import StructureManagementService as imp43
from tcsoa.gen.Manufacturing._2009_10.services import StructureSearchService as imp44
from tcsoa.gen.Manufacturing._2019_06.services import DataManagementService as imp45
from tcsoa.gen.Manufacturing._2014_06.services import StructureSearchService as imp46
from tcsoa.gen.Manufacturing._2014_12.services import ModelService as imp47
from tcsoa.base import TcService


class DataManagementService(TcService):
    addAssociatedContexts = imp0.addAssociatedContexts
    addOrRemoveAssociatedContexts = imp1.addOrRemoveAssociatedContexts
    applyConfigObjects = imp3.applyConfigObjects
    associateAndAllocateByPreview = imp0.associateAndAllocateByPreview
    automaticAllocatePreview = imp0.automaticAllocatePreview
    automaticAssociateAndAllocate = imp0.automaticAssociateAndAllocate
    cloneAssemblyAndProcessObjects = imp1.cloneAssemblyAndProcessObjects
    closeContexts = imp9.closeContexts
    closeViews = imp9.closeViews
    connectObjects = imp0.connectObjects
    createAttachments = imp14.createAttachments
    createObjects = imp16.createObjects
    createOrUpdateConfigObjects = imp3.createOrUpdateConfigObjects
    createOrUpdateMEActivityFolders = imp18.createOrUpdateMEActivityFolders
    createOrUpdateMENXObjects = imp18.createOrUpdateMENXObjects
    disconnectFromOrigin = imp0.disconnectFromOrigin
    disconnectObjects = imp16.disconnectObjects
    establishOriginLink = imp1.establishOriginLink
    getAssociatedContexts = imp0.getAssociatedContexts
    getConnectorInfo = imp31.getConnectorInfo
    getOccurrenceKinematicsInformation = imp34.getOccurrenceKinematicsInformation
    getPhysicalAttachmentsInScope = imp31.getPhysicalAttachmentsInScope
    getProcessResourceRelatedInfo = imp1.getProcessResourceRelatedInfo
    openContexts = imp9.openContexts
    openViews = imp9.openViews
    publishSelectionFromStudyToSource = imp45.publishSelectionFromStudyToSource
    removePhysicalAttachementRelation = imp31.removePhysicalAttachementRelation
    setAttributes = imp14.setAttributes
    setConnectorInfo = imp31.setConnectorInfo
    setOccurrenceKinematicsInformation = imp34.setOccurrenceKinematicsInformation
    setPhysicalAttachementsInScope = imp31.setPhysicalAttachementsInScope
    syncSelectionInStudyWithSource = imp45.syncSelectionInStudyWithSource
    syncStudyAndSource = imp14.syncStudyAndSource


class TimeManagementService(TcService):
    allocatedTimeRollUp = imp2.allocatedTimeRollUp
    calculateCriticalPathEx = imp5.calculateCriticalPathEx
    getActivityTimes = imp5.getActivityTimes
    populateAllocatedTimeProperties = imp5.populateAllocatedTimeProperties
    timeAnalysisRollup = imp2.timeAnalysisRollup
    updateTimeManagementProperties = imp5.updateTimeManagementProperties


class ModelService(TcService):
    calculateCriticalPath = imp4.calculateCriticalPath
    computeAppearancePath = imp11.computeAppearancePath
    createFlow = imp4.createFlow
    editLogicalAssignments = imp4.editLogicalAssignments
    getCandidateToolsForToolRequirement = imp30.getCandidateToolsForToolRequirement
    getResolvedNodesFromLA = imp4.getResolvedNodesFromLA
    getToolRequirements = imp30.getToolRequirements
    removeFlow = imp4.removeFlow
    resolveLogicalAssignments = imp4.resolveLogicalAssignments
    resolveToolRequirement = imp30.resolveToolRequirement
    updateFlows = imp30.updateFlows
    validateScopeFlowsConsistency = imp47.validateScopeFlowsConsistency


class ResourceManagementService(TcService):
    checkToolParameters = imp6.checkToolParameters
    getStepP21FileCounts = imp37.getStepP21FileCounts
    getVendorCatalogInfo = imp37.getVendorCatalogInfo
    importStep3DModels = imp37.importStep3DModels
    importStepP21Files = imp37.importStepP21Files
    importVendorCatalogHierarchy = imp37.importVendorCatalogHierarchy
    updateNXToolAssemblies = imp37.updateNXToolAssemblies


class IPAManagementService(TcService):
    cleanIPATree = imp7.cleanIPATree
    deleteFilteredIPA = imp19.deleteFilteredIPA
    deletefilteredIPA = imp20.deletefilteredIPA
    doesIPAExist = imp7.doesIPAExist
    findAndRepopulateDynamicIPAs = imp24.findAndRepopulateDynamicIPAs
    generateIPATree = imp7.generateIPATree
    generateSearchScope = imp20.generateSearchScope
    getFilteredIPA = imp20.getFilteredIPA
    getFilteredIPAType = imp19.getFilteredIPAType
    localUpdateIPATree = imp7.localUpdateIPATree
    repopulateDynamicIPAs = imp24.repopulateDynamicIPAs
    saveSearchResult = imp20.saveSearchResult
    updateIPATree = imp7.updateIPATree


class StructureManagementService(TcService):
    closeAttachmentWindow = imp8.closeAttachmentWindow
    copyEBOPStructure = imp12.copyEBOPStructure
    copyRecursively = imp13.copyRecursively
    createCollabPlanningContext = imp15.createCollabPlanningContext
    createOrUpdateAttachments = imp8.createOrUpdateAttachments
    deleteAttachments = imp8.deleteAttachments
    findAffectedCCs = imp23.findAffectedCCs
    getAttachmentLineChildren = imp8.getAttachmentLineChildren
    getBOMLineActivities = imp8.getBOMLineActivities
    getBOMLineAttachments = imp8.getBOMLineAttachments
    getReferenceContexts = imp36.getReferenceContexts
    getStructureContextActivityLines = imp8.getStructureContextActivityLines
    getStructureContextLines = imp12.getStructureContextLines
    getStructureContextTopLines = imp8.getStructureContextTopLines
    moveAndResequenceNodes = imp43.moveAndResequenceNodes
    pasteDuplicateStructure = imp12.pasteDuplicateStructure
    pasteDuplicateStructure2 = imp13.pasteDuplicateStructure
    setReferenceContexts = imp36.setReferenceContexts


class MFGPropertyCollectorService(TcService):
    collectProperties = imp10.collectProperties


class StructureSearchService(TcService):
    createOrUpdateAssignmentRecipe = imp17.createOrUpdateAssignmentRecipe
    deleteAssignmentRecipes = imp17.deleteAssignmentRecipes
    findStudies = imp28.findStudies
    getAssignmentRecipes = imp17.getAssignmentRecipes
    nextSearch = imp44.nextSearch
    resolveAssignmentRecipe = imp17.resolveAssignmentRecipe
    searchConnectedLines = imp46.searchConnectedLines
    startSearch = imp44.startSearch
    stopSearch = imp44.stopSearch


class ValidationService(TcService):
    executeValidations = imp21.executeValidations
    getAllRegisteredCallbacks = imp29.getAllRegisteredCallbacks
    getAllValidations = imp21.getAllValidations
    getMaturityReport = imp33.getMaturityReport


class ImportExportService(TcService):
    exportToBriefcase = imp22.exportToBriefcase
    importFromBriefcase = imp39.importFromBriefcase
    importManufacturingFeatures = imp40.importManufacturingFeatures
    importManufacturingFeatures2 = imp41.importManufacturingFeatures
    importManufacturingFeatures3 = imp22.importManufacturingFeatures
    importManufaturingFeatures = imp42.importManufaturingFeatures


class CoreService(TcService):
    findCheckedOutsInStructure = imp25.findCheckedOutsInStructure
    findNodeInContext = imp26.findNodeInContext
    findNodeInContext2 = imp27.findNodeInContext
    getAffectedProperties = imp26.getAffectedProperties
    matchObjectsAgainstVariantRules = imp27.matchObjectsAgainstVariantRules


class ModelDefinitionsService(TcService):
    getManufacturingPropretyDescs = imp32.getManufacturingPropretyDescs
    getValidRelationTypes = imp32.getValidRelationTypes


class ConstraintsService(TcService):
    getPrecedenceConstraintPaths = imp35.getPrecedenceConstraintPaths
    getPrecedenceConstraints = imp35.getPrecedenceConstraints
    validateConstraintConsistency = imp35.validateConstraintConsistency
    validateProcessAreaAssignments = imp35.validateProcessAreaAssignments


class TimeWayPlanService(TcService):
    getTWPInformation = imp38.getTWPInformation
    setProductImage = imp38.setProductImage
