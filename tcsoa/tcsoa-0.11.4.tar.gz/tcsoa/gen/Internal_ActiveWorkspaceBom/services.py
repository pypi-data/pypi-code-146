from tcsoa.gen.Internal_ActiveWorkspaceBom._2018_12.services import OccurrenceManagementService as imp0
from tcsoa.gen.Internal_ActiveWorkspaceBom._2019_06.services import OccurrenceManagementService as imp1
from tcsoa.gen.Internal_ActiveWorkspaceBom._2016_03.services import OccurrenceManagementService as imp2
from tcsoa.gen.Internal_ActiveWorkspaceBom._2018_05.services import OccurrenceManagementService as imp3
from tcsoa.gen.Internal_ActiveWorkspaceBom._2018_12.services import MarkupService as imp4
from tcsoa.gen.Internal_ActiveWorkspaceBom._2015_03.services import OccurrenceManagementService as imp5
from tcsoa.gen.Internal_ActiveWorkspaceBom._2018_12.services import CompareService as imp6
from tcsoa.gen.Internal_ActiveWorkspaceBom._2019_06.services import CompareService as imp7
from tcsoa.gen.Internal_ActiveWorkspaceBom._2017_06.services import OccurrenceManagementService as imp8
from tcsoa.gen.Internal_ActiveWorkspaceBom._2012_10.services import BOMIndexManagementService as imp9
from tcsoa.gen.Internal_ActiveWorkspaceBom._2019_12.services import OccurrenceConfigurationService as imp10
from tcsoa.gen.Internal_ActiveWorkspaceBom._2019_12.services import OccurrenceManagementService as imp11
from tcsoa.gen.Internal_ActiveWorkspaceBom._2015_07.services import OccurrenceManagementService as imp12
from tcsoa.gen.Internal_ActiveWorkspaceBom._2020_12.services import OccurrenceManagementService as imp13
from tcsoa.gen.Internal_ActiveWorkspaceBom._2012_10.services import OccurrenceManagementService as imp14
from tcsoa.gen.Internal_ActiveWorkspaceBom._2017_06.services import OccurrenceConfigurationService as imp15
from tcsoa.gen.Internal_ActiveWorkspaceBom._2017_12.services import OccurrenceManagementService as imp16
from tcsoa.gen.Internal_ActiveWorkspaceBom._2019_12.services import DataManagementService as imp17
from tcsoa.gen.Internal_ActiveWorkspaceBom._2015_10.services import OccurrenceManagementService as imp18
from tcsoa.gen.Internal_ActiveWorkspaceBom._2020_05.services import OccurrenceManagementService as imp19
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):
    addObject = imp0.addObject
    addObject2 = imp1.addObject2
    addOrRemoveOccurrenceEffectivities = imp2.addOrRemoveOccurrenceEffectivities
    addSubstitutes = imp3.addSubstitutes
    addToBookmark2 = imp2.addToBookmark2
    attachObjects = imp5.attachObjects
    cloneContent = imp1.cloneContent
    cloneContentAsync = imp1.cloneContentAsync
    createAndAddElementEffectivity = imp8.createAndAddElementEffectivity
    detachObjects = imp11.detachObjects
    duplicateAndReplace = imp3.duplicateAndReplace
    duplicateAndReplaceAsync = imp3.duplicateAndReplaceAsync
    editElementEffectivity = imp8.editElementEffectivity
    findMatchingFilters = imp12.findMatchingFilters
    findMatchingFilters2 = imp11.findMatchingFilters2
    getAllowedOccurrenceTypes = imp13.getAllowedOccurrenceTypes
    getChildOccurrences = imp14.getChildOccurrences
    getInfoForAddElement = imp14.getInfoForAddElement
    getInfoForAddElement2 = imp1.getInfoForAddElement2
    getInfoForAddElement3 = imp11.getInfoForAddElement3
    getInfoForAddToBookmark = imp14.getInfoForAddToBookmark
    getInfoForInsertLevel = imp13.getInfoForInsertLevel
    getNextChildOccurrences = imp14.getNextChildOccurrences
    getNextOccurrencesInProduct = imp14.getNextOccurrencesInProduct
    getOccurrences = imp0.getOccurrences
    getOccurrences2 = imp1.getOccurrences2
    getOccurrences3 = imp11.getOccurrences3
    getOccurrencesInProduct = imp14.getOccurrencesInProduct
    getPackedOccurrenceCSIDs = imp16.getPackedOccurrenceCSIDs
    getSubsetInfo2 = imp2.getSubsetInfo2
    getSubsetInfo3 = imp11.getSubsetInfo3
    insertLevel = imp14.insertLevel
    insertLevel2 = imp13.insertLevel2
    packSimilarElements = imp1.packSimilarElements
    preferSubstitute = imp3.preferSubstitute
    removeElements = imp3.removeElements
    removeInContextPropertyOverride = imp11.removeInContextPropertyOverride
    removeLevel = imp13.removeLevel
    removeSubstitutes = imp3.removeSubstitutes
    replaceElement = imp2.replaceElement
    resetUserWorkingContextState = imp13.resetUserWorkingContextState
    saveSelections = imp18.saveSelections
    saveUserWorkingContextState = imp8.saveUserWorkingContextState
    saveUserWorkingContextState2 = imp1.saveUserWorkingContextState2
    saveWorkingContext = imp19.saveWorkingContext
    updateContentBasedOnRevision = imp19.updateContentBasedOnRevision
    updateSavedBookmark = imp14.updateSavedBookmark
    updateWorkingContext = imp19.updateWorkingContext


class MarkupService(TcService):
    applyMarkup = imp4.applyMarkup
    cancelMarkup = imp4.cancelMarkup


class CompareService(TcService):
    compareContent2 = imp6.compareContent2
    compareContentAsync2 = imp7.compareContentAsync2
    getCompareOptions = imp6.getCompareOptions


class BOMIndexManagementService(TcService):
    createBOMIndexAdminData = imp9.createBOMIndexAdminData
    processBomIndex = imp9.processBomIndex


class OccurrenceConfigurationService(TcService):
    createOrUpdateClassicVariantRule = imp10.createOrUpdateClassicVariantRule
    getClassicVariants = imp10.getClassicVariants
    getConfigurationRules = imp15.getConfigurationRules
    getConfigurationRules2 = imp10.getConfigurationRules2


class DataManagementService(TcService):
    getViewModelForCreate = imp17.getViewModelForCreate
