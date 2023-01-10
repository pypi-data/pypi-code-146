from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchInput, ColumnConfigInput, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2017_12.DataManagement import GetTableViewModelPropertiesIn, StringMap8, LoadViewModelForEditing2Response, GetViewModelProps2Response, TCSessionAndAnalyticsInfo, FilterParams, GetTableViewModelPropsResp, GetAvailableWorkspacesResponse
from tcsoa.gen.Internal.AWS2._2017_12.FullTextSearch import QueryAndUpdateSyncDataResponse, GetIndexedObjectsAndUpdateResponse, QueryAndUpdateDataInput
from typing import List
from tcsoa.gen.Internal.AWS2._2017_06.DataManagement import LoadViewModelForEditingInfo
from tcsoa.gen.Internal.AWS2._2017_12.Finder import SearchResponse4
from tcsoa.base import TcService
from datetime import datetime


class DataManagementService(TcService):

    @classmethod
    def getTCSessionAnalyticsInfo(cls, extraInfo: List[str]) -> TCSessionAndAnalyticsInfo:
        """
        This operation provides information about the current user's Teamcenter session and data required for
        Teamcenter Software Analytics processing.
        
        Use cases:
        Use Case 1: After the user logs into Active Workspace this operation is invoked by the Active Workspace client
        to get information related to the user session like Groups, Projects, the Teamcenter Server version, platform
        type,License type, preference related to the time interval and product excellence agreement as required by
        analytics.
        """
        return cls.execute_soa_method(
            method_name='getTCSessionAnalyticsInfo',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='DataManagement',
            params={'extraInfo': extraInfo},
            response_cls=TCSessionAndAnalyticsInfo,
        )

    @classmethod
    def getTableViewModelProperties(cls, input: GetTableViewModelPropertiesIn) -> GetTableViewModelPropsResp:
        """
        The operation returns the column configuration and Table View Model properties for the input object UIDs.
        
        Use cases:
        Usecase 1: When the user opens a structure in the content tab and switch to table mode. The column
        configuration and related properties need to be fetched.
        
        Usecase 2: When a structure is opened in the tree mode. The column configuration and related properties need to
        be fetched.
        """
        return cls.execute_soa_method(
            method_name='getTableViewModelProperties',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetTableViewModelPropsResp,
        )

    @classmethod
    def getViewModelProperties2(cls, objects: List[BusinessObject], attributes: List[str], configs: StringMap8) -> GetViewModelProps2Response:
        """
        This service operation is provided to get property values of instances outside of the current object property
        policy for a particular business object. This operation is an enhanced version of the getProperties service
        operation and allows for retrieving values of dynamic compound properties as well.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getViewModelProperties call is executed to fetch required properties.
        """
        return cls.execute_soa_method(
            method_name='getViewModelProperties2',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='DataManagement',
            params={'objects': objects, 'attributes': attributes, 'configs': configs},
            response_cls=GetViewModelProps2Response,
        )

    @classmethod
    def loadViewModelForEditing2(cls, inputs: List[LoadViewModelForEditingInfo]) -> LoadViewModelForEditing2Response:
        """
        This method ensures that the properties can be edited and returns the last save date of the related objects for
        optimistic edit. This new operation is similar to the existing loadDataForEditing operation, the difference is
        that this SOA saves the ViewModelObject instead of model object, and this SOA supports dynamic compound
        properties. In addition to checking if the object and the properties are modifiable, if the property is dynamic
        compound property, this SOA also validates if the traversal path of the dynamic compound property is same as
        when properties was queries from server during display, if it is, then editing is not allowed.
        loadViewModelForEditing operation will be deprecated.
        """
        return cls.execute_soa_method(
            method_name='loadViewModelForEditing2',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=LoadViewModelForEditing2Response,
        )

    @classmethod
    def getAvailableWorkspaces(cls, filterParams: FilterParams) -> GetAvailableWorkspacesResponse:
        """
        This operation returns available workspaces. The list of workspaces is populated based on input criteria (e.g.
        current user session ).
        
        Use cases:
        Use Case 1: Click on the current workspace user is working in. 
        In Active Workspace, when user clicks on the header context link (which shows current workspace) the
        getAvailableWorkspaces operation will be called. The client will show a list of available workspaces to the
        user to choose a value from. 
        
        Use Case 2: Show list of all workspaces in primary workarea.
        In ActiveWorkspace, when user navigates to "workspaces" sublocation, primary work-area needs to display all the
        workspaces in the system. In order to populate the primary workarea, the getAvailableWorkspaces call is
        invoked. The returned data is parsed and processed in order to display list of all workspaces into the system.
        """
        return cls.execute_soa_method(
            method_name='getAvailableWorkspaces',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='DataManagement',
            params={'filterParams': filterParams},
            response_cls=GetAvailableWorkspacesResponse,
        )


class FinderService(TcService):

    @classmethod
    def performSearchViewModel2(cls, searchInput: SearchInput, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData, inflateProperties: bool) -> SearchResponse4:
        """
        This operation routes a search request to a specific provider specified as providerName in the searchInput
        structures.
        
        The framework allows a custom solution to be able to provide a new specific provider to collect data, perform
        sorting and filtering. The provider can be a User Inbox retriever or Full Text searcher, for example. The new
        data provider can be encapsulated via a new runtime business object from Fnd0BaseProvider class. The
        implementation is done using its fnd0performSearch operation.
        
        RuntimeBusinessObject 
        ---- Fnd0BaseProvider (foundation template) 
        -------- Fnd0GetChildrenProvider(foundation template) 
        -------- Awp0FullTextSearchProvider (aws template)
        -------- Awp0TaskSearchProvider (aws template) 
        -------- Aos0TestProvider (aosinternal template) 
        -------- etc.
        
        This operation provides a common interface to send the request to and receive the response from a new data
        provider. Ultimately it allows common framework in UI to support filter, pagination, and sorting. 
        
        This operation allows the caller to send the search input, filter values, and sorting data. These input values
        are then to be passed to the fnd0performSearch operation on the server to collect, sort, and filter its
        results. 
        
        The first two input parameters are important. The first input is the provider name. This is a string to
        represent the type name of RuntimeBusinessObject which this request should be routed to. If the template that
        contains the class is not installed, a partial error 217016 is returned. The second input is the search input
        map. The key is different per each provider. For example, for Full Text searcher, the input key would be a
        searchString. For User Inbox retriever, the input key would be an Inbox Type. The fnd0performSearch
        implementation for each provider takes into account the key name as it is used to store the values in
        OperationInput object. 
        
        The internal property name is passed as part of search input to allow grouping of business objects. The
        grouping allows for added functionality such as color coding, etc. If no internal property name is passed,
        default value is assumed as "object_type" to group the business objects. 
        
        If new list of column config data is passed in to be saved, it will get saved in the database for the login
        user scope. This will be done prior to performing the search. 
        
        The column configuration input has the criteria needed to query for the columns configured for the provided
        client and client scope URI. The final list of columns are identified based on the types returned back in the
        search results and the operation type (Union / Intersection / Configured ) configured for the client scope URI.
        Finally the determined column attributes and the attributes to be inflated passed in as part of search input
        criteria are combined. This combined list of attributes along with the business objects found during search are
        added to the Service data.
        
        Use cases:
        Use Case 1: User clicks on Inbox tile
        A search request will be made by passing in the needed criteria. In this case the provider name is
        "Awp0InboxProvider". It queries for the data and finds the effective columns for the client scope URI passed in
        through column config input. The results are finally shown in the view type selected in client. If table view
        is selected the returned effective columns will be shown.
        
        Use Case 2: User performs search by entering a keyword in global search input box. 
        A search request will be made by passing in the needed criteria that includes the keyword user has typed in. In
        this case the provider name is "Awp0FullTextSearchProvider". It queries for the data and finds the effective
        columns for the client scope URI passed in through column config input. The results are finally shown in the
        view type selected in client. If table view is selected the returned effective columns will be shown. 
        
        Use Case 3: User tries to save new column configurations after performing search. 
        The new list of column configurations will be saved for the login user scope. Later the search request will be
        made by passing in the needed criteria that includes the keyword user had typed in. In this case the provider
        name is "Awp0FullTextSearchProvider". It queries for the data and finds the effective columns for the client
        scope URI passed in through column config input. The results are finally shown in the view type selected in
        client. If table view is selected the returned effective columns will be shown.
        
        ---
        """
        return cls.execute_soa_method(
            method_name='performSearchViewModel2',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData, 'inflateProperties': inflateProperties},
            response_cls=SearchResponse4,
        )


class FullTextSearchService(TcService):

    @classmethod
    def queryAndUpdateSyncData(cls, inputData: QueryAndUpdateDataInput) -> QueryAndUpdateSyncDataResponse:
        """
        This service operation queries for the data to be synced and updates the state of those records in ACCT_TABLE. 
        The Full Text Search Indexer which indexes Teamcenter data uses the information for further processing.
        
        Queries for deleted objects that have been previously indexed after previous sync.
        Updates these records in ACCT_TABLE with DELETE_PENDING state
        Updates the :FTS_DEL_QRY app_id timetsamp in SUBSCRIPTION_TABLE
        
        Queries for newly added objects after previous sync.
        Inserts these records into ACCT_TABLE with ADD_MODIFY_PENDING state.
        Updates the timestamp of the :FTS_ADD_QRY app_id in SUBSCRIPTION_TABLE
        
        Queries for modifications via relations of indexed objects
        Updates these records in ACCT_TABLE with MODIFY_REL_PENDING state.
        Queries for modifications of indexed objects.
        Updates these records in ACCT_TABLE with ADD_MODIFY_PENDING state
        Updates the timestamp of the :FTS_SYNC app_id in SUBSCRIPTION_TABLE
        
        The count of added or deleted or modified objects found by queries will be returned back through SyncInfo map.
        Any errors during queries or update of records will be reported as partial errors through ServiceData object.
        """
        return cls.execute_soa_method(
            method_name='queryAndUpdateSyncData',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='FullTextSearch',
            params={'inputData': inputData},
            response_cls=QueryAndUpdateSyncDataResponse,
        )

    @classmethod
    def getIndexedObjectsAndUpdate(cls, applicationID: str, subscriptionAppID: str, exportedDate: datetime, statuses: List[int], classNames: List[str], maxObjectCount: int, statusToUpdate: int) -> GetIndexedObjectsAndUpdateResponse:
        """
        This operation queries for the indexed objects matching the given input criteria. Criteria include application
        ID, timestamp, list of export or import statuses of the object and list of object class names. The
        maxCountObject can be specified to limit the count of matching object UIDs to be fetched by the query.  The
        statusToUpdate will be used to update the records of the UIDs fetched by the query in ACCT_TABLE.
        """
        return cls.execute_soa_method(
            method_name='getIndexedObjectsAndUpdate',
            library='Internal-AWS2',
            service_date='2017_12',
            service_name='FullTextSearch',
            params={'applicationID': applicationID, 'subscriptionAppID': subscriptionAppID, 'exportedDate': exportedDate, 'statuses': statuses, 'classNames': classNames, 'maxObjectCount': maxObjectCount, 'statusToUpdate': statusToUpdate},
            response_cls=GetIndexedObjectsAndUpdateResponse,
        )
