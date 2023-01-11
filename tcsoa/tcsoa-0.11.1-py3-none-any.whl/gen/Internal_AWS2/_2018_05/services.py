from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2018_05.FullTextSearch import Awp0ModifyFTSSavedSearchInput, Awp0CreateFTSSavedSearchInput
from tcsoa.gen.Internal.AWS2._2015_10.FullTextSearch import Awp0FullTextSavedSearchResponse
from tcsoa.gen.Internal.AWS2._2016_03.Finder import ColumnConfigInput, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2018_05.FileMgmt import LoadPlmdTicketReplaceResponse, DatashareManagerReplaceInfo
from tcsoa.gen.Internal.AWS2._2018_05.Finder import FacetSearchInput, SearchResponse5, SearchInput2, FacetSearchResponse
from tcsoa.gen.Internal.AWS2._2018_05.DataManagement import Tile, UnpinObjectsResponse, SaveViewModelEditAndSubmitResponse2, GetCurrentUserGateway2Response, UpdateTilesResponse, PinObjectInput
from tcsoa.gen.Internal.AWS2._2018_05.TCXML import GetDiagnosticInfoForAcctTablesResp
from tcsoa.gen.BusinessObjects import Item, WorkspaceObject
from typing import List
from tcsoa.gen.Internal.AWS2._2017_06.DataManagement import SaveViewModelEditAndSubmitInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Internal.AWS2._2018_05.Workflow import WorkflowTaskViewModelInput, WorkflowTaskViewModelResponse


class GlobalAlternateService(TcService):

    @classmethod
    def addAlternates(cls, element: WorkspaceObject, alternatesToBeAdded: List[WorkspaceObject]) -> ServiceData:
        """
        Adds objects as alternates to the selected object. Alternates components are parts that are interchangeable
        globally.
        
        Use cases:
        In order to add one or more alternates to the selected object, the user can call addAlternates operation and
        pass in the selected object and a list of business objects to be defined as alternates of the selected object.
        """
        return cls.execute_soa_method(
            method_name='addAlternates',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='GlobalAlternate',
            params={'element': element, 'alternatesToBeAdded': alternatesToBeAdded},
            response_cls=ServiceData,
        )

    @classmethod
    def removeAlternates(cls, element: WorkspaceObject, alternatesToBeRemoved: List[Item]) -> ServiceData:
        """
        Removes alternates from the selected object.
        
        Use cases:
        In order to remove one or more alternates from the selected object, the user can call removeAlternates
        operation and pass in the selected object and a list of alternates to be removed.
        """
        return cls.execute_soa_method(
            method_name='removeAlternates',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='GlobalAlternate',
            params={'element': element, 'alternatesToBeRemoved': alternatesToBeRemoved},
            response_cls=ServiceData,
        )


class WorkflowService(TcService):

    @classmethod
    def getWorkflowTaskViewModel(cls, input: List[WorkflowTaskViewModelInput]) -> WorkflowTaskViewModelResponse:
        """
        Operation to get the properties on EPMTask and Signoff objects in JSON format.  It can also be used to traverse
        the reference properties on EPMTask and Signoff and get properties on the referenced objects.  The output JSON
        is designed to be consumed by the active workspace client panels.  The information needed to be displayed in
        the panels can be obtained by properly constructing the input structure.
        
        Use cases:
        In Active Workspace, Select-Signoff-Task perform panel needs to show the following data:
        - Required Profiles with the count of unstaffed profiles
        - Profile signoffs
        - Adhoc signoffs
        - Quorum data
        
        
        This SOA is designed to get all the above data .  It can also return a logical flag(s) to indicate if the task
        can be completed or not based on which complete button can be displayed in the dialog.This will avoid
        unnecessory complex logic on the client to segregate data( like profiles, profile signoffs and adhoc signoff)
        to display in the panel and to detemine current quorum based on exisiting signoffs etc.
        """
        return cls.execute_soa_method(
            method_name='getWorkflowTaskViewModel',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='Workflow',
            params={'input': input},
            response_cls=WorkflowTaskViewModelResponse,
        )


class TCXMLService(TcService):

    @classmethod
    def installDBTriggersForDataSync(cls, triggerType: int) -> ServiceData:
        """
        Installs Database triggers on POM_object table for tracking newly added objects and (or) deleted objects that
        are used for data synchronization purpose.
        
        Use cases:
        Data indexing uses TCXML as the payload for extracting data from Database. In order to support data
        synchronization, data indexing needs to install Database triggers to track newly added objects and deleted
        objects as the first step of indexing.
        """
        return cls.execute_soa_method(
            method_name='installDBTriggersForDataSync',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='TCXML',
            params={'triggerType': triggerType},
            response_cls=ServiceData,
        )

    @classmethod
    def removeDBTriggersForDataSync(cls, triggerType: int) -> ServiceData:
        """
        Removes the Database triggers on POM_object table for tracking newly added objects and (or) deleted objects
        that are used for data synchronization purpose.
        
        Use cases:
        Data indexing uses TCXML as the payload for extracting data from Database. In order to support data
        synchronization, data indexing needs to install Database triggers to track newly added objects and deleted
        objects as the first step of indexing. This operatoin is a mirror operation to remove the Database triggers
        that were installed by installDBTriggersForDataSync operation.
        """
        return cls.execute_soa_method(
            method_name='removeDBTriggersForDataSync',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='TCXML',
            params={'triggerType': triggerType},
            response_cls=ServiceData,
        )

    @classmethod
    def getDiagnosticInfoForAcctTables(cls, infoType: int) -> GetDiagnosticInfoForAcctTablesResp:
        """
        Returns the accountability tables' and the related POM tables' diagnostic information. The accountability
        tables are used for recording exported data and statuses, as well as data synchronization status and candidates.
        
        Use cases:
        Data indexing uses the operation to retrieve the accountability tables' diagnostic information and reports the
        information to end user. As an environment health check, this helps to understand the underlying tables status
        and diagnose any failure or performance problems.
        """
        return cls.execute_soa_method(
            method_name='getDiagnosticInfoForAcctTables',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='TCXML',
            params={'infoType': infoType},
            response_cls=GetDiagnosticInfoForAcctTablesResp,
        )


class FileMgmtService(TcService):

    @classmethod
    def loadPlmdTicketForReplace(cls, infos: List[DatashareManagerReplaceInfo]) -> LoadPlmdTicketReplaceResponse:
        """
        This operation assists in an asynchronous file replace using the Datashare Manager. When a single file is being
        replaced, the PLMD (Product Lifecycle Management Data) file is downloaded to the Transient volume and the file
        ticket returned. In the case of multiple files being replaced, the output structure is populated with
        additional informaton needed for the Replace operation.
        """
        return cls.execute_soa_method(
            method_name='loadPlmdTicketForReplace',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='FileMgmt',
            params={'infos': infos},
            response_cls=LoadPlmdTicketReplaceResponse,
        )


class FullTextSearchService(TcService):

    @classmethod
    def modifyFullTextSavedSearch(cls, inputs: List[Awp0ModifyFTSSavedSearchInput]) -> Awp0FullTextSavedSearchResponse:
        """
        This operation modifies existing Awp0FullTextSavedSearch objects.
        """
        return cls.execute_soa_method(
            method_name='modifyFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=Awp0FullTextSavedSearchResponse,
        )

    @classmethod
    def createFullTextSavedSearch(cls, inputs: List[Awp0CreateFTSSavedSearchInput]) -> Awp0FullTextSavedSearchResponse:
        """
        This operation creates Awp0FullTextSavedSearch objects. Awp0FullTextSavedSearch objects are used to store
        information about a saved search such as search name, search string, search filters, chart input parameters etc.
        """
        return cls.execute_soa_method(
            method_name='createFullTextSavedSearch',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=Awp0FullTextSavedSearchResponse,
        )


class FinderService(TcService):

    @classmethod
    def performFacetSearch(cls, facetSearchInput: FacetSearchInput) -> FacetSearchResponse:
        """
        This operation fetches facet values in a paged fashion for a selected filter category. It also supports search
        on facet values to get matching facet values for a given text input.
        
        Use cases:
        Use Case 1: User clicks on unpopulated filter category
        Only 200 classification filters are populated and available at the client. To get facet values for an
        unpopulated filter, a search request will be made by passing in the needed criteria. It queries for the facet
        values and returns to the client. The number of values to be returned is controlled by the input parameter
        maxToReturn.
        
        Use Case 2: User performs search for filter values by entering text in filter category search input box. 
        If user types in a value in the filter box, a search request will be made by passing in the needed criteria.
        The input text will be passed into &lsquo;stringValue&rsquo; parameter of the input searchFilterMap. It queries
        for the data and finds the facet values matching the input text. These facet values are included in the
        searchFilterMap of the response. 
        
        Use Case 3: User clicks on "More" to get next set of facet values
        If &lsquo;hasMoreFacetValues&rsquo; flag of the FacetSearchResponse is true, the client will make a search
        request for facet values. Facet values will be queried and returned based on the input criteria.
        """
        return cls.execute_soa_method(
            method_name='performFacetSearch',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='Finder',
            params={'facetSearchInput': facetSearchInput},
            response_cls=FacetSearchResponse,
        )

    @classmethod
    def performSearchViewModel3(cls, searchInput: SearchInput2, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData, inflateProperties: bool, noServiceData: bool) -> SearchResponse5:
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
            method_name='performSearchViewModel3',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData, 'inflateProperties': inflateProperties, 'noServiceData': noServiceData},
            response_cls=SearchResponse5,
        )


class DataManagementService(TcService):

    @classmethod
    def pinObjects(cls, input: List[PinObjectInput]) -> ServiceData:
        """
        This operation pins the objects represented by the input objects to the user&rsquo;s Gateway.
        
        Use cases:
        Pin an Object while not in the Gateway
        1. User logs into Active Workspace.
        2. User selects a previouslycreated BusinessObject object.
        3. User chooses the "pin" command.
        4. ActiveWorkspace invokes the pinObject service operation, providing the UID of the BusinessObject object to
        pin, along with any optional template ID or parameter information in the list of PinObjectInput structures.
        """
        return cls.execute_soa_method(
            method_name='pinObjects',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def saveViewModelEditAndSubmitWorkflow2(cls, inputs: List[SaveViewModelEditAndSubmitInfo]) -> SaveViewModelEditAndSubmitResponse2:
        """
        This operation saves the modified view model properties for the given input objects and submits the objects to
        a workflow. The workflow is submitted only if all of the save operations are successful. If the save fails for
        a single object  none of the input objects will be submitted to a workflow. This operation saves the
        ViewModelObject and supports dynamic compound properties.
        
        Use cases:
        User can modify the object(s) properties and submit the object(s) to workflow in one operation. This operation
        first saves the modified properties and then initiates the workflow process for all input objects.
        """
        return cls.execute_soa_method(
            method_name='saveViewModelEditAndSubmitWorkflow2',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveViewModelEditAndSubmitResponse2,
        )

    @classmethod
    def unpinObjects(cls, returnGateway: bool, uidsToUnpin: List[str]) -> UnpinObjectsResponse:
        """
        This operation unpins the objects represented by the input list of UIDs from the user&rsquo;s Gateway.
        
        Use cases:
        This operation is suited to update the Tile objects on the Active Workspace client gateway page.
        
        Unpin an Object while not in the Gateway
        1. User logs into Active Workspace.
        2. User selects a previously pinned BusinessObject object and chooses the "unpin" command.
        3. Active Workspace invokes unpinObjects operation.
        4. Using the unpinObjects&rsquo; response, Active Workspace displays the updated group of Tile objects that are
        configured for the logged in user.
        
        Unpin a user specific Awp0TileObject
        1. User logs into Active Workspace.
        2. Active Workspace invokes getCurrentUserGateway2 operation.
        3. Displays the groups of Tile objects that are configured for the logged in user.
        4. User selects a Tile object and chooses the "unpin" command.
        5. Active Workspace invokes unpinObjects operation.
        6. Using the unpinObjects&rsquo; response, Active Workspace displays the updated group of Tile objects that are
        configured for the logged in user.
        """
        return cls.execute_soa_method(
            method_name='unpinObjects',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='DataManagement',
            params={'returnGateway': returnGateway, 'uidsToUnpin': uidsToUnpin},
            response_cls=UnpinObjectsResponse,
        )

    @classmethod
    def updateTiles(cls, tiles: List[Tile], groupNames: List[str]) -> UpdateTilesResponse:
        """
        This operation updates the input list of Tile objects from the user&rsquo;s Gateway.  This includes moving Tile
        objects from one group to another, as well as updating properties on Tile objects such as the size and ordering
        of Tile objects.
        
        Use cases:
        This operation is suited to update the Tile objects on the Active Workspace client gateway page.
        
        Update the user specific Awp0Tile objects.
        1. User logs into Active Workspace.
        2. Active Workspace invokes getCurrentUserGateway2 operation.
        3. Displays the groups of Tile objects that are configured for the logged in user.
        4. User selects a Tile object and updates the Tile&rsquo;s size, order, and group.
        5. Active Workspace invokes updateTiles operation.
        6. Using the updateTiles&rsquo; response, Active Workspace displays the updated group of Tile objects that are
        configured for the logged in user.
        """
        return cls.execute_soa_method(
            method_name='updateTiles',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='DataManagement',
            params={'tiles': tiles, 'groupNames': groupNames},
            response_cls=UpdateTilesResponse,
        )

    @classmethod
    def getCurrentUserGateway2(cls) -> GetCurrentUserGateway2Response:
        """
        The operation looks for the Awp0TileCollection with current logged in user as scope and returns information
        about the Awp0Tile objects associated to it.
        
        Use cases:
        This operation is suited to display the Awp0Tile objects on the Active Workspace client gateway page. The Tile
        objects that are returned by this operation are the ones which are configured for the logged in user based on
        current group, role, and project.
        
        Display the user specific Awp0Tile objects during startup
        1. User logs into Active Workspace.
        2. Active Workspace invokes getCurrentUserGateway2 operation.
        3. Displays the groups of Tile objects that are configured for the logged in user.
        
        Display the user specific Awp0Tile objects during context change
        1.  User changes the group/role/project in Active Workspace.
        2.  Active Workspace invokes getCurrentUserGateway2 operation.
        3.  Displays the groups of Tile objects that are configured for the logged in user based on current group,
        role, and project.
        """
        return cls.execute_soa_method(
            method_name='getCurrentUserGateway2',
            library='Internal-AWS2',
            service_date='2018_05',
            service_name='DataManagement',
            params={},
            response_cls=GetCurrentUserGateway2Response,
        )
