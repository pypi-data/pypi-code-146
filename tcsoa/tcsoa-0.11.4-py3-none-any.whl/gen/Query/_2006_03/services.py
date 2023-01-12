from __future__ import annotations

from tcsoa.gen.Query._2006_03.SavedQuery import DescribeSavedQueriesResponse, GetSavedQueriesResponse, ExecuteSavedQueryResponse
from tcsoa.gen.BusinessObjects import ImanQuery
from typing import List
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def getSavedQueries(cls) -> GetSavedQueriesResponse:
        """
        Gets a list of all saved queries with query, query name, and query description information.
        
        Use cases:
        The user can open the search view and can select a query from the Change Search dialog which shows all
        available saved queries.
        The user can open the Query Builder to load all the saved queries, and then do the modification, deletion, and
        creation.
        """
        return cls.execute_soa_method(
            method_name='getSavedQueries',
            library='Query',
            service_date='2006_03',
            service_name='SavedQuery',
            params={},
            response_cls=GetSavedQueriesResponse,
        )

    @classmethod
    def describeSavedQueries(cls, queries: List[ImanQuery]) -> DescribeSavedQueriesResponse:
        """
        Returns the description of each of the input saved queries.The description for each query includes all the
        clause information (the attribute name, entry name, operation for each clause, the math operation for each
        clause, the ListOfValues for related clause if it has, and the attribute type).
        
        Use cases:
        User can get the description for queries by this service and then can show the details in search view so that
        user can execute the query.
        
        User can get the description for queries by this service and then show the details in query builder so that
        user can see the definition for the query or update the query.
        
        User can get the description for queries by this service and then use it to get the saved searches.
        
        User can get the description for queries by this service and then use it to get the search history.
        """
        return cls.execute_soa_method(
            method_name='describeSavedQueries',
            library='Query',
            service_date='2006_03',
            service_name='SavedQuery',
            params={'queries': queries},
            response_cls=DescribeSavedQueriesResponse,
        )

    @classmethod
    def executeSavedQuery(cls, query: ImanQuery, entries: List[str], values: List[str], limit: int) -> ExecuteSavedQueryResponse:
        """
        Executes a single saved query by input query with entries and values. If the returned result number is larger
        than the input limit(when limit > 0), then only the input limit result number objects will be returned;
        otherwise all results will be returned. The number of objects found is also returned; it may be larger than the
        limit number.
        
        Use cases:
        The user opens the search view, selects a query from the system defined queries or user defined queries, then
        fills in some input criteria, clicks the Execute button to run this query. The result objects will be returned
        in the search result view. If the total result objects number is larger than the limit number which is used to
        prevent loading too many objects in memory considering the performance issue(when limit > 0), then only return
        the limit number result objects for the query. The total search result objects number is displayed in the
        search result view.
        """
        return cls.execute_soa_method(
            method_name='executeSavedQuery',
            library='Query',
            service_date='2006_03',
            service_name='SavedQuery',
            params={'query': query, 'entries': entries, 'values': values, 'limit': limit},
            response_cls=ExecuteSavedQueryResponse,
        )
