from tcsoa.gen.StructureManagement._2008_12.services import StructureVerificationService as imp0
from tcsoa.gen.StructureManagement._2010_09.services import StructureVerificationService as imp1
from tcsoa.gen.StructureManagement._2012_02.services import StructureVerificationService as imp2
from tcsoa.gen.StructureManagement._2016_05.services import StructureVerificationService as imp3
from tcsoa.gen.StructureManagement._2012_09.services import StructureService as imp4
from tcsoa.gen.StructureManagement._2007_06.services import PublishByLinkService as imp5
from tcsoa.gen.StructureManagement._2013_05.services import VariantManagementService as imp6
from tcsoa.gen.StructureManagement._2019_06.services import VariantManagementService as imp7
from tcsoa.gen.StructureManagement._2008_03.services import CompositionService as imp8
from tcsoa.gen.StructureManagement._2012_02.services import IncrementalChangeService as imp9
from tcsoa.gen.StructureManagement._2008_05.services import StructureVerificationService as imp10
from tcsoa.gen.StructureManagement._2014_10.services import StructureService as imp11
from tcsoa.gen.StructureManagement._2012_09.services import VariantManagementService as imp12
from tcsoa.gen.StructureManagement._2018_11.services import StructureService as imp13
from tcsoa.gen.StructureManagement._2014_12.services import EffectivityService as imp14
from tcsoa.gen.StructureManagement._2012_10.services import StructureService as imp15
from tcsoa.gen.StructureManagement._2012_09.services import PublishByLinkService as imp16
from tcsoa.gen.StructureManagement._2008_06.services import StructureService as imp17
from tcsoa.gen.StructureManagement._2010_09.services import StructureService as imp18
from tcsoa.gen.StructureManagement._2011_06.services import StructureService as imp19
from tcsoa.gen.StructureManagement._2015_10.services import EffectivityService as imp20
from tcsoa.gen.StructureManagement._2014_10.services import MassUpdateService as imp21
from tcsoa.gen.StructureManagement._2014_06.services import StructureFilterWithExpandService as imp22
from tcsoa.gen.StructureManagement._2016_09.services import PublishByLinkService as imp23
from tcsoa.gen.StructureManagement._2014_06.services import StructureVerificationService as imp24
from tcsoa.gen.StructureManagement._2010_09.services import StructureSearchService as imp25
from tcsoa.gen.StructureManagement._2012_10.services import StructureVerificationService as imp26
from tcsoa.gen.StructureManagement._2013_05.services import StructureVerificationService as imp27
from tcsoa.gen.StructureManagement._2014_12.services import StructureSearchService as imp28
from tcsoa.gen.StructureManagement._2012_09.services import MassUpdateService as imp29
from tcsoa.gen.StructureManagement._2008_05.services import StructureSearchService as imp30
from tcsoa.gen.StructureManagement._2017_05.services import StructureSearchService as imp31
from tcsoa.gen.StructureManagement._2013_05.services import IncrementalChangeService as imp32
from tcsoa.gen.StructureManagement._2010_04.services import StructureSearchService as imp33
from tcsoa.base import TcService


class StructureVerificationService(TcService):
    accountabilityCheck = imp0.accountabilityCheck
    accountabilityCheck2 = imp1.accountabilityCheck
    accountabilityCheck3 = imp2.accountabilityCheck
    accountabilityCheck4 = imp3.accountabilityCheck2
    accountabilityCheckAsync = imp2.accountabilityCheckAsync
    checkAlignment = imp10.checkAlignment
    compareNetEffectivity = imp1.compareNetEffectivity
    compareNetEffectivity2 = imp2.compareNetEffectivity
    getACFavorite = imp24.getACFavorite
    getAssignmentComparisonDetails = imp2.getAssignmentComparisonDetails
    getAssignmentComparisonDetails2 = imp26.getAssignmentComparisonDetails
    getAttrGrpsAndFormsComparisonDetail = imp3.getAttrGrpsAndFormsComparisonDetail
    getAttributeGroupsAndFormsComparisonDetails = imp27.getAttributeGroupsAndFormsComparisonDetails
    getComparisonSummaries = imp26.getComparisonSummaries
    getConnectedObjectsComparisonDetails = imp27.getConnectedObjectsComparisonDetails
    getDescendentComparisonDetails = imp2.getDescendentComparisonDetails
    getPartitionComparisonDetails = imp2.getPartitionComparisonDetails
    getPredecessorComparisonDetails = imp2.getPredecessorComparisonDetails
    getPropertyComparisonDetails = imp2.getPropertyComparisonDetails
    manageACFavorites = imp24.manageACFavorites
    propagateProperties = imp2.propagateProperties


class StructureService(TcService):
    add = imp4.add
    cloneStructure = imp11.cloneStructure
    cloneStructureAsync = imp11.cloneStructureAsync
    cloneStructureExpandOrUpdate = imp11.cloneStructureExpandOrUpdate
    createInterchangeableGroups = imp13.createInterchangeableGroups
    cutItems = imp15.cutItems
    duplicate = imp17.duplicate
    duplicate2 = imp18.duplicate2
    duplicate3 = imp19.duplicate3
    expandOrUpdateDuplicateItems = imp17.expandOrUpdateDuplicateItems
    expandOrUpdateDuplicateItems2 = imp18.expandOrUpdateDuplicateItems2
    expandOrUpdateDuplicateItems3 = imp19.expandOrUpdateDuplicateItems3
    packOrUnpack = imp18.packOrUnpack
    setClosureRuleVariablesAndValues = imp19.setClosureRuleVariablesAndValues
    toggleOccurrenceSuppression = imp11.toggleOccurrenceSuppression
    togglePrecision = imp11.togglePrecision
    unloadBelow = imp19.unloadBelow
    validateOccurrenceConditions = imp4.validateOccurrenceConditions
    validateParentChildConditions = imp4.validateParentChildConditions
    validateStructureItemIds = imp17.validateStructureItemIds
    validateStructureItemIds2 = imp18.validateStructureItemIds2
    validateStructureItemIds3 = imp19.validateStructureItemIds3


class PublishByLinkService(TcService):
    addTargets = imp5.addTargets
    completenessCheck = imp5.completenessCheck
    createLinks = imp5.createLinks
    deleteLinkForSource = imp5.deleteLinkForSource
    deleteLinksForSource2 = imp16.deleteLinksForSource2
    deleteTargetsFromLink = imp5.deleteTargetsFromLink
    findLinesWithSameLogicalIdentity = imp5.findLinesWithSameLogicalIdentity
    findSourceInWindow = imp5.findSourceInWindow
    findSourcesInWindow = imp23.findSourcesInWindow
    findTargetsInWindow = imp5.findTargetsInWindow
    getSourceTopLevel = imp5.getSourceTopLevel
    publishData = imp5.publishData


class VariantManagementService(TcService):
    applyBOMVariantRules = imp6.applyBOMVariantRules
    applyBOMVariantRules2 = imp7.applyBOMVariantRules2
    createAndSubstituteVariantItem = imp12.createAndSubstituteVariantItem
    createVariantItem = imp12.createVariantItem
    getBOMVariantRules = imp6.getBOMVariantRules
    getBOMVariantRules2 = imp7.getBOMVariantRules2
    getVariantExpressionsMatchInfo = imp6.getVariantExpressionsMatchInfo
    setBOMVariantRules = imp6.setBOMVariantRules
    setBOMVariantRules2 = imp7.setBOMVariantRules2


class CompositionService(TcService):
    assignChildLines = imp8.assignChildLines


class IncrementalChangeService(TcService):
    carryOver = imp9.carryOver
    removeIncrementalChanges = imp32.removeIncrementalChanges


class EffectivityService(TcService):
    createOccurrenceEffectivities = imp14.createOccurrenceEffectivities
    createReleaseStatusEffectivity = imp14.createReleaseStatusEffectivity
    editOccurrenceEffectivity = imp20.editOccurrenceEffectivity
    editReleaseStatusEffectivity = imp20.editReleaseStatusEffectivity
    removeOccurrenceEffectivities = imp20.removeOccurrenceEffectivities
    removeReleaseStatusEffectivity = imp20.removeReleaseStatusEffectivity


class MassUpdateService(TcService):
    executeMarkupChanges = imp21.executeMarkupChanges
    expandOneLevel = imp21.expandOneLevel
    getImpactedObjectDetails = imp21.getImpactedObjectDetails
    getImpactedObjects = imp21.getImpactedObjects
    getMarkupChangesForUpdate = imp21.getMarkupChangesForUpdate
    getRevisionRules = imp21.getRevisionRules
    manageImpactedObjectUpdates = imp21.manageImpactedObjectUpdates
    massGetAffectedParents = imp29.massGetAffectedParents
    massUpdateExecutionECN = imp29.massUpdateExecutionECN
    massUpdateExecutionECR = imp29.massUpdateExecutionECR
    updateImpactedObjects = imp21.updateImpactedObjects
    updateImpactedObjectsEnd = imp21.updateImpactedObjectsEnd
    updateImpactedObjectsStart = imp21.updateImpactedObjectsStart
    validateChangeObjectForMassUpdate = imp21.validateChangeObjectForMassUpdate


class StructureFilterWithExpandService(TcService):
    expandAndSearch = imp22.expandAndSearch


class StructureSearchService(TcService):
    getAssemblyBoundingBox = imp25.getAssemblyBoundingBox
    getStructureChanges = imp28.getStructureChanges
    isSpatialDataAvailable = imp25.isSpatialDataAvailable
    nextSearch = imp30.nextSearch
    nextSearch2 = imp31.nextSearch2
    startSearch = imp30.startSearch
    startSearch2 = imp33.startSearch
    startSearch3 = imp25.startSearch
    startSearch4 = imp31.startSearch2
    stopSearch = imp30.stopSearch
    stopSearch2 = imp31.stopSearch2
