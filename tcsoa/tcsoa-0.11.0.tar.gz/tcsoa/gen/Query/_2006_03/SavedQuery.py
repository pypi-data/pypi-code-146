from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanQuery
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExecuteSavedQueryResponse(TcBaseObj):
    """
    Holds the response for ExecuteSavedQuery. The number of objects found is the 
     total number found and may be greater than the number return in the vector of 
     objects if a limit was specified on executing the query.
    
    :var nFound: The number of objects found by the query.
    :var objects: The objects returned.
    :var serviceData: The standard service data which includes the returned objects.
    """
    nFound: int = 0
    objects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class GetSavedQueriesResponse(TcBaseObj):
    """
    Holds the response for GetSavedQueries
    
    :var queries: A list of SavedQueryObjects each of which contains the query, query name, and query description for a
    saved query.
    :var serviceData: Standard ServiceData
    """
    queries: List[SavedQueryObject] = ()
    serviceData: ServiceData = None


@dataclass
class SavedQueryFieldListObject(TcBaseObj):
    """
    A  list of saved query fields for a saved query.
    
    :var fields: Holds one entry per clause
    """
    fields: List[SavedQueryFieldObject] = ()


@dataclass
class SavedQueryFieldObject(TcBaseObj):
    """
    The data for a field of a saved query.
    
    :var attributeName: The attribute name for the clause.
    :var entryName: User entry name for clause.
    :var logicalOperation: Logical operator for clause
    :var mathOperation: Math operator for clause
    :var value: Default value for clause
    :var lov: LOV for the clause
    :var attributeType: Attribute type for clause
    """
    attributeName: str = ''
    entryName: str = ''
    logicalOperation: str = ''
    mathOperation: str = ''
    value: str = ''
    lov: BusinessObject = None
    attributeType: int = 0


@dataclass
class SavedQueryObject(TcBaseObj):
    """
    The data for each saved query found.
    
    :var query: The saved query.
    :var name: The name of the saved query.
    :var description: The description of the saved query.
    """
    query: ImanQuery = None
    name: str = ''
    description: str = ''


@dataclass
class DescribeSavedQueriesResponse(TcBaseObj):
    """
    Holds the field data for each saved query.
    
    :var fieldLists: A list of fields for each input query.
    :var serviceData: The standard ServiceData.
    """
    fieldLists: List[SavedQueryFieldListObject] = ()
    serviceData: ServiceData = None
