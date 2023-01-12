from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2016_03.Finder import GetClassificationPropsResponse, SearchResponse, SaveColumnConfigData, SearchInput, ColumnConfigInput
from tcsoa.gen.Internal.AWS2._2016_03.DataManagement import GetUnprocessedXRTResponse, GetStyleSheetResponse, DSInfo
from tcsoa.gen.Internal.AWS2._2016_03.RequirementsManagement import ExportToApplicationInputData2, ExportToApplicationResponse2
from tcsoa.gen.Internal.AWS2._2016_03.UiConfig import GetVisibleCommandsResponse, SaveColumnConfigData, GetVisibleCommandsInfo, GetOrResetUIColumnConfigInput, GetOrResetUIColumnConfigResponse
from tcsoa.gen.Internal.AWS2._2016_04.DataManagement import GetStyleSheetIn
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class UiConfigService(TcService):

    @classmethod
    def getOrResetUIColumnConfigs(cls, getOrResetUiConfigsIn: List[GetOrResetUIColumnConfigInput]) -> GetOrResetUIColumnConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes column configuration information. 
        If the resetColumnConfig flag is "True", this operation deletes the column configuration of the input scope and
        then queries the new effective UI column configuration for the login user. This operation will only clear the
        login user column configurations.
        
        Use cases:
        Request UI Configuration(s) based on the current login user
        Client requests the column  information for one or more client scopes using this operation and scope as login
        user.
        
        Request UI Configuration(s) based on a specific Teamcenter scope
        Client requests the column information for one or more client scopes using this operation and scope as Role,
        Site or Group.
        
        Request to reset UI Column Configuration(s) based on the current login user
        If a client needs to reset the column information for login user scope, they can use this operation. The new
        effective UI column configuration will be retrieved for the login user.
        """
        return cls.execute_soa_method(
            method_name='getOrResetUIColumnConfigs',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='UiConfig',
            params={'getOrResetUiConfigsIn': getOrResetUiConfigsIn},
            response_cls=GetOrResetUIColumnConfigResponse,
        )

    @classmethod
    def getVisibleCommands(cls, getVisibleCommandsInfo: List[GetVisibleCommandsInfo]) -> GetVisibleCommandsResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes commands that are visible.
        """
        return cls.execute_soa_method(
            method_name='getVisibleCommands',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='UiConfig',
            params={'getVisibleCommandsInfo': getVisibleCommandsInfo},
            response_cls=GetVisibleCommandsResponse,
        )

    @classmethod
    def saveUIColumnConfigs(cls, columnConfigurations: List[SaveColumnConfigData]) -> ServiceData:
        """
        This service operation saves column configuration information to the Teamcenter database. A Teamcenter client
        may use this information to render the user interface as the user navigates the Teamcenter client. Default
        column configurations are initally created by an utility during install. This operation will modify the default
        column configuration for the site, group, role or a specific user.
        
        Use cases:
        User level column configuration:
        A User wants to change the default column configuration for a Client Scope when he is logged into the client.
        The saved configuration will override the default configuration for the user's applicable role, group or site.
        """
        return cls.execute_soa_method(
            method_name='saveUIColumnConfigs',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='UiConfig',
            params={'columnConfigurations': columnConfigurations},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getStyleSheet2(cls, processEntireXRT: bool, input: List[GetStyleSheetIn]) -> GetStyleSheetResponse:
        """
        This operation returns the stylesheets and the required data to present that stylesheet for each input object.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getStylesheet call is invoked and the Stylesheet is processed in order to display the
        data to the user.
        
        Use Case 2: List view with Summary
        When an object is selected in the ActiveWorkspace navigator, when in list view with summary mode, the
        getStyleSheet SOA operation is invoked, and the returned data is parsed/processed in order to present the data
        to the user in the Summary panel.
        
        Use Case 3: Show Object Info
        When an object is selected in ActiveWorkspace, a user may choose the "Show Object Info" command.  When
        executed, a panel slides out from the right hand side of the application, and the selected objects data is
        presented.  In order to populate the panel, the getStylesheet call is invoked and the returned data is parsed
        and processed in order to build the UI.
        """
        return cls.execute_soa_method(
            method_name='getStyleSheet2',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='DataManagement',
            params={'processEntireXRT': processEntireXRT, 'input': input},
            response_cls=GetStyleSheetResponse,
        )

    @classmethod
    def getUnprocessedXRT(cls, client: str, type: str, location: str, sublocation: str, stylesheetType: str, preferenceLocation: str) -> GetUnprocessedXRTResponse:
        """
        This operation returns the unprocessed XRT stylesheet.
        
        Use cases:
        XRT administration using the internal client "xrtFiddle".
        """
        return cls.execute_soa_method(
            method_name='getUnprocessedXRT',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='DataManagement',
            params={'client': client, 'type': type, 'location': location, 'sublocation': sublocation, 'stylesheetType': stylesheetType, 'preferenceLocation': preferenceLocation},
            response_cls=GetUnprocessedXRTResponse,
        )

    @classmethod
    def saveXRT(cls, dsInfo: DSInfo) -> ServiceData:
        """
        Saves an XRT definition to the specified context.   In this version, saving of injected datasets is not
        supported.
        
        Use cases:
        Save an XRT from the internal client called xrtFiddle.
        """
        return cls.execute_soa_method(
            method_name='saveXRT',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='DataManagement',
            params={'dsInfo': dsInfo},
            response_cls=ServiceData,
        )


class FinderService(TcService):

    @classmethod
    def performSearch(cls, searchInput: SearchInput, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData) -> SearchResponse:
        """
        This operation routes a search request to a specific provider specified as providerName in the searchInput
        structures
        
        The framework allows a custom solution to be able to provide a new specific provider to collect data, perform
        sorting and filtering. The provider can be a User Inbox retriever or Full Text searcher, for example. The new
        data provider can be encapsulated via a new runtime business object from Fnd0BaseProvider class. The
        implementation is done using its fnd0performSearch operation.
        
        RuntimeBusinessObject
        ---- Fnd0BaseProvider (foundation template)
        -------- Fnd0GetChildrenProvider (foundation template)
        -------- Awp0FullTextSearchProvider (aws template)
        -------- Awp0TaskSearchProvider (aws template)
        -------- Aos0TestProvider (aosinternal template)
        -------- etc.
        This operation provides a common interface to send the request to and receive the response from a new data
        provider. Ultimately it allows common framework in UI to support filter, pagination, and sorting.
        
        This operation allows the caller to send the search input, filter values, and sorting data. These input values
        are then to be passed to the fnd0performSearch operation on the server to collect, sort, and filter its results.
        
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
        search results and the operation type( Union / Intersection / Configured ) configured for the client scope URI.
        Finally the determined column attributes and the attributes to be inflated passed in as part of search input
        criteria are combined. This combined list of attributes along with the business objects found during search are
        added to the Service data.
        
        Use cases:
        Use Case 1: User clicks on Inbox tile
        A search request will be made by passing in the needed criteria. In this case the the provider name is
        "Awp0InboxProvider". It queries for the data and finds the effective columns for the client scope URI passed in
        through column config input. The results are finally shown in the view type selected in client. If table view
        is selected the returned effective columns will be shown.
        
        Use Case 2: User performs search by entering a keyword in global search input box.
        A search request will be made by passing in the needed criteria that includes the keyword user has typed in. In
        this case the the provider name is "Awp0FullTextSearchProvider". It queries for the data and finds the
        effective columns for the client scope URI passed in through column config input. The results are finally shown
        in the view type selected in client. If table view is selected the returned effective columns will be shown.
        
        Use Case 3: User tries to save new column configuartions after performing search.
        The new list of column configurations will be saved for the login user scope. Later the search request will be
        made by passing in the needed criteria that includes the keyword user had typed in. In this case the the
        provider name is "Awp0FullTextSearchProvider". It queries for the data and finds the effective columns for the
        client scope URI passed in through column config input. The results are finally shown in the view type selected
        in client. If table view is selected the returned effective columns will be shown.
        """
        return cls.execute_soa_method(
            method_name='performSearch',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData},
            response_cls=SearchResponse,
        )

    @classmethod
    def getClassificationProps(cls, objects: List[WorkspaceObject], showAllProperties: bool) -> GetClassificationPropsResponse:
        """
        This operation provides classification properties for a given WorkspaceObject(s).
        
        Use cases:
        User wants to find classification properties for WorkspaceObjects. Each time a WorkspaceObject is classified in
        a classification class a classification object (icm0) is created. After searching for all the classification
        objects corresponding to a workspace object, user can find more information about the classification(s) of a
        workspace object. The operation getClassificationProps() can be used to get detailed information about the
        classification objects.
        """
        return cls.execute_soa_method(
            method_name='getClassificationProps',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='Finder',
            params={'objects': objects, 'showAllProperties': showAllProperties},
            response_cls=GetClassificationPropsResponse,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def exportToApplication(cls, input: List[ExportToApplicationInputData2]) -> ExportToApplicationResponse2:
        """
        This operation will exports the selected occurrences in the structure to the application such as MSWord and
        MSExcel. The behavior of export operation is controlled by applicationFormat argument specified in
        ExportToApplicationInput2 structure.
        Following are supported application formats from input.
        
        - MSExcelLive - This mode provides the capability of editing of properties of  underlying ItemRevision  in
        MSExcel and save the changes to Teamcenter. The generated sheet allows user to login and change the properties
        from MSExcel application. The changes will be saved to Teamcenter when user exits out of the cell in MSExcel
        application.  Teamcenter extensions for Microsoft Office should be installed on the client machine to support
        this application format.
        - MSWordXMLLive - This mode provides the capability of structural editing of SpecElementRevisions in MSWord.
        Users can edit the rich text of Requirement and perform structural changes to the exported Requirement(s) in
        the word document. Office Client should be installed on the client machine to support this application format.
        - MSExcel - This mode provides the capability of exporting objects to static MSExcel application. 
        - MSExcelReimport- This mode provides the capability of exporting objects to MSExcel application for reimport
        purpose. The generated sheet can be used to for add/remove structure elements or to update the properties on
        the SpecElement revision. The generated sheet should be reimported back to  Teamcenter. Office Client should be
        installed on the client machine to support this application format.
        - MSWordCompare - This mode provides the capability of comparing the contents of source and target objects
        using MSWord application.  The comparison document is generated asynchonously in the background and user is
        notified when the comparison document is generated. Dispatcher and notification services should be running to
        support this application format.
        - HTML- This mode provides the capability of fetching the HTML contents  of input SpecElement objects.
        
        
        
        Use cases:
        - User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure. User selects an occurrence and clicks on the Export To Word or Export to Excel
        button in the toolbar. This action will allow users to select a template that will be used for export purpose.
        If user has selected a single occurrence and clicks on export, then the occurrence and all its children are
        exported to MSWord or MSExcel. If user has selected multiple occurrences and clicks on export, then the
        selected occurrences are exported to MSWord or MSExcel.
        - User selects single or multiple objects in Active Workspace Client. User clicks on the Export to Excel button
        in the toolbar. User can select View, Edit or Reimport option. Depending upon the option selected, a static
        MSExcel report or a Live MSExcel sheet or a sheet is generated that can be reimported back to Teamcenter. 
        - User select s single or multiple objects in Active Workspace Client and sets them as source objects to
        compare. Similarly user selects single or multiple target objects to compare. User clicks on the Export to Word
        button in the toolbar along with the checkbox for compare contents. User selects the compare contents checkbox
        that allows user to compare the MSWord contents of source and target objects. User is notified when the
        comparison document is generated and attached to a dataset.
        - User selects a SpecElement created from Active Workspace client and clicks on the Viewer tab. The HTML
        contents of the selected SpecElement is shown in the Viewer tab.
        
        """
        return cls.execute_soa_method(
            method_name='exportToApplication',
            library='Internal-AWS2',
            service_date='2016_03',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=ExportToApplicationResponse2,
        )
