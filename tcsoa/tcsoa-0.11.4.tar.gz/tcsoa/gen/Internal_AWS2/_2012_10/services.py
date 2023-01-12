from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, EPMTaskTemplate, RevisionRule, ItemRevision
from tcsoa.gen.Internal.AWS2._2012_10.FullTextSearch import FullTextSearchInput, GetAddedObjectsToUpdateIndexResponse, FullTextSearchResponse, GetDeletedObjectsToUpdateIndexResponse, GetObjectsToIndexResponse, SearchSuggestionsResponse, GetAddedObjectsToUpdateIndexResponse1, CreateFullTextSavedSearchResponse, GetDeletedObjectsToUpdateIndexResponse1, UpdateIndexerStatusInput, FullTextSavedSearchInput, GetImpactedItemRevsForReIndexResponse, GetDatasetIndexableFilesInfoResponse, SearchSuggestionsInput, GetTcObjectsToIndexInput, PreFiltersResponse, FindFullTextSavedSearchesResponse
from tcsoa.gen.Internal.AWS2._2012_10.RequirementsManagement import SetContentInput, ExportToApplicationInputData, ExportToApplicationResponse
from tcsoa.gen.Internal.AWS2._2012_10.Finder import FindUsersTasksResponse, FindObjectsResponse2, FindObjectsInput2
from tcsoa.gen.Internal.AWS2._2012_10.DataManagement import SaveEditAndSubmitResponse, GetTCSessionInfoResponse, HistoryInput, LoadDataForEditingInfo, LoadDataForEditingResponse, SaveEditAndSubmitInfo, GetChildrenResponse, GetCurrentUserGatewayResponse, HistoryResult, SaveEditInfo
from tcsoa.gen.Internal.AWS2._2012_10.Workflow import GetTaskResultsResponse
from tcsoa.gen.Internal.AWS2._2012_10.OrganizationManagement import GroupMembershipInput, GroupMembershipResponse
from tcsoa.gen.Internal.AWS2._2012_10.LOV import LOVData, InitialLovData, LOVSearchResults, ValidateLOVValueSelectionsResponse, LOVInput
from typing import List
from tcsoa.gen.Internal.AWS2._2012_10.StructureSearch import ParentsWhereUsedResponse, ProductsWhereUsedRespone
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def getParentsWhereUsed(cls, itemRevisions: List[ItemRevision], revisionRule: RevisionRule, pageNumber: int) -> ParentsWhereUsedResponse:
        """
        The response of this operation is the list of Parent Item Revisions where each one of the input Item Revisions
        are used.
        """
        return cls.execute_soa_method(
            method_name='getParentsWhereUsed',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='StructureSearch',
            params={'itemRevisions': itemRevisions, 'revisionRule': revisionRule, 'pageNumber': pageNumber},
            response_cls=ParentsWhereUsedResponse,
        )

    @classmethod
    def getProductsWhereUsed(cls, itemRevisions: List[ItemRevision], pageNumber: int) -> ProductsWhereUsedRespone:
        """
        The response of this operation is the list of Product Items where each one of the input Item Revisions are used.
        """
        return cls.execute_soa_method(
            method_name='getProductsWhereUsed',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='StructureSearch',
            params={'itemRevisions': itemRevisions, 'pageNumber': pageNumber},
            response_cls=ProductsWhereUsedRespone,
        )


class FullTextSearchService(TcService):

    @classmethod
    def getPreFilters(cls) -> PreFiltersResponse:
        """
        Fetches the pre filter properties and their values from the preferences defined in the system.
        """
        return cls.execute_soa_method(
            method_name='getPreFilters',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={},
            response_cls=PreFiltersResponse,
        )

    @classmethod
    def getSuggestions(cls, searchInput: SearchSuggestionsInput) -> SearchSuggestionsResponse:
        """
        This operation returns a list of search suggestions for the given search string.
        """
        return cls.execute_soa_method(
            method_name='getSuggestions',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'searchInput': searchInput},
            response_cls=SearchSuggestionsResponse,
        )

    @classmethod
    def performFullTextSearch(cls, searchInput: FullTextSearchInput) -> FullTextSearchResponse:
        """
        This operation returns a list of business objects obtained after performing a full text search using the input
        search criteria.
        """
        return cls.execute_soa_method(
            method_name='performFullTextSearch',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'searchInput': searchInput},
            response_cls=FullTextSearchResponse,
        )

    @classmethod
    def updateIndexingStatus(cls, indexerStatusInput: UpdateIndexerStatusInput) -> ServiceData:
        """
        Updates the subscription table with the application id and processed date time of an action during indexing
        process.
        """
        return cls.execute_soa_method(
            method_name='updateIndexingStatus',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'indexerStatusInput': indexerStatusInput},
            response_cls=ServiceData,
        )

    @classmethod
    def createFullTextSavedSearch(cls, inputs: List[FullTextSavedSearchInput]) -> CreateFullTextSavedSearchResponse:
        """
        Create FullTextSavedSearch objects
        """
        return cls.execute_soa_method(
            method_name='createFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=CreateFullTextSavedSearchResponse,
        )

    @classmethod
    def findFullTextSavedSearches(cls) -> FindFullTextSavedSearchesResponse:
        """
        Find FullTextSavedSearch objects
        """
        return cls.execute_soa_method(
            method_name='findFullTextSavedSearches',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={},
            response_cls=FindFullTextSavedSearchesResponse,
        )

    @classmethod
    def getAddedObjectsToUpdateIndex(cls, applicationID: str) -> GetAddedObjectsToUpdateIndexResponse:
        """
        This operation queries the scratch table to identify objects that have been added since the last indexing
        operation.
        """
        return cls.execute_soa_method(
            method_name='getAddedObjectsToUpdateIndex',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'applicationID': applicationID},
            response_cls=GetAddedObjectsToUpdateIndexResponse,
        )

    @classmethod
    def getAddedObjectsToUpdateIndex1(cls, applicationID: str) -> GetAddedObjectsToUpdateIndexResponse1:
        """
        This operation queries the scratch table to identify objects that have been added since the last indexing
        operation.
        """
        return cls.execute_soa_method(
            method_name='getAddedObjectsToUpdateIndex1',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'applicationID': applicationID},
            response_cls=GetAddedObjectsToUpdateIndexResponse1,
        )

    @classmethod
    def getDatasetIndexableFilesInfo(cls, datasetUIDs: List[str]) -> GetDatasetIndexableFilesInfoResponse:
        """
        This operation finds all the files associated with the given list of datasets and filters out that are not
        supported for indexing. Finally returns back a map of datasets uids and supported files information of file UID
        and FMS read ticket for downloading the file.
        """
        return cls.execute_soa_method(
            method_name='getDatasetIndexableFilesInfo',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'datasetUIDs': datasetUIDs},
            response_cls=GetDatasetIndexableFilesInfoResponse,
        )

    @classmethod
    def getDeletedObjectsToUpdateIndex(cls, applicationID: str) -> GetDeletedObjectsToUpdateIndexResponse:
        """
        This operation queries the scratch table to identify objects that have been deleted since the last indexing
        operation.
        """
        return cls.execute_soa_method(
            method_name='getDeletedObjectsToUpdateIndex',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'applicationID': applicationID},
            response_cls=GetDeletedObjectsToUpdateIndexResponse,
        )

    @classmethod
    def getDeletedObjectsToUpdateIndex1(cls, applicationID: str) -> GetDeletedObjectsToUpdateIndexResponse1:
        """
        This operation queries the scratch table to identify objects that have been deleted since last indexing
        operation.
        """
        return cls.execute_soa_method(
            method_name='getDeletedObjectsToUpdateIndex1',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'applicationID': applicationID},
            response_cls=GetDeletedObjectsToUpdateIndexResponse1,
        )

    @classmethod
    def getImpactedItemRevsForReIndex(cls) -> GetImpactedItemRevsForReIndexResponse:
        """
        The operation queries on scratch, accountability and subscription tables to identify the impacted ItemRevisions
        from last index time due to adds/modify/deletes that took place. These impacted objects need to be re-indexed
        to have the revision rule selectors updated.
        Steps:
        1.    Queries for deleted objects from scratch table. Gets their parent Items from accountability table 
        impacted island if they exist. For the Items found, it fetches all the ItemRevisions and adds them to the
        response.
        2.    Queries for newly added objects from scratch table. Filters out non ItemRevisions from the list. Adds the
        ItemRevisions to the reponse.
        3.    Queries for any Modified islands from the accountability table. If modified island belongs to an
        ItemRevision, then the ItemRevision will be added to the response.
        
        Finally the response will contain the impacted ItemRevisions due to adds/modify/deletes.
        
        
        Use cases:
        Use Case 1: TcFtsIndexer Sync
        
        When data is indexed for the first time the Revision rule slector information is also indexed on each
        ItemRevision. So whenever  a new ItemRevision is added/deleted/modified that impacts all the ItemRevisions
        associated with its parent Item and the revision rule selector information need to be regenerated. This new
        operation will help in identifying the impacted objects and they can be re-indexed to sync the index data .
        """
        return cls.execute_soa_method(
            method_name='getImpactedItemRevsForReIndex',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={},
            response_cls=GetImpactedItemRevsForReIndexResponse,
        )

    @classmethod
    def getObjectsToIndex(cls, objectsToIndexInput: GetTcObjectsToIndexInput) -> GetObjectsToIndexResponse:
        """
        Determine the list of objects to index based on the given date/time range and the "Awp0SearchIsIndexed"
        business object constant.
        """
        return cls.execute_soa_method(
            method_name='getObjectsToIndex',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='FullTextSearch',
            params={'objectsToIndexInput': objectsToIndexInput},
            response_cls=GetObjectsToIndexResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def getTCSessionInfo(cls) -> GetTCSessionInfoResponse:
        """
        This operation gets information about the current user's Teamcenter session.
        """
        return cls.execute_soa_method(
            method_name='getTCSessionInfo',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={},
            response_cls=GetTCSessionInfoResponse,
        )

    @classmethod
    def loadDataForEditing(cls, inputs: List[LoadDataForEditingInfo]) -> LoadDataForEditingResponse:
        """
        This SOA method ensures that the properties can be edited, and returns the last save date of the related
        objects for optimistic edit
        """
        return cls.execute_soa_method(
            method_name='loadDataForEditing',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=LoadDataForEditingResponse,
        )

    @classmethod
    def saveEdit(cls, inputs: List[SaveEditInfo]) -> ServiceData:
        """
        Save the edits on the objects
        """
        return cls.execute_soa_method(
            method_name='saveEdit',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def saveEditAndSubmitToWorkflow(cls, inputs: List[SaveEditAndSubmitInfo]) -> SaveEditAndSubmitResponse:
        """
        This generic operation saves the modified properties for the given input objects and submits them to workflow.
        First it will perform the save operation and if completed successfully, will initiate a workflow process for
        all input objects.
        
        Use cases:
        User can modify the object(s) properties and submit the object(s) to workflow in one operation. This operation
        first saves the modified properties and then initiates the workflow process for all input objects.
        """
        return cls.execute_soa_method(
            method_name='saveEditAndSubmitToWorkflow',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveEditAndSubmitResponse,
        )

    @classmethod
    def updateHistory(cls, historyInput: HistoryInput) -> HistoryResult:
        """
        This operation adds objects to the history and/or removes objects from the history.
        """
        return cls.execute_soa_method(
            method_name='updateHistory',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={'historyInput': historyInput},
            response_cls=HistoryResult,
        )

    @classmethod
    def clearHistory(cls) -> HistoryResult:
        """
        This operation clears the objects in the history and returns the objects that were present in the history.
        """
        return cls.execute_soa_method(
            method_name='clearHistory',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={},
            response_cls=HistoryResult,
        )

    @classmethod
    def getChildren(cls, input: List[BusinessObject]) -> GetChildrenResponse:
        """
        getChildren
        """
        return cls.execute_soa_method(
            method_name='getChildren',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetChildrenResponse,
        )

    @classmethod
    def getCurrentUserGateway(cls) -> GetCurrentUserGatewayResponse:
        """
        The operation looks for the Awp0TileCollection with current logged in user as scope and returns information
        about the Awp0Tile objects associated to it.
        
        Use cases:
        This operation is suited to display the Awp0Tile objects on the Active Workspace client gateway page. The
        Awp0Tiles that are returned by this operation are the ones which are configured for the logged in user based on
        current group, role, and project. 
        
        Display the user specific Awp0Tile objects during startup
        - User logs into Active Workspace.
        - Active Workspace invokes 'getCurrentUserGateway' operation.
        - Displays the Awp0Tile that are configured for the logged in user.
        
        
        
        Display the user specific Awp0Tile objects during context change
        - User changes the group/role/project in Active Workspace.
        - Active Workspace invokes 'getCurrentUserGateway' operation.
        - Displays the Awp0Tile that are configured for the logged in user based on current group, role, and project.
        
        """
        return cls.execute_soa_method(
            method_name='getCurrentUserGateway',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={},
            response_cls=GetCurrentUserGatewayResponse,
        )

    @classmethod
    def getHistory(cls) -> HistoryResult:
        """
        This operation returns the objects in the history.
        """
        return cls.execute_soa_method(
            method_name='getHistory',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='DataManagement',
            params={},
            response_cls=HistoryResult,
        )


class WorkflowService(TcService):

    @classmethod
    def getTaskResults(cls, taskTemplates: List[EPMTaskTemplate]) -> GetTaskResultsResponse:
        """
        Return the task results of a given task template
        """
        return cls.execute_soa_method(
            method_name='getTaskResults',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='Workflow',
            params={'taskTemplates': taskTemplates},
            response_cls=GetTaskResultsResponse,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def setRichContent(cls, inputs: List[SetContentInput]) -> ServiceData:
        """
        This SOA operation sets the body text property of a FullText object to the supplied html or pain text content.
        The SOA operation is called when a user modifies requirements in the active workspace client. It accepts
        SpecElement Revision or FullText objects to process. All modified objects and exceptions are added to the
        returned service data.
        """
        return cls.execute_soa_method(
            method_name='setRichContent',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def exportToApplication(cls, inputs: List[ExportToApplicationInputData]) -> ExportToApplicationResponse:
        """
        exportToApplication
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ExportToApplicationResponse,
        )


class LOVService(TcService):

    @classmethod
    def validateLOVValueSelections(cls, lovInput: LOVInput, propName: str, uidOfSelectedRows: List[str]) -> ValidateLOVValueSelectionsResponse:
        """
        This operation can be invoked after selecting a value from the LOV.  Use this operation to do additional
        validation to be done on server such as validating Range value, getting the dependent properties values in case
        of interdependent LOV (resetting the dependendent property values), Coordinated LOVs ( populating dependent
        property values )
        """
        return cls.execute_soa_method(
            method_name='validateLOVValueSelections',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='LOV',
            params={'lovInput': lovInput, 'propName': propName, 'uidOfSelectedRows': uidOfSelectedRows},
            response_cls=ValidateLOVValueSelectionsResponse,
        )

    @classmethod
    def getInitialLOVValues(cls, initialData: InitialLovData) -> LOVSearchResults:
        """
        This operation is invoked to query the data for a property having an LOV attachment. The results returned from
        the server also take into consideration any filter string that is in the input.  This operation returns both
        LOV meta data as necessary for the client to render the LOV and partial LOV values list as specified.
        
        The operation will return the results in the LOVSearchResults data structure. Maximum number of results to be
        returned are specified in the InitialLOVData data structure. If there are more results, the moreValuesExist
        flag in the LOVSearchResults data structure will be true. If the flag is true, more values can be retrieved
        with a call to the getNextLOVValues operation.
        """
        return cls.execute_soa_method(
            method_name='getInitialLOVValues',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='LOV',
            params={'initialData': initialData},
            response_cls=LOVSearchResults,
        )

    @classmethod
    def getNextLOVValues(cls, lovData: LOVData) -> LOVSearchResults:
        """
        This operation is invoked after a call to getInitialLOVValues if the moreValuesExist flag is true in the
        LOVSearchResults output returned from a call to the getInitialLOVValues operation. The operation will retrieve
        the next set of LOV values
        """
        return cls.execute_soa_method(
            method_name='getNextLOVValues',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='LOV',
            params={'lovData': lovData},
            response_cls=LOVSearchResults,
        )


class FinderService(TcService):

    @classmethod
    def findObjectsByClassAndAttributes2(cls, input: FindObjectsInput2) -> FindObjectsResponse2:
        """
        Returns a list of objects for a specific class type with certain attributes and values.
        """
        return cls.execute_soa_method(
            method_name='findObjectsByClassAndAttributes2',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='Finder',
            params={'input': input},
            response_cls=FindObjectsResponse2,
        )

    @classmethod
    def findUsersTasks(cls) -> FindUsersTasksResponse:
        """
        Finds all the tasks the user has.
        """
        return cls.execute_soa_method(
            method_name='findUsersTasks',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='Finder',
            params={},
            response_cls=FindUsersTasksResponse,
        )


class OrganizationManagementService(TcService):

    @classmethod
    def getGroupMembership(cls, groupMembershipInput: GroupMembershipInput) -> GroupMembershipResponse:
        """
        This operation returns a list of business objects containing group membership information.
        """
        return cls.execute_soa_method(
            method_name='getGroupMembership',
            library='Internal-AWS2',
            service_date='2012_10',
            service_name='OrganizationManagement',
            params={'groupMembershipInput': groupMembershipInput},
            response_cls=GroupMembershipResponse,
        )
