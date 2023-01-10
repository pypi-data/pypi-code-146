from __future__ import annotations

from tcsoa.gen.StructureManagement._2008_05.StructureVerification import BOMLinePair, AlignmentCheckResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.StructureManagement._2008_05.StructureSearch import SearchScope, StructureSearchResultResponse, SearchExpressionSet
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def nextSearch(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        This operation gets the next set of search results, which was initialized by the 'startSearch' operation. This
        operation returns the results in batches and needs to be called repeatedly until the flag for search complete
        is true in the response. Input to this operation is the search cursor object which was returned by the
        'startSearch' or a previous call to 'nexSearch' operation.
        
        Use cases:
        A user wants to perform structure search within a particular scope. The user needs to select search
        criteria(s), from the supported list to create search expression and start search operation. Once the initial
        set of a search result is returned, this operation will be used to get the next set of search result.
        
        Exceptions:
        >None
        """
        return cls.execute_soa_method(
            method_name='nextSearch',
            library='StructureManagement',
            service_date='2008_05',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def startSearch(cls, scope: SearchScope, searchExpression: SearchExpressionSet) -> StructureSearchResultResponse:
        """
        Start searching a structure for a given search expression within the scope specified
        """
        return cls.execute_soa_method(
            method_name='startSearch',
            library='StructureManagement',
            service_date='2008_05',
            service_name='StructureSearch',
            params={'scope': scope, 'searchExpression': searchExpression},
            response_cls=StructureSearchResultResponse,
        )

    @classmethod
    def stopSearch(cls, searchCursor: BusinessObject) -> StructureSearchResultResponse:
        """
        This operation stops the current search identified by the search cursor object. The input to the operation is
        the search cursor object which was returned by the 'startSearch' or previous call to 'nextSearch' operation.
        
        Use cases:
        A user wants to perform Cacheless search within a particular scope. The user needs to select  search
        criteria(s) from the supported list to create search expression and start search operation. Once the initial
        batch of search result is returned, this operation can be used to stop the search.
        
        Exceptions:
        >Invalid SearchCursor object is passed in input.
        """
        return cls.execute_soa_method(
            method_name='stopSearch',
            library='StructureManagement',
            service_date='2008_05',
            service_name='StructureSearch',
            params={'searchCursor': searchCursor},
            response_cls=StructureSearchResultResponse,
        )


class StructureVerificationService(TcService):

    @classmethod
    def checkAlignment(cls, input: List[BOMLinePair]) -> AlignmentCheckResponse:
        """
        An alignment connects two occurrences that are to be considered equivalent. They are referred
        to as source and target. An alignment can connect one source
        to multiple targets. Alignment can be used to transfer data from source to target.
        An alignment check is used to determine if the source and target of an alignment have matching data.
        """
        return cls.execute_soa_method(
            method_name='checkAlignment',
            library='StructureManagement',
            service_date='2008_05',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=AlignmentCheckResponse,
        )
