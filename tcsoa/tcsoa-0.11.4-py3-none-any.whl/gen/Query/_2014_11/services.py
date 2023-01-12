from __future__ import annotations

from typing import List
from tcsoa.gen.Query._2014_11.Finder import ObjectsGroupedByPropertyResponse, ObjectPropertyGroupInput, SearchResponse2, SearchInput2
from tcsoa.base import TcService


class FinderService(TcService):

    @classmethod
    def groupObjectsByProperties(cls, objectPropertyGroupInputList: List[ObjectPropertyGroupInput]) -> ObjectsGroupedByPropertyResponse:
        """
        This operation classifies business objects into groups. In the list of ObjectPropertyGroupInput objects, each
        object containing an internal property name, list of PropertyGroupingValue objects identifying groups and a
        list of business objects to be classified into the groups. Each PropertyGroupingValue object contains a start
        and an end value. The end value is used for range values if populated. Unclassified business objects are
        retuned back in a list.
        
        Use cases:
        In Active Workspace client, a user navigates to a new filter category on the filter panel. The cells in the
        visible view for the search results (e.g. list view or table view) need to be colored to match the colors on
        the bar chart for the objects in the search results. The client invokes this operation, which identifies the
        property group (or bar on the chart) the objects belong to. The client can then color the cells corresponding
        to the objects appropriately based on the grouping information that is returned.
        """
        return cls.execute_soa_method(
            method_name='groupObjectsByProperties',
            library='Query',
            service_date='2014_11',
            service_name='Finder',
            params={'objectPropertyGroupInputList': objectPropertyGroupInputList},
            response_cls=ObjectsGroupedByPropertyResponse,
        )

    @classmethod
    def performSearch(cls, searchInput: SearchInput2) -> SearchResponse2:
        """
        This operation routes search request to a specific provider specified as providerName in the searchInput
        structures. 
        A framework allows custom solution to be able to provide a new specific provider to collect data, perform
        sorting and filtering. Such provider can be a User Inbox retriever, or Full Text searcher. The new data
        provider can be encapsulated via a new runtime business object from Fnd0BaseProvider class. The implementation
        is done using its fnd0performSearch operation.
        
        RuntimeBusinessObject
        ---- Fnd0BaseProvider (foundation template)
        -------- Fnd0GetChildrenProvider(foundation template)
        -------- Awp0FullTextSearchProvider (aws template)
        -------- Awp0TaskSearchProvider (aws template)
        -------- Aos0TestProvider (aosinternal template)
        -------- etc.
        
        This operation provides a common interface to send the request to and receive the response from a new data
        provider. Ultimately it allows common framework in UI to support filter, pagination, and sorting. 
        This operation allows user to send the search input, filter values, and sorting data.  These input values then
        be passed to the fnd0performSearch operation input values, which then use to collect, sort, and filter its
        results.
        The first two input parameters are important.  The first input is provider name.  This is a string to represent
        the type name of RuntimeBusinessObject to which this request should be routed to.  If the template that
        contains the class is not installed, a partial error 217016 is returned. The second input is the search input
        map.  The key is different per each provider.  For example, for Full Text searcher, the input key would be
        searchString.  For User Inbox retriever, the input key would be Inbox Type.  The fnd0performSearch
        implementation for each provider shall take into account on the key name as it is used to store the values in
        OperationInput object.
        """
        return cls.execute_soa_method(
            method_name='performSearch',
            library='Query',
            service_date='2014_11',
            service_name='Finder',
            params={'searchInput': searchInput},
            response_cls=SearchResponse2,
        )
