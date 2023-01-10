from __future__ import annotations

from tcsoa.gen.Internal.Search._2020_12.SearchFolder import GetSearchFolderAccessorsOutput, ImportInput, ExportSearchFoldersResponse, ReportSearchRecipeInput, SearchFoldersInput, CreateOrEditSearchFoldersOutput, ReportSearchRecipeResponse, ImportSearchFolderResponse
from typing import List
from tcsoa.base import TcService


class SearchFolderService(TcService):

    @classmethod
    def getSearchFolderAccessors(cls, searchFolders: List[str]) -> GetSearchFolderAccessorsOutput:
        """
        Returns list of accessors for each of the provided Awp0SearchFolder instance. An Awp0SearchFolder can be shared
        with different organizational entities like users, groups, roles. The list of accessors represent these
        entities with whom the folder has been shared.
        
        Use cases:
        When a user selects an Awp0SearchFolder instance, the list of accessors having share access on the folder
        should also be displayed. Client will make a call to this operation to get the accessors list.
        """
        return cls.execute_soa_method(
            method_name='getSearchFolderAccessors',
            library='Internal-Search',
            service_date='2020_12',
            service_name='SearchFolder',
            params={'searchFolders': searchFolders},
            response_cls=GetSearchFolderAccessorsOutput,
        )

    @classmethod
    def getTranslatedReportSearchRecipe(cls, reportDefinitionCriteria: List[ReportSearchRecipeInput]) -> ReportSearchRecipeResponse:
        """
        Generates target data source compatible search recipe and parameters for a given list of Teamcenter
        ReportDefinition objects. The returned search recipes can be directly consumed by external data sources, like
        Solr, without additional help from Teamcenter. A ReportDefinition object holds platform independent search
        recipe. When this object is opened or executed from within Teamcenter applications, the recipe is first
        translated to work with the target data source and then necessary search actions are performed. This operation
        provides translated search parameters to the caller so that search actions associated with Reports can be done
        outside of Teamcenter.
        
        Use cases:
        Currently Teamcenter product data can be indexed in Apache Solr search engine as part of Active Workspace
        solution to facilitate full text search. The Active Workspace global search feature allows users to find and
        load Teamcenter objects indexed in Solr. To take further advantage of the indexed Teamcenter data in Solr, a
        microservice to generate charting information for a requested Teamcenter property has been introduced. The
        microservice expects a Solr compatible query to be sent as part of the request, along with the property for
        which charting information is desired. It then executes the query and sends back analytical information which
        the client can display as charts. Operation getTranslatedReportSearchRecipe provides the calling client
        information necessary to make a request to the microservice. 1.    Client calls the
        getTranslatedReportSearchRecipe operation to obtain Solr compatible translated search parameters for a group of
        ReportDefinition objects. 
        2.    Once the client obtains the necessary information, it makes asynchronous call to the microservice using
        the translated search parameters.
        3.    Microservice performs the necessary search action, puts together charting response for the requested
        ReportDefinition objects and sends it back to the client.
        4.    Client can then render the obtained data as charts.
        Note: Since the whole search and chart generation process does not involve Teamcenter, live update of the
        Report objects can be done asynchronously and without blocking the client from executing any other actions.
        """
        return cls.execute_soa_method(
            method_name='getTranslatedReportSearchRecipe',
            library='Internal-Search',
            service_date='2020_12',
            service_name='SearchFolder',
            params={'reportDefinitionCriteria': reportDefinitionCriteria},
            response_cls=ReportSearchRecipeResponse,
        )

    @classmethod
    def importSearchFolder(cls, input: ImportInput) -> ImportSearchFolderResponse:
        """
        Imports a TCXML file containing Awp0SearchFolder object with its hierarchy and its associated ReportDefinition
        and Awp0SearchFolderShareRule objects.
        
        Use cases:
        Importing an Awp0SearchFolder hierarchy under an existing Awp0SearchFolder object
        
        1. In Active Workspace client, user selects an existing Awp0SearchFolder object and clicks on the Import Active
        Folder command. A panel is displayed where the user can specify input TCXML file to import. 
        
        2. Once the user chooses a valid file, a preview of the Awp0SearchFolder hierarchy that is to be imported is
        rendered. 
        
        3. After the preview is complete, a button to import the file is displayed. When the user clicks on the import
        button, the folder hierarchy will be imported under the selected Awp0SearchFolder object.
        
        Note: If an existing Awp0SearchFolder object is not selected during import, the hierarchy read from the input
        TCXML file will be created under the user&rsquo;s Awp0MySearchFolder object.
        """
        return cls.execute_soa_method(
            method_name='importSearchFolder',
            library='Internal-Search',
            service_date='2020_12',
            service_name='SearchFolder',
            params={'input': input},
            response_cls=ImportSearchFolderResponse,
        )

    @classmethod
    def createOrEditSearchFolders(cls, input: List[SearchFoldersInput]) -> CreateOrEditSearchFoldersOutput:
        """
        Creates or edits one or more Awp0SearchFolder objects. An Awp0SearchFolder object is a subtype of Folder with
        an integrated search definition. It displays dynamic contents based on the search definition it contains.
        Internally, Awp0SearchFolder' s search definition is represented by a ReportDefinition object. This operation
        supports creation and modification of Awp0SearchFolder's with necessary inputs.
        
        Use cases:
        Create Active Folders: User needs to create one or more instances of Awp0SearchFolder with their respective
        search definitions. Edit existing instances of Awp0SearchFolder: User needs to modify existing Active Folder
        instances. This can include updating the existing search definition or other Search Folder attributes like name
        or description.
        """
        return cls.execute_soa_method(
            method_name='createOrEditSearchFolders',
            library='Internal-Search',
            service_date='2020_12',
            service_name='SearchFolder',
            params={'input': input},
            response_cls=CreateOrEditSearchFoldersOutput,
        )

    @classmethod
    def exportSearchFolders(cls, searchFolderUIDs: List[str]) -> ExportSearchFoldersResponse:
        """
        Exports one or more Awp0SearchFolder objects and its hierarchy. Every valid instance of Awp0SearchFolder is
        exported with its associated ReportDefinition and Awp0SearchFolderShareRule.
        
        Use cases:
        1. In Active Workspace, users will click on an Awp0SearchFolder object and on clicking the "Export Active
        Folder" command, an exported TCXML will be send back to the client through a transient file ticket in the
        service response, which the client  uses to download the exported file.
        """
        return cls.execute_soa_method(
            method_name='exportSearchFolders',
            library='Internal-Search',
            service_date='2020_12',
            service_name='SearchFolder',
            params={'searchFolderUIDs': searchFolderUIDs},
            response_cls=ExportSearchFoldersResponse,
        )
