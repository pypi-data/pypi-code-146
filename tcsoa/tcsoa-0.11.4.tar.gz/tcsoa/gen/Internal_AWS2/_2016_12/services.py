from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2016_12.AdvancedSearch import AdvancedSearchResponse, AdvancedQueryCriteriaResponse
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchInput, ColumnConfigInput, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2016_12.RequirementsManagement import ExportInputDataAsync, ExportToApplicationInputData3, SetContentInput2
from tcsoa.gen.Internal.AWS2._2016_03.RequirementsManagement import ExportToApplicationResponse2
from tcsoa.gen.Internal.AWS2._2016_12.DataManagement import GetDeclarativeStyleSheetResponse, SaveEditAndSubmitInfo, GetDefaultRelationResponse, GetDefaultRelationIn
from tcsoa.gen.Internal.AWS2._2016_04.DataManagement import GetStyleSheetIn
from tcsoa.gen.BusinessObjects import ImanQuery
from typing import List
from tcsoa.gen.Internal.AWS2._2012_10.DataManagement import SaveEditAndSubmitResponse
from tcsoa.gen.Internal.AWS2._2016_12.Finder import SearchResponse2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AdvancedSearchService(TcService):

    @classmethod
    def getSelectedQueryCriteria(cls, selectedQuery: ImanQuery) -> AdvancedQueryCriteriaResponse:
        """
        Creates the Advanced Query Criteria business object (Awp0AdvancedQueryCriteria). This object is used to
        populate criteria for currently selected Saved Query. The Query Criteria are represented by dynamic runtime
        business objects. This is necessary because the query criteria fields change deepending on which Saved Query is
        selected by the user. Advanced Query Criteria is the parent business object of the dynamic runtime business
        objects.
        
        Use cases:
        Advanced Search panel is loaded and saved queries are populated in the Advanced Query field. User selects any
        of the listed query, this will retrieve the criteria defined for that query from the database. The criteria
        will be shown on the Advanced Search panel as user input fields so that the user can enter the appropriate
        values to execute the advanced search. This will be called after the getAdvancedSearchInput operation.
        """
        return cls.execute_soa_method(
            method_name='getSelectedQueryCriteria',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='AdvancedSearch',
            params={'selectedQuery': selectedQuery},
            response_cls=AdvancedQueryCriteriaResponse,
        )

    @classmethod
    def createAdvancedSearchInput(cls) -> AdvancedSearchResponse:
        """
        Creates the Advanced Search Input business object (Awp0AdvancedSearchInput). This object is used to populate
        values for the advanced query name or the quick search name. Based on the quick search name or advanced query
        name that is populated on this object, the quick search criteria or advanced search criteria fields are shown
        in the client UI. The Advanced Search object that is created also has a property with the default quick search
        name populated.
        
        Use cases:
        User clicks on the advanced search link in Active Workspace UI. This brings up a panel that is used to collect
        the initial user input for the quick search name or the advanced search name. This panel is represented by the
        Advanced Search Input business object and its properties that is instantiated by this operation.
        """
        return cls.execute_soa_method(
            method_name='createAdvancedSearchInput',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='AdvancedSearch',
            params={},
            response_cls=AdvancedSearchResponse,
        )


class FinderService(TcService):

    @classmethod
    def performSearch2(cls, searchInput: SearchInput, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData) -> SearchResponse2:
        """
        This operation routes a search request to a specific provider specified as providerName in the searchInput
        structures
        
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
            method_name='performSearch2',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData},
            response_cls=SearchResponse2,
        )


class DataManagementService(TcService):

    @classmethod
    def saveEditAndSubmitToWorkflow(cls, inputs: List[SaveEditAndSubmitInfo]) -> SaveEditAndSubmitResponse:
        """
        This operation saves the modified properties for the given input objects and submits the objects to a workflow.
        The workflow is submitted only if all of the save operations are successful. If the save fails for a single
        object  none of  the input objects will be submitted to a workflow.
        
        Use cases:
        User can modify the object(s) properties and submit the object(s) to workflow in one operation. This operation
        first saves the modified properties and then initiates the workflow process for all input objects.
        """
        return cls.execute_soa_method(
            method_name='saveEditAndSubmitToWorkflow',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveEditAndSubmitResponse,
        )

    @classmethod
    def getDeclarativeStyleSheets(cls, processEntireXRT: bool, input: List[GetStyleSheetIn]) -> GetDeclarativeStyleSheetResponse:
        """
        This operation returns the declarative UI definition generated from stylesheets for each input object. It first
        gets the stylesheets for each input object, then converts them into declarative view defintions which can be
        rended as HTML page by declarative UI framework.
        
        Use cases:
        Use Case 1: Load Create Object Panel
        When creating an object of selected type in creation panel, the getDeclarativeStyleSheets SOA operation is
        invoked, and the returned data is parsed/processed in the declarative UI framework to display the creation
        panel.
        
        Use Case 2: Show Object Info
        When an object is selected in ActiveWorkspace, a user may choose the "Show Object Info" command.  When
        executed, a panel slides out from the right hand side of the application, and the selected objects data is
        presented.  In order to populate the panel, the getDeclarativeStyleSheets call is invoked and the returned data
        is parsed and processed in order to build the declarative UI.
        """
        return cls.execute_soa_method(
            method_name='getDeclarativeStyleSheets',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='DataManagement',
            params={'processEntireXRT': processEntireXRT, 'input': input},
            response_cls=GetDeclarativeStyleSheetResponse,
        )

    @classmethod
    def getDefaultRelation(cls, input: List[GetDefaultRelationIn]) -> GetDefaultRelationResponse:
        """
        This operation returns the value of default relation preference for given combination of primary and secondary
        object types as defined by Teamcenter Administrator. The entire type hierarchy of secondary object type is
        traversed while determining the default relation preference. The preference format should be as follows:
        <primary_object_type>_<secondary_object_type>_default_relation
        
        If the secondary object type is passed as empty, then the preference format should be as follows:
        <primaty_object_type>_default_relation
        
        Use cases:
        Use Case 1: Preference for Primary and Secondary object type default relation exists
        Teamcenter Administrator defines the default relation betweeen ItemRevision and DocumentRevision to be
        IMAN_manifestation through the following preference:
        
        ItemRevision_DocumentRevision_default_relation : IMAN_ manifestation
        
        When getDefaultRelation operation of DataManagement service is invoked passing primary object type as
        "ItemRevision" and secondary object type as "DocumentRevision", the response returned is "IMAN_manifestation".
        
        Use Case 2: Preference for Primary and Parent of Secondary object type default relation exists
        Teamcenter Administrator defines the default relation between ItemRevision and DocumentRevision to be
        IMAN_manifestation through the following preference:
        
        ItemRevision_DocumentRevision_default_relation : IMAN_ manifestation
        
        When getDefaultRelation operation of DataManagement service is invoked passing primary object type as
        "ItemRevision" and secondary object type as "EmailRevision", the operation will check preference value for
        given combination of types. In case the preference is not defined for given pair, the operation will try
        finding preference value for combination of  "ItemRevision" and each type in "EmailRevision" business object's
        type hierarchy. EmailRevision inherits DocumentRevision and since the preference for primary type as
        "ItemRevision" and secondary type as "DocumentRevision" is defined, the  default relation in response is
        returned as "IMAN_manifestation". 
        
        Use Case 3: Preference for Primary object type default relation exists
        Teamcenter Administrator defines the default relation for ItemRevision to be IMAN_specification through the
        following preference:
        
        ItemRevision_default_relation : IMAN_ specification
        
        When getDefaultRelation operation of DataManagement service is invoked passing primary object type as
        "ItemRevision" and secondary object type as "DocumentRevision", the operatin will check for preference value
        for input types. In case the preference value for given combination and any combination from secondary type
        hierarchy is not found, the operation will return preference value for "ItemRevision_default_relation" as
        "IMAN_specification".
        """
        return cls.execute_soa_method(
            method_name='getDefaultRelation',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetDefaultRelationResponse,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def setRichContent2(cls, inputs: List[SetContentInput2]) -> ServiceData:
        """
        This operation sets the contents of the FullText or SpecElementRevision object. The input content type can be
        'HTML', 'Plain' or 'RichText' type. All modified objects and exceptions are added to the returned service data.
        Additionally this operation will prevent the user from overwriting the contents of FullText or
        SpecElementRevision object, when multiple users are trying to update contents of same object by comparing last
        saved date of FullText object.
        
        Use cases:
        1. User selects a object of type SpecElement created from Active Workspace client and clicks on the Viewer tab.
        The HTML contents of the selected SpecElement type is shown in the Viewer tab. User can set rich text contents
        of Requirement object by using setRichContent2 operation.
        
        2. When multiple users edit a requirement's content concurrently and try to save using setRichContent2
        operation. It prevent user from overwriting changes of another user for the same requirement by comparing last
        saved date of FullText object.
        """
        return cls.execute_soa_method(
            method_name='setRichContent2',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def exportAsync(cls, inputs: ExportInputDataAsync) -> None:
        """
        This operation exports the selected occurrences in the structure asynchronously to an application such as
        MSExcel. The behavior of export operation is controlled by applicationFormat argument specified in
        ExportInputDataAsync structure. The objects may be checked out during the export.
        
        Following are supported application formats from input.
        
        - MSExcelLive - This mode provides the capability of editing of properties of  underlying ItemRevision in
        MSExcel and save the changes to Teamcenter. The generated sheet allows user to login and change the properties
        from MSExcel application. The changes will be saved to Teamcenter when user exits out of the cell in MSExcel
        application.  Teamcenter extensions for Microsoft Office should be installed on the client machine to support
        this application format.
        - MSExcel - This mode provides the capability of exporting objects to static MSExcel application. 
        - MSExcelReimport - This mode provides the capability of exporting objects to MSExcel application for reimport
        purpose. The generated sheet can be used to add/remove structure elements or to update the properties on the
        SpecElementRevision. The generated sheet should be reimported back to Teamcenter. Office Client should be
        installed on the client machine to support this application format
        
        
        
        Use cases:
        - User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure.User selects an occurrence and clicks on the Export to Excel button in the
        toolbar. This will show a panel with options to "View", "Live Edit" and "Edit and Import". This panel allows
        user to select a template and if user clicks on Export button, an Excel sheet will be generated. If user has
        selected a single occurrence and clicks on export, then the occurrence and all its children are exported to
        MSExcel. If user has selected multiple occurrences and clicks on export, then the selected occurrences are
        exported to MSExcel.
        - User selects single or multiple objects in Active Workspace Client. User clicks on the Export to Excel button
        in the toolbar. User can select View, Edit or Reimport option. Depending upon the option selected, a static
        MSExcel report or a Live MSExcel sheet or a sheet is generated that can be reimported back to Teamcenter.
        - User selects an ItemRevision and clicks on the Export to Excel button on the toolbar. If user selects "Check
        out" option then selected ItemRevision and its children will be checked out and exported to MSExcel.
        - User selects single or multiple objects in ActiveWorkspace Client. User selects the background checkbox in
        the export panel and clicks on the Export to Excel button in the toolbar. This will invoke the Export to Excel
        using the async service options. When the Export to Excel completes, a notification is sent to the client to
        download the Excel file. The generated file is also attached to the MSExcelX dataset.
        - User selects the "apply_bom_crawling" LOV value on the ExcelTemplate and selects an occurrence in ACE and
        clicks on Export to Excel button in the toolbar. This will crawlback from the selected object to its parent's
        recursively till its top line and the exported structure will export the selected line along with its parents.
        
        """
        return cls.execute_soa_method(
            method_name='exportAsync',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=None,
        )

    @classmethod
    def exportToApplication2(cls, input: List[ExportToApplicationInputData3]) -> ExportToApplicationResponse2:
        """
        This operation exports  the selected occurrences in the structure to an application such as MSWord and MSExcel.
        The behavior of export operation is controlled by applicationFormat argument specified in
        ExportToApplicationInput structure. Additionlly this operation allows callers  of the SOA  to supply a
        parameter to let the objects be checked out during export.will allow Teamcenter objects to be checked out.  The
        objects may be checked out during the export. 
        
        Following are supported application formats from input.
        
        -  MSExcelLive - This mode provides the capability of editing of properties of  underlying ItemRevision  in
        MSExcel and save the changes to Teamcenter. The generated sheet allows user to login and change the properties
        from MSExcel application. The changes will be saved to Teamcenter when user exits out of the cell in MSExcel
        application.  Teamcenter extensions for Microsoft Office should be installed on the client machine to support
        this application format.
        - MSWordXMLLive - This mode provides the capability of structural editing of SpecElementRevisions in MSWord.
        Users can edit the rich text of Requirement and perform structural changes to the exported Requirement(s) in
        the word document. Office Client should be installed on the client machine to support this application format.
        -  MSExcel - This mode provides the capability of exporting objects to static MSExcel application. 
        -  MSExcelReimport- This mode provides the capability of exporting objects to MSExcel application for reimport
        purpose. The generated sheet can be used to for add/remove structure elements or to update the properties on
        the SpecElement revision. The generated sheet should be reimported back to  Teamcenter. Office Client should be
        installed on the client machine to support this application format.
        -  MSWordCompare - This mode provides the capability of comparing the contents of source and target objects
        using MSWord application.  The comparison document is generated asynchonously in the background and user is
        notified when the comparison document is generated. Dispatcher and notification services should be running to
        support this application format.
        -  HTML- This mode provides the capability of fetching the HTML contents of input SpecElement objects.
        
        
        
        This operation is for Teamcenter internal use and is unpublished.
        
        Use cases:
        1)  User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure.
        User selects an occurrence and clicks on the Export To Word or Export to Excel button in the toolbar. This
        action will allow users to select a template that will be used for export purpose. If user has selected a
        single occurrence and clicks on export, then the occurrence and all its children are exported to MSWord or
        MSExcel. If user has selected multiple occurrences and clicks on export, then the selected occurrences are
        exported to MSWord or MSExcel.
        
        2)  User selects single or multiple objects in Active Workspace Client. User clicks on the Export to Excel
        button in the toolbar. User can select View, Edit or Reimport option. Depending upon the option selected, a
        static MSExcel report or a Live MSExcel sheet or a sheet is generated that can be reimported back to
        Teamcenter. 
        3)  User selects single or multiple objects in Active Workspace Client and sets them as source objects to
        compare. Similarly user selects single or multiple target objects to compare. User clicks on the Export to Word
        button in the toolbar along with the checkbox for compare contents. User selects the compare contents checkbox
        that allows user to compare the MSWord contents of source and target objects. User is notified when the
        comparison document is generated and attached to a dataset.
        4)  User selects a SpecElement created from Active Workspace client and clicks on the Viewer tab. The HTML
        contents of the selected SpecElement is shown in the Viewer tab.
        5)  User selects an   ItemRevision  and clicks on the Export To Word or Export to Excel button in on the
        toolbar. If user selects "Check out" option then selected  occurrences ItemRevision and its children will be
        checked out and exported to MSWord or MSExcel.
        """
        return cls.execute_soa_method(
            method_name='exportToApplication2',
            library='Internal-AWS2',
            service_date='2016_12',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=ExportToApplicationResponse2,
        )
