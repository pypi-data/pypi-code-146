from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanQuery
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class QueryInput(TcBaseObj):
    """
    The information about each Saved Query to be processed is provided 
    by way of the SavedQueryInput data structure.
    
    :var query: The saved query object to be executed.
    :var entries: Names of search criteria relevant to the query object.
    :var values: Values for the criteria.
    :var limitList: A list of objects (optional) against which the search is conducted,
    if the list is empty, search will be conducted against the database.
    :var maxNumToReturn: A specified maximum number of matches to be returned,
    0 means no limit.
    :var resultsType: The type of results expected from this operation:
    0 (top-level objects only),
    1 (top-level objects plus children: Hierarchical/Indented results),
    2 (default value as specified on the query object).
    """
    query: ImanQuery = None
    entries: List[str] = ()
    values: List[str] = ()
    limitList: List[BusinessObject] = ()
    maxNumToReturn: int = 0
    resultsType: int = 0


@dataclass
class QueryResults(TcBaseObj):
    """
    Results of saved query  execution, including hierarchy information in a relation map for Hierarchical/Indented
    execution.  Hierarchical/Indented execution example1: If the query is: Find all Items where the Item Revisions have
    a Specification Dataset with name = "xyz1", then results will be comprised of subsets, each containing: an Item, a
    qualifying Item Revision and a qualifying Dataset. For each result subset, the corresponding entries in the
    relation map would be 0 (for root Item), 1 (for first-level Item Revision), 2 (for second-level Dataset).  
    Hierarchical/Indented execution example2: If the query is: Find all Item Revisions that have a Specification
    Dataset with name = "xyz1" AND Form of type Item Revision Master with user_data_1 = "xyz2", then the results will
    comprise of subsets, each containing: an Item Revision, a qualifying Dataset, a qualifying Form and a qualifying
    Item Revision Master. For each result subset, the corresponding entries in the relation map would be 0 (for root
    Item Revision), 1 (for first-level Dataset), 1 (for first-level Form) and 2 (for second-level Item Revision Master).
    
    :var objectsRelMap: Used only for Hierarchical/Indented execution. An integer array containing the hierarchy level
    information which maps 1-to-1 to the returned list of objects which is ordered as subsets. The integer code in the
    relation map indicates if the corresponding object in the results set is a root object (=0), or a first-level child
    (=1), or a second-level child (=2) and so on. In the case of child levels, the level information is with respect to
    the immediately preceding root object entry in the mapping. The order of returns is relevant.
    :var objectUIDS: The object UIDs returned from the search.
    """
    objectsRelMap: List[int] = ()
    objectUIDS: List[str] = ()


@dataclass
class SavedQueriesResponse(TcBaseObj):
    """
    Contains a list of business objects found as well as the service data returned.
    
    :var arrayOfResults: A set of QueryResults data structures.
    :var serviceData: The service data.
    """
    arrayOfResults: List[QueryResults] = ()
    serviceData: ServiceData = None
