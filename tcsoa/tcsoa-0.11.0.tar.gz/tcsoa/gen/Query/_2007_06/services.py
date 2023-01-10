from __future__ import annotations

from tcsoa.gen.Query._2007_06.SavedQuery import RetrieveSearchCriteriaResponse, SavedQueryInput, ExecuteSavedQueriesResponse, SaveSearchCriteriaInfo
from tcsoa.gen.Query._2007_06.Finder import FindWorkspaceObjectsResponse, WSOFindSet
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SavedQueryService(TcService):

    @classmethod
    def retrieveSearchCriteria(cls, searchNames: List[str]) -> RetrieveSearchCriteriaResponse:
        """
        Retrieve the corresponding search criteria for the given saved search names.
        """
        return cls.execute_soa_method(
            method_name='retrieveSearchCriteria',
            library='Query',
            service_date='2007_06',
            service_name='SavedQuery',
            params={'searchNames': searchNames},
            response_cls=RetrieveSearchCriteriaResponse,
        )

    @classmethod
    def saveSearchCriteria(cls, searchCriteria: List[SaveSearchCriteriaInfo]) -> ServiceData:
        """
        Save a set of search criteria.  Each search criteria pertains to 
         a saved search, a collection of which is known as "My Saved Searches".
        """
        return cls.execute_soa_method(
            method_name='saveSearchCriteria',
            library='Query',
            service_date='2007_06',
            service_name='SavedQuery',
            params={'searchCriteria': searchCriteria},
            response_cls=ServiceData,
        )

    @classmethod
    def executeSavedQueries(cls, input: List[SavedQueryInput]) -> ExecuteSavedQueriesResponse:
        """
        Executes a set of saved queries of following type:
        
        - QRY_RUN_BY_TC ( 0 )
        - QRY_RUN_BY_USER_EXIT ( 8 )
        - QRY_RUN_BY_KEYWORD_SEARCH ( 24 )
        - QRY_RUN_BY_EINT_EXIT ( 32 )
        - QRY_RUN_BY_TC_PLUS_PROCESS ( 56 )
        
        
          
        The saved queries can be executed to yield results in 2 modes:
        
        - Flat mode: In this traditional execution mode, only the first-level  objects (corresponding to         the
        queried class) satisfying the query  are returned
        - Hierarchical/Indented mode: This mode is only applicable for saved queries that allow        
        Hierarchical/Indented results. In this execution mode, the first-level objects as well as any         sub-level
        objects satisfying the query criteria are returned. The hierarchy level information is         also returned so
        that result subsets can be  re-constructed using the resulting objects. 
        
        
                 This service will return the matched object UIDs.   After fetching UIDs, client needs to call        
        DataManagementService.loadObjects operation to load objects by pages.  See the         QueryInput and
        QueryResults data structures for usage details.
        
        Use cases:
        Execute a set of saved queries of following types: QRY_RUN_BY_TC,  QRY_RUN_BY_KEYWORD_SEARCH and
        QRY_RUN_BY_TC_PLUS_PROCESS etc.
        """
        return cls.execute_soa_method(
            method_name='executeSavedQueries',
            library='Query',
            service_date='2007_06',
            service_name='SavedQuery',
            params={'input': input},
            response_cls=ExecuteSavedQueriesResponse,
        )


class FinderService(TcService):

    @classmethod
    def findWorkspaceObjects(cls, findList: List[WSOFindSet]) -> FindWorkspaceObjectsResponse:
        """
        Query the database for WorkspaceObjects. A collection of WSOFindSets are used to do the queries. For each
        WSOFindSet , a FindWorkspaceObjectsOutput will be generated if any WorkspaceObjects are found that meet all the
        criteria.  Each FindWorkspaceObjectsOutput will contain the tags of the WorkspaceObjects that meet all the
        criteria and the index of the WSOFindSet in the findList that generated the output.  If an error is
        encountered, then no FindWorkspaceObjectsOutput will be generated for that WSOFindSet (no partial data
        returned) and the index for the WSOFindSet in the findList will be the client ID in the partial error.  If no
        WSOFindSet generates any output, a null outputList is returned.
        
        Use cases:
        Find workspace object using basic attributes such as object type, object name, owner, group, created before,
        created after etc.
        """
        return cls.execute_soa_method(
            method_name='findWorkspaceObjects',
            library='Query',
            service_date='2007_06',
            service_name='Finder',
            params={'findList': findList},
            response_cls=FindWorkspaceObjectsResponse,
        )
