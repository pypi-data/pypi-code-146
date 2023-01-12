from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanQuery
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExecuteSavedQueriesResponse(TcBaseObj):
    """
    Holds the response for executeSavedQueries.
    
    :var arrayOfResults: A set of SavedQueryResults data structures
    :var serviceData: serviceData
    """
    arrayOfResults: List[SavedQueryResults] = ()
    serviceData: ServiceData = None


@dataclass
class RetrieveSearchCriteriaResponse(TcBaseObj):
    """
    Holds a vector of SavedSearchCriteriaInfo and a ServiceData. 
     To be used as a response for operation "retrieveSearchCriteria"
    
    :var output: A vector of SavedSearchCriteriaInfo
    :var serviceData: Standard ServiceData
    """
    output: List[SaveSearchCriteriaInfo] = ()
    serviceData: ServiceData = None


@dataclass
class SaveSearchCriteriaInfo(TcBaseObj):
    """
    Holds the criteria information to be saved or retrieved for a 
    saved search, a collection of which is known as "My Saved Searches". 
    A saved search stores the user's entries for a particular saved query 
    execution so that it can be recalled and rerun in the future.
    
    :var searchName: A unique name for the saved search
    :var queryName: The name of the saved query associated with the saved search
    :var keys: Unique keys associated with the "values" below - each key represents a criteria field
    :var values: The values associated with the "keys" above
    :var resultsType: The results type associated with the saved search
    :var virtualFolderPath: The virtual folder the saved search belongs to
    """
    searchName: str = ''
    queryName: str = ''
    keys: List[str] = ()
    values: List[str] = ()
    resultsType: str = ''
    virtualFolderPath: str = ''


@dataclass
class SavedQueryInput(TcBaseObj):
    """
    The information about each Saved Query to be processed is provided 
    by way of the SavedQueryInput data structure.
    
    :var query: The saved query object to be executed.
    :var entries: Names of search criteria relevant to the query object.
    :var values: Values for the criteria.
    :var limitList: A list of objects (optional) against which the search is conducted,
    if the list is empty, search will be conducted against the database.
    :var limitListCount: The size of the limitList.
    :var maxNumToReturn: A specified maximum number of matches to be returned,
    0 means no limit.
    :var resultsType: The type of results expected from this operation:
    0 (top-level objects only),
    1 (top-level objects plus children: Hierarchical/Indented results),
    2 (default value as specified on the query object).
    :var maxNumToInflate: The number of objects in the returned result that must 
    include properties:
    (-1)(all),
    n (any positive integer less than or equal to the maxNumToReturn).
    """
    query: ImanQuery = None
    entries: List[str] = ()
    values: List[str] = ()
    limitList: List[BusinessObject] = ()
    limitListCount: int = 0
    maxNumToReturn: int = 0
    resultsType: int = 0
    maxNumToInflate: int = 0


@dataclass
class SavedQueryResults(TcBaseObj):
    """
    Results of Saved Query execution, number of objects returned and hierarchy information in a relation map for
    Hierarchical/Indented execution.  Hierarchical/Indented execution example1: If the query is: Find all Items where
    the Item Revisions have a Specification Dataset with name = "xyz1", then results will be comprised of subsets, each
    containing: an Item, a qualifying Item Revision and a qualifying Dataset. For each result subset, the corresponding
    entries in the relation map would be 0 (for root Item), 1 (for first-level Item Revision), 2 (for second-level
    Dataset).   Hierarchical/Indented execution example2: If the query is: Find all Item Revisions that have a
    Specification Dataset with name = "xyz1" AND Form of type Item Revision Master with user_data_1 = "xyz2", then the
    results will comprise of subsets, each containing: an Item Revision, a qualifying Dataset, a qualifying Form and a
    qualifying Item Revision Master. For each result subset, the corresponding entries in the relation map would be 0
    (for root Item Revision), 1 (for first-level Dataset), 1 (for first-level Form) and 2 (for second-level Item
    Revision Master).
    
    :var numOfObjects: The number of objects returned.
    :var objectsRelMap: Used only for Hierarchical/Indented execution. An integer array containing the hierarchy level
    information which maps 1-to-1 to the the returned list of objects which is ordered as subsets. The integer code in
    the relation map indicates if the corresponding object in the results set is a root object (=0), or a first-level
    child (=1), or a second-level child (=2) and so on. In the case of child levels, the level information is with
    respect to the immediately preceding root object entry in the mapping. The order of returns is relevant.
    :var objects: The objects returned from the search.
    """
    numOfObjects: int = 0
    objectsRelMap: List[int] = ()
    objects: List[BusinessObject] = ()
