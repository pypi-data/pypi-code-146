from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2017_06.RequirementsManagement import ExportToApplicationInputData4, BaselineInputData, BaselineInputDataAsync
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchInput, ColumnConfigInput, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2016_03.RequirementsManagement import ExportToApplicationResponse2
from tcsoa.gen.Internal.AWS2._2016_03.UiConfig import GetOrResetUIColumnConfigInput
from tcsoa.gen.Internal.AWS2._2017_06.UiConfig import GetOrResetUIColumnConfigResponse
from tcsoa.gen.Internal.AWS2._2016_04.DataManagement import GetStyleSheetIn
from tcsoa.gen.Internal.AWS2._2017_06.DataManagement import GetStyleSheetResponse, SaveViewModelEditAndSubmitResponse, GetViewerDataResponse, GetViewerDataIn, GetViewModelPropsResponse, LoadViewModelForEditingResponse, SaveViewModelEditAndSubmitInfo, LoadViewModelForEditingInfo
from tcsoa.gen.Internal.AWS2._2017_06.FullTextSearch import IdentifyImpactedObjectsResponse, IdentifyImpactedObjInput
from typing import List
from tcsoa.gen.Internal.AWS2._2017_06.EffectivityManagment import ReleaseStatusEffectivityInput
from tcsoa.gen.Internal.AWS2._2017_06.Finder import SearchResponse3
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivityManagmentService(TcService):

    @classmethod
    def addOrRemoveRelStatusEffectivities(cls, input: ReleaseStatusEffectivityInput) -> ServiceData:
        """
        This operation adds or removes shared Effectivity objects to or from the input ReleaseStatus.
        
        Exceptions:
        >126231 The effectivities cannot be updated on ReleaseStatus.
        """
        return cls.execute_soa_method(
            method_name='addOrRemoveRelStatusEffectivities',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='EffectivityManagment',
            params={'input': input},
            response_cls=ServiceData,
        )


class UiConfigService(TcService):

    @classmethod
    def getOrResetUIColumnConfigs2(cls, getOrResetUiConfigsIn: List[GetOrResetUIColumnConfigInput]) -> GetOrResetUIColumnConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes column configuration information. 
        If the resetColumnConfig flag is "True", this operation deletes the column configuration of the input scope and
        then queries the new effective UI column configuration for the login user. This operation will clear the login
        user column configurations.
        
        Use cases:
        Request UI Configuration(s) based on the current login user
        Client requests the column information for one or more client scopes using this operation and scope as login
        user.
        
        Request UI Configuration(s) based on a specific Teamcenter scope
        Client requests the column information for one or more client scopes using this operation and scope as Role,
        Site or Group.
        
        Request to reset UI Column Configuration(s) based on the current login user
        If a client needs to reset the column information for login user scope, they can use this operation. The new
        effective UI column configuration will be retrieved for the login user.
        """
        return cls.execute_soa_method(
            method_name='getOrResetUIColumnConfigs2',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='UiConfig',
            params={'getOrResetUiConfigsIn': getOrResetUiConfigsIn},
            response_cls=GetOrResetUIColumnConfigResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def getStyleSheet3(cls, processEntireXRT: bool, input: List[GetStyleSheetIn]) -> GetStyleSheetResponse:
        """
        This operation returns the stylesheets and the required data to present that stylesheet for each input object.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getStylesheet call is invoked and the stylesheet is processed in order to display the
        data to the user.
        
        Use Case 2: List view with Summary
        When an object is selected in the ActiveWorkspace navigator, when in list view with summary mode, the
        getStyleSheet operation is invoked, and the returned data is parsed and processed in order to present the data
        to the user in the Summary panel.
        
        Use Case 3: Show Object Info
        When an object is selected in ActiveWorkspace, a user may choose the "Show Object Info" command.  When
        executed, a panel slides out from the right hand side of the application, and the selected objects data is
        presented.  In order to populate the panel, the getStylesheet call is invoked and the returned data is parsed
        and processed in order to build the UI.
        """
        return cls.execute_soa_method(
            method_name='getStyleSheet3',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='DataManagement',
            params={'processEntireXRT': processEntireXRT, 'input': input},
            response_cls=GetStyleSheetResponse,
        )

    @classmethod
    def getViewModelProperties(cls, objects: List[BusinessObject], attributes: List[str]) -> GetViewModelPropsResponse:
        """
        This service operation is provided to get property values of instances outside of the current object property
        policy for a particular business object.This operation is an enhanced version of the getProperties service
        operation and allows for retrieving values of dynamic compound properties as well.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getViewModelProperties call is executed to fetch required properties.
        """
        return cls.execute_soa_method(
            method_name='getViewModelProperties',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='DataManagement',
            params={'objects': objects, 'attributes': attributes},
            response_cls=GetViewModelPropsResponse,
        )

    @classmethod
    def getViewerData(cls, inputs: GetViewerDataIn) -> GetViewerDataResponse:
        """
        This operation returns the dataset, file and relevant viewer data for given combination of input object,
        dataset  and direction by processing the viewer preference set by Teamcenter Administrator. Datasets associated
        with input object are retrieved and sorted based on the values of viewer preference. Thereafter, appropriate
        dataset is identified using the input dataset and direction. The corresponding file and viewer information
        along with dataset is returned in the response.
        """
        return cls.execute_soa_method(
            method_name='getViewerData',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=GetViewerDataResponse,
        )

    @classmethod
    def loadViewModelForEditing(cls, inputs: List[LoadViewModelForEditingInfo]) -> LoadViewModelForEditingResponse:
        """
        This method ensures that the properties can be edited, and returns the last save date of the related objects
        for optimistic edit. This service operation is similar to loadDataForEditing service operation, the difference
        is that this operation saves the ViewModelObject instead of model object, and this operation supports dynamic
        compound properties. If the property is dynamic compound property, this operation checks if the traversal path
        on server is same as the input traversal path , if it is not the same, then editing is not allowed.
        """
        return cls.execute_soa_method(
            method_name='loadViewModelForEditing',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=LoadViewModelForEditingResponse,
        )

    @classmethod
    def saveViewModelEditAndSubmitWorkflow(cls, inputs: List[SaveViewModelEditAndSubmitInfo]) -> SaveViewModelEditAndSubmitResponse:
        """
        This operation saves the modified view model properties for the given input objects and submits the objects to
        a workflow. The workflow is submitted only if all of the save operations are successful. If the save fails for
        a single object  none of the input objects will be submitted to a workflow. This operation is similar to the
        saveEditAndSubmitToWorkflow operation, the difference is that this operation saves the ViewModelObject instead
        of model object, and this operation supports dynamic compound properties.
        
        Use cases:
        User can modify the object(s) properties and submit the object(s) to workflow in one operation. This operation
        first saves the modified properties and then initiates the workflow process for all input objects.
        """
        return cls.execute_soa_method(
            method_name='saveViewModelEditAndSubmitWorkflow',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=SaveViewModelEditAndSubmitResponse,
        )


class FullTextSearchService(TcService):

    @classmethod
    def identifyImpactedObjects(cls, impactedObjectsInput: IdentifyImpactedObjInput) -> IdentifyImpactedObjectsResponse:
        """
        The operation identifies the siblings of Revisionable Objects that have been added/modified/deleted.
        
        The identified siblings are marked in the accountability table with the TIE sync status provided and returned
        if requsted
        
        Based on the value of the addModDelBitMask the following steps will be executed. 
        Steps:
        1.  Queries for siblings of deleted objects from scratch table. Gets their parent Item objects from
        accountability table impacted island if they exist. For the Item objects found, it fetches all the Revisionable
        Objects and adds them to the response.
        2.  Queries for siblings of newly added objects from scratch table. Filters out non Revisionable Objects from
        the list.
        Adds the Revisionable Objects to the reponse.
        3.  Queries for any Modified islands from the accountability table. If modified island belongs to an
        Revisionable Objects, then queries for the Revisionable Objects siblings and adds to the response.
        
        Finally the response will contain the impacted Revisionable Objects due to adds/modify/deletes.
        
        Use cases:
        Use Cases:
        Use Case 1: TcFtsIndexer Sync
        
        Whenever Revisionable Objects are indexed  the Revision rule slector information (Working, Latest Working,
        etc&hellip;) is also indexed on each Revisionable Object. So whenever  a new Revisionable Object  is
        added/deleted/modified that impacts all the Revisionable Object associated with its parent Item and the
        revision rule selector information need to be regenerated. This operation will help in identifying the impacted
        objects and they can be re-indexed to sync the index data .
        """
        return cls.execute_soa_method(
            method_name='identifyImpactedObjects',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='FullTextSearch',
            params={'impactedObjectsInput': impactedObjectsInput},
            response_cls=IdentifyImpactedObjectsResponse,
        )


class FinderService(TcService):

    @classmethod
    def performSearchViewModel(cls, searchInput: SearchInput, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData, inflateProperties: bool) -> SearchResponse3:
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
        
        ---
        """
        return cls.execute_soa_method(
            method_name='performSearchViewModel',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData, 'inflateProperties': inflateProperties},
            response_cls=SearchResponse3,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def createBaseline(cls, input: List[BaselineInputData]) -> ServiceData:
        """
        This operation creates baseline of the selected business object.The selected object can be of type ItemRevision
        or Awb0Element .Baseline is a mechanism to to preserve the current state of the object in time . This is a
        synchronous operation and it returns back immediately with partial errors if any. This operation calls
        createBaselineAsync (asynchronous service operation) which performs the actual baseline creation. When the
        business object selected for baselining is a structure occurrence of type Awb0Element, new baseline revision is
        created for all the occurrences in that structure. When the selected business object is of type ItemRevision,
        then a single baseline revision is created. User is notified after baseline creation is complete.
        
        This operation is for Teamcenter internal use and is unpublished.
        
        Use cases:
        1. User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure.
        User selects an occurrence and in Tool and Info command bar, clicks on 'Save As or Revise' option. This will
        show up a panel with tab options as  "Revision" and  "New". In Revision tab, 'Save as Baseline' checkbox is
        present. After selecting this checkbox, 'Baseline Template' dropdown box appears. The user selects a baseline
        template from dropdown followed by a click on "Save" button, resulting into baseline creation. Irrespective of
        the selected occurrence, after clicking "Save"; the entire structure ie. top most parent occurrence and all its
        children are baselined. When the baseline creation completes, a notification is sent to the client.
        
        2. User selects an ItemRevision in non ACE view and in Tool and Info command bar clicks on 'Save As or Revise'
        option. This will show up a panel with tab options as  "Revision" and  "New". After selecting this checkbox,
        'Baseline Template' dropdown box appears. In Revision tab, 'Save as Baseline' checkbox is present. The user
        selects a baseline template from dropdown followed by a click on "Save" button, resulting into baseline
        creation for this item revision. When the baseline creation completes, a notification is sent to the client.
        """
        return cls.execute_soa_method(
            method_name='createBaseline',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def createBaselineAsync(cls, input: List[BaselineInputDataAsync]) -> None:
        """
        This operation creates baseline of the selected business object.The selected object can be of type ItemRevision
        or Awb0Element .Baseline is a mechanism to to preserve the current state of the object in time . This is
        asynchronous operation and is invoked by synchronous service operation createBaseline . createBaselineAsync
        operation performs the actual baseline creation. When the business object selected for baselining is a
        structure occurrence of type Awb0Element, new baseline revision is created for all the occurrences in that
        structure. When the selected business object is of type ItemRevision, then a single baseline revision is
        created. User is notified after baseline creation is complete.
        
        Use cases:
        1. User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure.
        User selects an occurrence and in Tool and Info command bar, clicks on 'Save As or Revise' option. This will
        show up a panel with tab options as  "Revision" and  "New". In Revision tab, 'Save as Baseline' checkbox is
        present. After selecting this checkbox, 'Baseline Template' dropdown box appears. The user selects a baseline
        template from dropdown followed by a click on "Save" button, resulting into baseline creation. Irrespective of
        the selected occurrence, after clicking "Save"; the entire structure ie. top most parent occurrence and all its
        children are baselined. When the baseline creation completes, a notification is sent to the client.
        
        2. User selects an ItemRevision in non ACE view and in Tool and Info command bar clicks on 'Save As or Revise'
        option. This will show up a panel with tab options as  "Revision" and  "New". After selecting this checkbox,
        'Baseline Template' dropdown box appears. In Revision tab, 'Save as Baseline' checkbox is present. The user
        selects a baseline template from dropdown followed by a click on "Save" button, resulting into baseline
        creation for this item revision. When the baseline creation completes, a notification is sent to the client.
        """
        return cls.execute_soa_method(
            method_name='createBaselineAsync',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=None,
        )

    @classmethod
    def exportAsync2(cls, input: ExportToApplicationInputData4) -> None:
        """
        This operation exports the selected occurrences in the structure asynchronously to an application such as
        MSExcel and MSWord. The behavior of export operation is controlled by applicationFormat and
        objectTemplateInputs arguments specified in ExportInputDataAsync2 structure. If user selects the "include
        attachments" option, then this operation can export a .zip file that will include all the attachments
        associated with the selected object along with the document. The objects may be checked out during the export.
        
        Following are supported application formats from input.
        
        - MSExcelLive - This mode provides the capability of editing of properties of underlying ItemRevision in
        MSExcel and save the changes to Teamcenter. The generated sheet allows user to login and change the properties
        from MSExcel application. The changes will be saved to Teamcenter when user exits out of the cell in MSExcel
        application.  Teamcenter extensions for Microsoft Office should be installed on the client machine to support
        this application format.
        - MSExcel - This mode provides the capability of exporting objects to static MSExcel application. 
        - MSExcelReimport - This mode provides the capability of exporting objects to MSExcel application for reimport
        purpose. The generated sheet can be used to add/remove structure elements or to update the properties on the
        SpecElementRevision. The generated sheet should be reimported back to Teamcenter. Office Client should be
        installed on the client machine to support this application format.
        - MSWordXMLLive - This mode provides the capability of structural editing of SpecElementRevision in MSWord.
        Users can edit the rich text of Requirements and perform structural changes to the exported Requirements in the
        word document. Office Client should be installed on the client machine to support this application format.
        
        
        
        Use cases:
        - User loads a structure in ACE (Active Content Experience) panel. The ACE panel is used for smart navigation
        of occurrences in a structure. User selects an occurrence and clicks on the Export to Excel button in the
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
        - User selects single or multiple objects in ActiveWorkspace Client. User selects the background checkbox in
        the export panel and clicks on the Export to Word button in the toolbar. This will invoke the Export to MSWord
        using the async service options. When the Export to MSWord completes, a notification is sent to the client to
        download the file.
        - User selects single or multiple objects in Active Workspace Client, and clicks on   Export to Word button on
        the toolbar. User may select the Object Template that will be applied on the exported document.
        - User selects single or multiple objects in Active workspace client and clicks on Export to Word button on the
        toolbar. If the user selects "Include attachments"option, then a zip file will be exported that includes the
        Word document along with all the attachments associated with the selected object.
        
        """
        return cls.execute_soa_method(
            method_name='exportAsync2',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=None,
        )

    @classmethod
    def exportToApplication3(cls, input: List[ExportToApplicationInputData4]) -> ExportToApplicationResponse2:
        """
        This operation exports  the selected occurrences in the structure to an application such as MSWord and MSExcel.
        The behavior of export operation is controlled by applicationFormat and objectTemplateInputs arguments
        specified in ExportToApplicationInput4 structure. If user selects the "include attachments" option, then this
        operation can export a .zip file that will include all the attachments associated with the selected object
        along with the document. The objects may be checked out during the export.
        
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
        - HTML- This mode provides the capability of fetching the HTML contents of input SpecElement objects.
        
        
        
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
        - User selects single or multiple objects in Active Workspace Client and sets them as source objects to
        compare. Similarly user selects single or multiple target objects to compare. User clicks on the Export to Word
        button in the toolbar along with the checkbox for compare contents. User selects the compare contents checkbox
        that allows user to compare the MSWord contents of source and target objects. User is notified when the
        comparison document is generated and attached to a dataset.
        - User selects a SpecElement created from Active Workspace client and clicks on the Viewer tab. The HTML
        contents of the selected SpecElement is shown in the Viewer tab.
        - User selects an  ItemRevision and clicks on the Export To Word or Export to Excel button on the toolbar. If
        user selects "Check out" option then selected ItemRevision and its children will be checked out and exported to
        MSWord or MSExcel.
        - User selects single or multiple objects in Active Workspace Client, and clicks on   Export to Word button on
        the toolbar. User may select the Object Template that will be applied on the exported document.
        - User selects single or multiple objects in Active workspace client and clicks on Export to Word button on the
        toolbar. If user selects "Include attachments"option, then a zip file will be exported that includes the Word
        document along with all the attachments associated with the selected object.
        
        """
        return cls.execute_soa_method(
            method_name='exportToApplication3',
            library='Internal-AWS2',
            service_date='2017_06',
            service_name='RequirementsManagement',
            params={'input': input},
            response_cls=ExportToApplicationResponse2,
        )
