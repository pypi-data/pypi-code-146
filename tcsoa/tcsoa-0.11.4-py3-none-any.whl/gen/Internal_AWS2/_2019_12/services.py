from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2016_03.Finder import ColumnConfigInput
from tcsoa.gen.Internal.AWS2._2019_12.Finder import FilterFacetInput, StringMap4, FilterFacetResponse, SearchInput4, ExportObjectsToFileResponse, PropertyInfo
from tcsoa.gen.Internal.AWS2._2019_12.DataManagement import IDContextOutput, IdentifierTypesOut, IdentifierTypesIn, IDDispRuleCreateIn
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class DataManagementService(TcService):

    @classmethod
    def createIdDisplayRules(cls, idDispRuleCreIns: List[IDDispRuleCreateIn]) -> ServiceData:
        """
        This operation creates the ID Display Rules (IdDispRule) with the input names and the corresponding ID Context
        information. ID Display Rule can also be created without the any input ID Context and user can update the
        object later with ID Context information.
        ID Display Rule contains the list of ID Contexts and their order. Based on the order of the ID Contexts
        defined, the system evaluates the display name of the Item and ItemRevision from their Alternate IDs.
        
        ID Context (IdContext), represents the context information under which the OEM defines the unique IDs of their
        Item and ItemRevision. This context information is used when Teamcenter users define the unique IDs of Item and
        ItemRevision objects.
        
        User can set one of the ID Display Rules as the current ID Display Rule. The current ID Display Rule is used to
        evaluate the display names of the Item and ItemRevision. In case the ID Context of the Alternate ID with the
        Item and ItemRevision object does not match with that of the current ID Display Rule then system uses the
        default ID Display Rule to evaluate the display names of Item and ItemRevision objects.
        """
        return cls.execute_soa_method(
            method_name='createIdDisplayRules',
            library='Internal-AWS2',
            service_date='2019_12',
            service_name='DataManagement',
            params={'idDispRuleCreIns': idDispRuleCreIns},
            response_cls=ServiceData,
        )

    @classmethod
    def getIdContexts(cls, inputObjs: List[WorkspaceObject]) -> IDContextOutput:
        """
        This operation fetches all instances of the ID Context objects (IdContext) from the Teamcenter database
        applicable for the input objects of type Item and ItemRevision based on defined ID Context Rules
        (IdContextRule) by the system administrators.
        
        This operation queries ID Context Rule objects and fetches the ID Context objects based on the input Item,
        ItemRevision or NULL. The input is the identifiable type defined on the ID Context Rules. For a NULL input, it
        returns the Id Context objects where the identifiable type is NULL.
        All ID Context objects from the Teamcenter data base are returned in case input object is other than Item,
        ItemRevision or NULL. An empty input list would also return all ID Context objects from the Teamcenter data
        base.
        
        IdContext objects represents the context information under which the OEM defines the unique IDs of their Item
        and ItemRevision objects. This context information is used when Teamcenter users define the unique IDs of Item
        and ItemRevision objects.
        
        Alternate and Alias IDs of Teamcenter are the example of the such unique IDs of Item and ItemRevision. Users
        define Alternate and Alias IDs with the help of the ID Context as one of the unique attribute of the ID.
        """
        return cls.execute_soa_method(
            method_name='getIdContexts',
            library='Internal-AWS2',
            service_date='2019_12',
            service_name='DataManagement',
            params={'inputObjs': inputObjs},
            response_cls=IDContextOutput,
        )

    @classmethod
    def getIdentifierTypes(cls, identifierTypesIn: List[IdentifierTypesIn]) -> IdentifierTypesOut:
        """
        This operation fetches the applicable Identifier types for the input objects of type Item and/or ItemRevision
        along with the input IdContext object. System queries the ID Context Rules defined in Teamcenter database and
        retrives the Identifier types.
        
        Alternate and Alias IDs are defined in Teamcenter as instances of business object of type Identifier. ID
        Context, of business object type IdContext, represents the context information under which the OEM defines the
        unique IDs of their Item and ItemRevision. This context information is used when Teamcenter users define the
        Alternate and Alias IDs of Item and ItemRevision objects.
        
        ID Context Rules are defined as instances of business object type IdContextRule in Teamcenter database. These
        rules map the combination of ID Context and the object type e.g.  Item or ItemRevision, called Identifiable
        types, to the type of the Identifier applicable in the context.
        
        This operation also returns the other applicable objects for which Alternate IDs along with the input objects
        can be defined. In case of input objects of type Item, this operation returns the list of revision objects of
        the Item, and in case of input objects of type ItemRevision, this operation returns the Item object as the
        applicable object for which Alternate IDs can be defined.
        """
        return cls.execute_soa_method(
            method_name='getIdentifierTypes',
            library='Internal-AWS2',
            service_date='2019_12',
            service_name='DataManagement',
            params={'identifierTypesIn': identifierTypesIn},
            response_cls=IdentifierTypesOut,
        )


class FinderService(TcService):

    @classmethod
    def exportObjectsToFile(cls, searchInput: SearchInput4, objectsToExport: List[str], attributesToExport: List[PropertyInfo], columnConfigInput: ColumnConfigInput, exportOptions: StringMap4) -> ExportObjectsToFileResponse:
        """
        This operation exports either a given list of objects or the objects found through the given search input. If
        searchInput and objectsToExport are both present in the input, then objectsToExport will take precedence. The
        objects are exported in a tabular format, with the objects as the rows and the given attributesToExport as the
        columns. If an object does not contain an attribute in attributesToExport then the value that will be exported
        is an empty string. There is also no relation between attributesToExport and columnsToExclude from
        columnConfigInput. 
        
        This operation allows callers to specify export options, which determines the behavior of the export operation.
        The only supported export option for AW4.3 is "fileFormat":"MSExcel" but will be extended in future releases.
        
        Use cases:
        1) User clicks the export command in an object set, which launches the export properties panel. User selects
        the desired properties to export and clicks the export button. Then the objects and the selected properties are
        exported into a table into Excel.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsToFile',
            library='Internal-AWS2',
            service_date='2019_12',
            service_name='Finder',
            params={'searchInput': searchInput, 'objectsToExport': objectsToExport, 'attributesToExport': attributesToExport, 'columnConfigInput': columnConfigInput, 'exportOptions': exportOptions},
            response_cls=ExportObjectsToFileResponse,
        )

    @classmethod
    def getFilterValues(cls, filterFacetInput: FilterFacetInput) -> FilterFacetResponse:
        """
        This operation fetches the possible filter values (Facets) of a given column in a table. Each table in Active
        Workspace is typically backed by a provider, so the input of this operation is similar to performSearch
        operation&rsquo;s searchInput request. 
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
        
        This operation provides a common interface to get Filter Facet values in a generic way from any data provider
        that is compatible with performSearch operation. This operation takes the data provider which is responsible
        for fetching the objects, a columnName one which the filter values need to be obtained, and a filter or query
        criteria which is used to refine the filter facet values. Once the query or filtering is complete, the ui
        values are obtained from the search results and are returned as the facet values.
        
        Use cases:
        User clicks on "Name" column in Home Folder and clicks on Show Filters to expand the possible Filter facet
        values
        A getFilterValues request will be made by passing in the needed query or filter criteria. In this case the
        provider name is "Awp0ObjectSetRowProvider". The provider is responsible for fetching the objects of the Home
        Folder, then it queries for the Name property of all the objects returned by the data provider and returns a
        unique sorted UI values for the "Name" column. These are the facet results and are shown in a list of
        checkboxes in a column menu in the client.
        """
        return cls.execute_soa_method(
            method_name='getFilterValues',
            library='Internal-AWS2',
            service_date='2019_12',
            service_name='Finder',
            params={'filterFacetInput': filterFacetInput},
            response_cls=FilterFacetResponse,
        )
