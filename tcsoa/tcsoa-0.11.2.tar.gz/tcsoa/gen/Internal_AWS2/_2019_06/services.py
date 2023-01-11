from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2019_06.AdvancedSavedSearch import Awp0AdvancedSavedSearchResponse, Awp0CreateAdvancedSavedSearchInput, Awp0UpdateAdvancedSavedSearchInput
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.AWS2._2016_03.Finder import ColumnConfigInput
from tcsoa.gen.Internal.AWS2._2019_06.RequirementsManagement import RequirementInput, FullTextResponse
from typing import List
from tcsoa.gen.Internal.AWS2._2019_06.Finder import SaveColumnConfigData2, SearchResponse6, SearchInput3
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def modifyFavorites(cls, favorites: List[BusinessObject], action: str) -> ServiceData:
        """
        This operation updates the user's favorites by adding or removing the objects specified with the input.
        
        Favorites are stored per user in the database as Teamcenter preference: "MyFavorites"
        
        The operation takes list of objects and the action as input whether to add or remove and finalizes the complete
        list of favorites before they are saved to the database. This implies that the caller of the operation needs to
        send delta list of objects to add or remove to the user's favorites.
        """
        return cls.execute_soa_method(
            method_name='modifyFavorites',
            library='Internal-AWS2',
            service_date='2019_06',
            service_name='DataManagement',
            params={'favorites': favorites, 'action': action},
            response_cls=ServiceData,
        )


class FinderService(TcService):

    @classmethod
    def performSearchViewModel4(cls, searchInput: SearchInput3, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData2, inflateProperties: bool, noServiceData: bool) -> SearchResponse6:
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
            method_name='performSearchViewModel4',
            library='Internal-AWS2',
            service_date='2019_06',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData, 'inflateProperties': inflateProperties, 'noServiceData': noServiceData},
            response_cls=SearchResponse6,
        )


class AdvancedSavedSearchService(TcService):

    @classmethod
    def updateAdvancedSavedSearch(cls, inputs: List[Awp0UpdateAdvancedSavedSearchInput]) -> Awp0AdvancedSavedSearchResponse:
        """
        This operation updates advanced saved searches for given inputs.
        """
        return cls.execute_soa_method(
            method_name='updateAdvancedSavedSearch',
            library='Internal-AWS2',
            service_date='2019_06',
            service_name='AdvancedSavedSearch',
            params={'inputs': inputs},
            response_cls=Awp0AdvancedSavedSearchResponse,
        )

    @classmethod
    def createAdvancedSavedSearch(cls, inputs: List[Awp0CreateAdvancedSavedSearchInput]) -> Awp0AdvancedSavedSearchResponse:
        """
        This operation creates advanced saved searches for given inputs.
        """
        return cls.execute_soa_method(
            method_name='createAdvancedSavedSearch',
            library='Internal-AWS2',
            service_date='2019_06',
            service_name='AdvancedSavedSearch',
            params={'inputs': inputs},
            response_cls=Awp0AdvancedSavedSearchResponse,
        )


class RequirementsManagementService(TcService):

    @classmethod
    def getFullTextVersionInfo(cls, inputs: List[RequirementInput]) -> FullTextResponse:
        """
        This operation retrieves the information about the FullText dataset versions for the given Requirements. It
        also retrieves the contents and properties of the FullText dataset which are displayed in the user interface.
        The following partial errors may be returned:
        159001: An internal error has occurred in the Requirements Management module. Please report this error to your
        system administrator.
        141308: The type of operation to perform in invalid.
        141309: The selected input object does not contain FullText object.
        
        Use cases:
        Use Case 1: Get FullText dataset versions and contents
        User selects a Requirement in Home folder. User goes to History tab where document history list will be
        displayed.This document history list will contain information about all the Requirement Revision and its
        FullText dataset versions and its contents. User selects any two FullText dataset versions and clicks on
        compare which will give compare HTML report.
        
        Use Case 2: Get FullText dataset versions during Freeze of derived Requirement
        User loads the requirement specification in ACE (Active Content Experience) panel. User clicks on 'Reuse'
        command which shows the 'Reuse and Derived' panel. User selects 'Create a derived Specification' and selects a
        tracelink type and clicks on Create button. This creates a derived of the existing Requirement specification.
        User selects a derived Requirement and clicks on 'Freeze' option which shows the FullText dataset versions.
        User will pick a version and clicks on Ok button. This will freeze the Requirement and it will show the
        contents from the dataset version that user had picked.
        """
        return cls.execute_soa_method(
            method_name='getFullTextVersionInfo',
            library='Internal-AWS2',
            service_date='2019_06',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=FullTextResponse,
        )
