from __future__ import annotations

from tcsoa.gen.Query._2012_10.Finder import SearchResponse, SearchInput
from tcsoa.base import TcService


class FinderService(TcService):

    @classmethod
    def performSearch(cls, searchInput: SearchInput) -> SearchResponse:
        """
        This operation routes search request to a specific provider specified as providerName in the searchInput
        structures. 
        A framework will allow custom solution to be able to provide a new specific provider to collect data, perform
        sorting and filtering.  Such provider can be a User Inbox retriever, or Full Text searcher. The new data
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
        This operation allows user to send the search input, filter values, and sorting data.  These input values will
        then be passed to the fnd0performSearch operation input values, which then use to collect, sort, and filter its
        results.
        The first two input parameters are important.  The first input is provider name.  This is a string to represent
        the type name of RuntimeBusinessObject to which this request should be routed to.  If the template that
        contains the class is not installed, a partial error is returned in the service data. The second input is the
        search input map.  The key will be different per each provider.  For example, for Full Text searcher, the input
        key would be searchString.  For User Inbox retriever, the input key would be Inbox Type.  The fnd0performSearch
        implementation for each provider shall take into account on the key name as it is used to store the values in
        OperationInput object.
        """
        return cls.execute_soa_method(
            method_name='performSearch',
            library='Query',
            service_date='2012_10',
            service_name='Finder',
            params={'searchInput': searchInput},
            response_cls=SearchResponse,
        )
