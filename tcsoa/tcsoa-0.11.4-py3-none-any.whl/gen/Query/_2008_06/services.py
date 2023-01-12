from __future__ import annotations

from typing import List
from tcsoa.gen.Query._2008_06.SavedQuery import QueryInput
from tcsoa.gen.Query._2007_09.SavedQuery import SavedQueriesResponse
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def executeSavedQueries(cls, input: List[QueryInput]) -> SavedQueriesResponse:
        """
        Executes a set of saved queries of following type 
        QRY_RUN_BY_TC ( 0 ),QRY_RUN_BY_USER_QUERY ( 16 ), QRY_RUN_BY_KEYWORD_SEARCH ( 24 ). 
        
        The saved queries can be executed to yield results in 2 modes: 
        - Flat mode: In this traditional execution mode, only the first-level 
        objects (corresponding to the queried class) satisfying the query 
        are returned 
        - Hierarchical/Indented mode: This mode is only applicable for 
        saved queries that allow Hierarchical/Indented results. In this 
        execution mode, the first-level objects as well as any sub-level 
        objects satisfying the query criteria are returned. The hierarchy 
        level information is also returned so that result subsets can be 
        re-constructed using the resulting objects. 
        
        This service will retun the matched object UIDs. 
        
        After fetching UIDs, client need to call DataManagementService.loadObjects operation 
        to load objects by pages. 
        See the QueryInput and QueryResults data structures for 
        usage details.
        """
        return cls.execute_soa_method(
            method_name='executeSavedQueries',
            library='Query',
            service_date='2008_06',
            service_name='SavedQuery',
            params={'input': input},
            response_cls=SavedQueriesResponse,
        )
