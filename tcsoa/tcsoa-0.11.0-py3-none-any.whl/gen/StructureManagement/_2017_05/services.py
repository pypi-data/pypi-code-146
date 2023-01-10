from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.StructureManagement._2017_05.StructureSearch import SearchScope, StructureSearchResultResponse, SearchExpressionSet
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def nextSearch2(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        This operation gets the next set of search results, which was initialized by the startSearch2 operation. This
        operation returns the results in batches and needs to be called repeatedly until the flag for search complete
        is true in the response. Input to this operation is the search cursor object which was returned by the
        startSearch2 or a previous call to nextSearch2 operation.
        
        Use cases:
        A user wants to perform structure search within a particular scope. The user needs to select search
        criteria(s), from the supported list to create search expression and start search operation. Once the initial
        set of a search result is returned, this operation will be used to get the next set of search result.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='nextSearch2',
            library='StructureManagement',
            service_date='2017_05',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def startSearch2(cls, scope: SearchScope, searchExpression: SearchExpressionSet, returnLiteLines: bool) -> StructureSearchResultResponse:
        """
        This operation initializes the structure search. The input to the operation is a search expression set and the
        scope to perform the search in.
        
        Use cases:
        A user wants to perform structure search within a particular scope. The user needs to select search criteria(s)
        from the supported list to create search expression and start search operation.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='startSearch2',
            library='StructureManagement',
            service_date='2017_05',
            service_name='StructureSearch',
            params={'scope': scope, 'searchExpression': searchExpression, 'returnLiteLines': returnLiteLines},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def stopSearch2(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        This operation stops the current search identified by the search cursor object. The input to the operation is
        the search cursor object which was returned by the startSearch2 or previous call to nextSearch2 operation.
        
        Use cases:
        A user wants to perform Cacheless search within a particular scope. The user needs to select search criteria(s)
        from the supported list to create search expression and start search operation. Once the initial batch of
        search result is returned, this operation can be used to stop the search.
        """
        return cls.execute_soa_method(
            method_name='stopSearch2',
            library='StructureManagement',
            service_date='2017_05',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )
