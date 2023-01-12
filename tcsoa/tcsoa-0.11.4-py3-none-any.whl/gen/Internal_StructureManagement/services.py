from tcsoa.gen.Internal_StructureManagement._2007_06.services import GlobalAlternateService as imp0
from tcsoa.gen.Internal_StructureManagement._2016_03.services import StructureVerificationService as imp1
from tcsoa.gen.Internal_StructureManagement._2010_04.services import BOMMarkupService as imp2
from tcsoa.gen.Internal_StructureManagement._2019_06.services import VariantManagementService as imp3
from tcsoa.gen.Internal_StructureManagement._2015_10.services import VariantManagementService as imp4
from tcsoa.gen.Internal_StructureManagement._2008_06.services import StructureService as imp5
from tcsoa.gen.Internal_StructureManagement._2007_06.services import PublishByLinkService as imp6
from tcsoa.gen.Internal_StructureManagement._2011_06.services import StructureService as imp7
from tcsoa.gen.Internal_StructureManagement._2009_10.services import EffectivitiesManagementService as imp8
from tcsoa.gen.Internal_StructureManagement._2014_12.services import StructureVerificationService as imp9
from tcsoa.gen.Internal_StructureManagement._2020_05.services import RevisionRuleAdministrationService as imp10
from tcsoa.gen.Internal_StructureManagement._2016_10.services import EffectivityService as imp11
from tcsoa.gen.Internal_StructureManagement._2013_05.services import StructureExpansionLiteService as imp12
from tcsoa.gen.Internal_StructureManagement._2013_12.services import StructureExpansionLiteService as imp13
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureExpansionLiteService as imp14
from tcsoa.gen.Internal_StructureManagement._2012_02.services import StructureVerificationService as imp15
from tcsoa.gen.Internal_StructureManagement._2011_06.services import IncrementalChangeService as imp16
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureVerificationService as imp17
from tcsoa.gen.Internal_StructureManagement._2011_06.services import VariantManagementService as imp18
from tcsoa.gen.Internal_StructureManagement._2014_12.services import BrokenLinksService as imp19
from tcsoa.gen.Internal_StructureManagement._2007_12.services import BrokenLinksService as imp20
from tcsoa.gen.Internal_StructureManagement._2018_11.services import StructureVerificationService as imp21
from tcsoa.gen.Internal_StructureManagement._2012_09.services import StructureVerificationService as imp22
from tcsoa.gen.Internal_StructureManagement._2018_11.services import MassUpdateService as imp23
from tcsoa.gen.Internal_StructureManagement._2007_06.services import RestructureService as imp24
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureLiteConversionService as imp25
from tcsoa.gen.Internal_StructureManagement._2008_05.services import RestructureService as imp26
from tcsoa.gen.Internal_StructureManagement._2014_12.services import RestructureService as imp27
from tcsoa.gen.Internal_StructureManagement._2008_03.services import StructureService as imp28
from tcsoa.gen.Internal_StructureManagement._2010_09.services import StructureService as imp29
from tcsoa.gen.Internal_StructureManagement._2007_06.services import RedliningService as imp30
from tcsoa.gen.Internal_StructureManagement._2008_05.services import StructureService as imp31
from tcsoa.base import TcService


class GlobalAlternateService(TcService):
    addRelatedGlobalAlternates = imp0.addRelatedGlobalAlternates
    listGlobalAlternates = imp0.listGlobalAlternates
    removeRelatedGlobalAlternates = imp0.removeRelatedGlobalAlternates
    setPreferredGlobalAlternate = imp0.setPreferredGlobalAlternate


class StructureVerificationService(TcService):
    alignMatchedCandidates = imp1.alignMatchedCandidates
    createOrUpdatePropagationDetails = imp9.createOrUpdatePropagationDetails
    createOrUpdateReviewStatus = imp9.createOrUpdateReviewStatus
    findMatchingCandidates = imp1.findMatchingCandidates
    findReviewStatus = imp9.findReviewStatus
    getActivitiesComparisonDetails = imp15.getActivitiesComparisonDetails
    getAttachmentComparisonDetails = imp17.getAttachmentComparisonDetails
    getMountAttachComparisonDetails = imp21.getMountAttachComparisonDetails
    getPropertyPropagationStatusDetails = imp9.getPropertyPropagationStatusDetails
    getStructureChangeDetails = imp9.getStructureChangeDetails
    getStructureChangeImpactedLines = imp9.getStructureChangeImpactedLines
    getToolRequirementComparisonDetails = imp15.getToolRequirementComparisonDetails
    getValidCriteria = imp22.getValidCriteria


class BOMMarkupService(TcService):
    applyBOMMarkup = imp2.applyBOMMarkup
    createBOMMarkup = imp2.createBOMMarkup
    savePendingEditsAsMarkup = imp2.savePendingEditsAsMarkup


class VariantManagementService(TcService):
    applyRollupVariantConfiguration = imp3.applyRollupVariantConfiguration
    applyVariantConfiguration = imp4.applyVariantConfiguration
    getBOMVariantConfigOptions = imp18.getBOMVariantConfigOptions
    getModularOptionsForBom = imp18.getModularOptionsForBom


class StructureService(TcService):
    copyRecursively = imp5.copyRecursively
    createOrSavePSBOMViewRevision = imp7.createOrSavePSBOMViewRevision
    findHighestFindNumberInExpand = imp5.findHighestFindNumberInExpand
    getAvailableViewTypes = imp7.getAvailableViewTypes
    resequence = imp28.resequence
    resequence2 = imp29.resequence
    syncAlignedOccurrences = imp31.syncAlignedOccurrences


class PublishByLinkService(TcService):
    createIDCWindowForDesignAsm = imp6.createIDCWindowForDesignAsm


class EffectivitiesManagementService(TcService):
    createOrUpdateEffectivites = imp8.createOrUpdateEffectivites
    getEffectivityGrpRevList = imp8.getEffectivityGrpRevList
    setEndItemEffectivityGroups = imp8.setEndItemEffectivityGroups


class RevisionRuleAdministrationService(TcService):
    createOrUpdateRevisionRule = imp10.createOrUpdateRevisionRule
    getRevisionRuleInfo = imp10.getRevisionRuleInfo


class EffectivityService(TcService):
    cutbackUnitOccurrenceEffectivity = imp11.cutbackUnitOccurrenceEffectivity
    getUnitNetOccurrenceEffectivity = imp11.getUnitNetOccurrenceEffectivity


class StructureExpansionLiteService(TcService):
    expandBasedOnOccurrenceList = imp12.expandBasedOnOccurrenceList
    expandBasedOnOccurrenceList2 = imp13.expandBasedOnOccurrenceList2
    expandNext = imp12.expandNext
    expandNext2 = imp13.expandNext2
    expandNext3 = imp14.expandNext3
    getUndelivered = imp12.getUndelivered
    getUndelivered2 = imp13.getUndelivered2
    getUndelivered3 = imp14.getUndelivered3
    unloadBelow = imp12.unloadBelow
    unloadBelow2 = imp13.unloadBelow2


class IncrementalChangeService(TcService):
    getAttachmentChanges = imp16.getAttachmentChanges
    getAttributeChanges = imp16.getAttributeChanges
    getParentAndChildComponents = imp16.getParentAndChildComponents
    getPredecessorChanges = imp16.getPredecessorChanges
    getStructureChanges = imp16.getStructureChanges


class BrokenLinksService(TcService):
    getBrokenLinkAndReplacements = imp19.getBrokenLinkAndReplacements
    getBrokenLinkInfoWithFixOpt = imp20.getBrokenLinkInfoWithFixOpt
    repairBrokenLinks = imp20.repairBrokenLinks


class MassUpdateService(TcService):
    hasActiveMarkupAssociated = imp23.hasActiveMarkupAssociated
    saveImpactedAssemblies = imp23.saveImpactedAssemblies


class RestructureService(TcService):
    insertLevel = imp24.insertLevel
    moveNode = imp24.moveNode
    removeLevel = imp24.removeLevel
    replaceInContext = imp26.replaceInContext
    replaceItems = imp27.replaceItems
    splitOccurrence = imp24.splitOccurrence


class StructureLiteConversionService(TcService):
    liteBOMLinesToBOMLines = imp25.liteBOMLinesToBOMLines


class RedliningService(TcService):
    revertAllPendingEdits = imp30.revertAllPendingEdits
    revertPendingEdits = imp30.revertPendingEdits
