from tcsoa.gen.Internal_AWS2._2018_05.services import GlobalAlternateService as imp0
from tcsoa.gen.Internal_AWS2._2017_06.services import EffectivityManagmentService as imp1
from tcsoa.gen.Internal_AWS2._2015_03.services import FullTextSearchService as imp2
from tcsoa.gen.Internal_AWS2._2012_10.services import DataManagementService as imp3
from tcsoa.gen.Internal_AWS2._2019_06.services import AdvancedSavedSearchService as imp4
from tcsoa.gen.Internal_AWS2._2016_12.services import AdvancedSearchService as imp5
from tcsoa.gen.Internal_AWS2._2017_06.services import RequirementsManagementService as imp6
from tcsoa.gen.Internal_AWS2._2012_10.services import FullTextSearchService as imp7
from tcsoa.gen.Internal_AWS2._2015_10.services import FullTextSearchService as imp8
from tcsoa.gen.Internal_AWS2._2018_05.services import FullTextSearchService as imp9
from tcsoa.gen.Internal_AWS2._2019_12.services import DataManagementService as imp10
from tcsoa.gen.Internal_AWS2._2020_05.services import UiConfigService as imp11
from tcsoa.gen.Internal_AWS2._2016_12.services import RequirementsManagementService as imp12
from tcsoa.gen.Internal_AWS2._2019_12.services import FinderService as imp13
from tcsoa.gen.Internal_AWS2._2018_12.services import FinderService as imp14
from tcsoa.gen.Internal_AWS2._2012_10.services import RequirementsManagementService as imp15
from tcsoa.gen.Internal_AWS2._2016_03.services import RequirementsManagementService as imp16
from tcsoa.gen.Internal_AWS2._2018_12.services import MultiSiteService as imp17
from tcsoa.gen.Internal_AWS2._2012_10.services import FinderService as imp18
from tcsoa.gen.Internal_AWS2._2017_12.services import DataManagementService as imp19
from tcsoa.gen.Internal_AWS2._2016_03.services import FinderService as imp20
from tcsoa.gen.Internal_AWS2._2018_05.services import DataManagementService as imp21
from tcsoa.gen.Internal_AWS2._2015_10.services import DataManagementService as imp22
from tcsoa.gen.Internal_AWS2._2016_12.services import DataManagementService as imp23
from tcsoa.gen.Internal_AWS2._2018_05.services import TCXMLService as imp24
from tcsoa.gen.Internal_AWS2._2014_11.services import RequirementsManagementService as imp25
from tcsoa.gen.Internal_AWS2._2020_05.services import FileMgmtService as imp26
from tcsoa.gen.Internal_AWS2._2019_06.services import RequirementsManagementService as imp27
from tcsoa.gen.Internal_AWS2._2012_10.services import OrganizationManagementService as imp28
from tcsoa.gen.Internal_AWS2._2013_12.services import OrganizationManagementService as imp29
from tcsoa.gen.Internal_AWS2._2017_12.services import FullTextSearchService as imp30
from tcsoa.gen.Internal_AWS2._2012_10.services import LOVService as imp31
from tcsoa.gen.Internal_AWS2._2016_04.services import DataManagementService as imp32
from tcsoa.gen.Internal_AWS2._2020_12.services import DataManagementService as imp33
from tcsoa.gen.Internal_AWS2._2016_03.services import UiConfigService as imp34
from tcsoa.gen.Internal_AWS2._2017_06.services import UiConfigService as imp35
from tcsoa.gen.Internal_AWS2._2012_10.services import StructureSearchService as imp36
from tcsoa.gen.Internal_AWS2._2020_05.services import DataManagementService as imp37
from tcsoa.gen.Internal_AWS2._2020_05.services import FullTextSearchService as imp38
from tcsoa.gen.Internal_AWS2._2015_03.services import DataManagementService as imp39
from tcsoa.gen.Internal_AWS2._2016_03.services import DataManagementService as imp40
from tcsoa.gen.Internal_AWS2._2017_06.services import DataManagementService as imp41
from tcsoa.gen.Internal_AWS2._2013_12.services import DataManagementService as imp42
from tcsoa.gen.Internal_AWS2._2012_10.services import WorkflowService as imp43
from tcsoa.gen.Internal_AWS2._2014_11.services import WorkflowService as imp44
from tcsoa.gen.Internal_AWS2._2018_05.services import WorkflowService as imp45
from tcsoa.gen.Internal_AWS2._2017_06.services import FullTextSearchService as imp46
from tcsoa.gen.Internal_AWS2._2018_05.services import FileMgmtService as imp47
from tcsoa.gen.Internal_AWS2._2019_06.services import DataManagementService as imp48
from tcsoa.gen.Internal_AWS2._2018_05.services import FinderService as imp49
from tcsoa.gen.Internal_AWS2._2016_12.services import FinderService as imp50
from tcsoa.gen.Internal_AWS2._2017_06.services import FinderService as imp51
from tcsoa.gen.Internal_AWS2._2017_12.services import FinderService as imp52
from tcsoa.gen.Internal_AWS2._2019_06.services import FinderService as imp53
from tcsoa.gen.Internal_AWS2._2013_12.services import WorkflowService as imp54
from tcsoa.base import TcService


class GlobalAlternateService(TcService):
    addAlternates = imp0.addAlternates
    removeAlternates = imp0.removeAlternates


class EffectivityManagmentService(TcService):
    addOrRemoveRelStatusEffectivities = imp1.addOrRemoveRelStatusEffectivities


class FullTextSearchService(TcService):
    cleanupScratchTable = imp2.cleanupScratchTable
    createFullTextSavedSearch = imp7.createFullTextSavedSearch
    createFullTextSavedSearch2 = imp8.createFullTextSavedSearch
    createFullTextSavedSearch3 = imp9.createFullTextSavedSearch
    deleteFullTextSavedSearch = imp8.deleteFullTextSavedSearch
    deleteIndexedIslands = imp2.deleteIndexedIslands
    deregisterApplicationIDs = imp2.deregisterApplicationIDs
    findFullTextSavedSearches = imp7.findFullTextSavedSearches
    getAMImpactedObjects = imp2.getAMImpactedObjects
    getAddedObjectsToUpdateIndex = imp7.getAddedObjectsToUpdateIndex
    getAddedObjectsToUpdateIndex1 = imp7.getAddedObjectsToUpdateIndex1
    getDatasetIndexableFilesInfo = imp7.getDatasetIndexableFilesInfo
    getDeletedObjectsToUpdateIndex = imp7.getDeletedObjectsToUpdateIndex
    getDeletedObjectsToUpdateIndex1 = imp7.getDeletedObjectsToUpdateIndex1
    getImpactedItemRevsForReIndex = imp7.getImpactedItemRevsForReIndex
    getIndexedObjects = imp2.getIndexedObjects
    getIndexedObjectsAndUpdate = imp30.getIndexedObjectsAndUpdate
    getModifiedObjectsToSync = imp2.getModifiedObjectsToSync
    getObjectsToIndex = imp7.getObjectsToIndex
    getPreFilters = imp7.getPreFilters
    getSearchSettings = imp38.getSearchSettings
    getSuggestions = imp7.getSuggestions
    identifyImpactedObjects = imp46.identifyImpactedObjects
    modifyFullTextSavedSearch = imp8.modifyFullTextSavedSearch
    modifyFullTextSavedSearch2 = imp9.modifyFullTextSavedSearch
    performFullTextSearch = imp7.performFullTextSearch
    queryAndUpdateSyncData = imp30.queryAndUpdateSyncData
    updateIndexIslandStatus = imp2.updateIndexIslandStatus
    updateIndexingStatus = imp7.updateIndexingStatus


class DataManagementService(TcService):
    clearHistory = imp3.clearHistory
    createIdDisplayRules = imp10.createIdDisplayRules
    getAvailableWorkspaces = imp19.getAvailableWorkspaces
    getChildren = imp3.getChildren
    getCurrentUserGateway = imp3.getCurrentUserGateway
    getCurrentUserGateway2 = imp21.getCurrentUserGateway2
    getDatasetTypesWithDefaultRelation = imp22.getDatasetTypesWithDefaultRelation
    getDeclarativeStyleSheets = imp23.getDeclarativeStyleSheets
    getDefaultRelation = imp23.getDefaultRelation
    getHistory = imp3.getHistory
    getIdContexts = imp10.getIdContexts
    getIdentifierTypes = imp10.getIdentifierTypes
    getInitialTableRowData = imp32.getInitialTableRowData
    getLocalizedProperties = imp33.getLocalizedProperties
    getRelatedObjsForConfiguredRevision = imp37.getRelatedObjsForConfiguredRevision
    getStyleSheet = imp39.getStyleSheet
    getStyleSheet2 = imp32.getStyleSheet
    getStyleSheet3 = imp40.getStyleSheet2
    getStyleSheet4 = imp41.getStyleSheet3
    getTCSessionAnalyticsInfo = imp19.getTCSessionAnalyticsInfo
    getTCSessionInfo = imp3.getTCSessionInfo
    getTCSessionInfo2 = imp42.getTCSessionInfo2
    getTCSessionInfo3 = imp42.getTCSessionInfo3
    getTableViewModelProperties = imp19.getTableViewModelProperties
    getUnprocessedXRT = imp40.getUnprocessedXRT
    getViewModelProperties = imp41.getViewModelProperties
    getViewModelProperties2 = imp19.getViewModelProperties2
    getViewerData = imp41.getViewerData
    loadDataForEditing = imp3.loadDataForEditing
    loadDataForEditing2 = imp32.loadDataForEditing
    loadViewModelForEditing = imp41.loadViewModelForEditing
    loadViewModelForEditing2 = imp19.loadViewModelForEditing2
    modifyFavorites = imp48.modifyFavorites
    pinObjects = imp21.pinObjects
    saveEdit = imp3.saveEdit
    saveEditAndSubmitToWorkflow = imp3.saveEditAndSubmitToWorkflow
    saveEditAndSubmitToWorkflow2 = imp32.saveEditAndSubmitToWorkflow
    saveEditAndSubmitToWorkflow3 = imp23.saveEditAndSubmitToWorkflow
    saveViewModelEditAndSubmitWorkflow = imp41.saveViewModelEditAndSubmitWorkflow
    saveViewModelEditAndSubmitWorkflow2 = imp21.saveViewModelEditAndSubmitWorkflow2
    saveXRT = imp40.saveXRT
    setLocalizedProperties = imp33.setLocalizedProperties
    unpinObjects = imp21.unpinObjects
    updateHistory = imp3.updateHistory
    updateTiles = imp21.updateTiles


class AdvancedSavedSearchService(TcService):
    createAdvancedSavedSearch = imp4.createAdvancedSavedSearch
    updateAdvancedSavedSearch = imp4.updateAdvancedSavedSearch


class AdvancedSearchService(TcService):
    createAdvancedSearchInput = imp5.createAdvancedSearchInput
    getSelectedQueryCriteria = imp5.getSelectedQueryCriteria


class RequirementsManagementService(TcService):
    createBaseline = imp6.createBaseline
    createBaselineAsync = imp6.createBaselineAsync
    exportAsync = imp12.exportAsync
    exportAsync2 = imp6.exportAsync2
    exportToApplication = imp15.exportToApplication
    exportToApplication2 = imp16.exportToApplication
    exportToApplication3 = imp12.exportToApplication2
    exportToApplication4 = imp6.exportToApplication3
    getExportTemplates = imp25.getExportTemplates
    getFullTextVersionInfo = imp27.getFullTextVersionInfo
    setRichContent = imp15.setRichContent
    setRichContent2 = imp12.setRichContent2


class UiConfigService(TcService):
    createNamedColumnConfig = imp11.createNamedColumnConfig
    deleteNamedColumnConfig = imp11.deleteNamedColumnConfig
    getNamedColumnConfigs = imp11.getNamedColumnConfigs
    getOrResetUIColumnConfigs = imp34.getOrResetUIColumnConfigs
    getOrResetUIColumnConfigs2 = imp35.getOrResetUIColumnConfigs2
    getVisibleCommands = imp34.getVisibleCommands
    loadNamedColumnConfig = imp11.loadNamedColumnConfig
    saveNamedColumnConfig = imp11.saveNamedColumnConfig
    saveUIColumnConfigs = imp34.saveUIColumnConfigs


class FinderService(TcService):
    exportObjectsToFile = imp13.exportObjectsToFile
    exportSearchResults = imp14.exportSearchResults
    findObjectsByClassAndAttributes2 = imp18.findObjectsByClassAndAttributes2
    findUsersTasks = imp18.findUsersTasks
    getClassificationProps = imp20.getClassificationProps
    getFilterValues = imp13.getFilterValues
    performFacetSearch = imp49.performFacetSearch
    performSearch = imp20.performSearch
    performSearch2 = imp50.performSearch2
    performSearchViewModel = imp51.performSearchViewModel
    performSearchViewModel2 = imp52.performSearchViewModel2
    performSearchViewModel3 = imp49.performSearchViewModel3
    performSearchViewModel4 = imp53.performSearchViewModel4


class MultiSiteService(TcService):
    fetchODSRecords = imp17.fetchODSRecords


class TCXMLService(TcService):
    getDiagnosticInfoForAcctTables = imp24.getDiagnosticInfoForAcctTables
    installDBTriggersForDataSync = imp24.installDBTriggersForDataSync
    removeDBTriggersForDataSync = imp24.removeDBTriggersForDataSync


class FileMgmtService(TcService):
    getFileNamesWithTicketInfo = imp26.getFileNamesWithTicketInfo
    loadPlmdTicketForReplace = imp47.loadPlmdTicketForReplace


class OrganizationManagementService(TcService):
    getGroupMembership = imp28.getGroupMembership
    getGroupMembership2 = imp29.getGroupMembership2


class LOVService(TcService):
    getInitialLOVValues = imp31.getInitialLOVValues
    getNextLOVValues = imp31.getNextLOVValues
    validateLOVValueSelections = imp31.validateLOVValueSelections


class StructureSearchService(TcService):
    getParentsWhereUsed = imp36.getParentsWhereUsed
    getProductsWhereUsed = imp36.getProductsWhereUsed


class WorkflowService(TcService):
    getTaskResults = imp43.getTaskResults
    getWorkflowGraph = imp44.getWorkflowGraph
    getWorkflowGraphLegend = imp44.getWorkflowGraphLegend
    getWorkflowTaskViewModel = imp45.getWorkflowTaskViewModel
    performTaskSearch = imp54.performTaskSearch
