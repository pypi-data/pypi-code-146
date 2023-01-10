from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanItemBOPLine
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchScopedStructureInputInfo(TcBaseObj):
    """
    A search input consists of list of process line object from BOP structure on which the search is executed, the
    object type to be searched for, the query type of the search, the closure rule to traverse the BOP structure , a
    flag to return the object type which are assigned to the input process line object and a map containing the
    additional information (if required).
    
    :var processScopeForSearch: The list of process line object from BOP structure, which has defined scope from Bill
    of Material (BOM).
    :var objectType: The object type to be searched for. Valid types are: Mfg0BvrWeldPoint, Mfg0BvrArcWeld, Mfg0BvrPLP
    and Mfg0BvrPart.
    :var queryType: The query to search on the input process scope. The valid values are: "Unassigned",
    "ConsumedConnected" and "ConsumedConnectedUnassigned". The "Unassigned" query searches for the unassigned input
    object type in the process scope specified as input. The "ConsumedConnected" query first searches for the assigned
    input object type in the input process scope and then for output objects, it finds out the connected parts. The
    "ConsumedConnectedUnassigned" query first searches for the assigned input object type in the input process scope
    and then for output objects, it finds out the connected parts and filter out unassigned parts.
    :var closureRuleName: The name of the closure rule to be used to traverse the BOP structure.
    :var returnAssignedObjects: If true, the response also returns input object type which are assigned to the input
    process scope.
    :var additionalInfo: A structure containing the maps to capture the additional information.
    1. User can provide the additional scope for the query which is not defined by "Set Scope" operation. The key is
    "AdditionalScope" and the value is list of additional scope from the BOM structure.
    2. User need to search for the objects of specific type which are not part of the BOM scope. The key is
    "OutOfScopeObjects" and the value is the "Object Type".
    """
    processScopeForSearch: List[ImanItemBOPLine] = ()
    objectType: BusinessObject = None
    queryType: str = ''
    closureRuleName: str = ''
    returnAssignedObjects: bool = False
    additionalInfo: AdditionalInfo2 = None


@dataclass
class SearchScopedStructureResponse(TcBaseObj):
    """
    Returns a list of object which is result of search query, a list of object which is part of input process scope but
    not part of BOM scope, a list of objects which is assigned to input process scope and partial errors in the service
    data.
    
    :var queryOutput: A list of object which is result of search query based on the input criteria.
    :var outOfScopeObjects: A list of object which is part of the input process scope from Bill Of Process (BOP)
    structure but not part of the product scope from Bill Of Material (BOM) structure.
    :var assignedObjects: A list of object which is assigned to the input process line object in Bill Of Process (BOP)
    structure. This list is populated only if the logical value of "returnAssignedObjects" in the input is "true".
    :var serviceData: A service data containing partial errors.
    """
    queryOutput: List[BusinessObject] = ()
    outOfScopeObjects: List[BusinessObject] = ()
    assignedObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class AdditionalInfo2(TcBaseObj):
    """
    A structure containing the maps to capture the additional information.
    
    :var strToDateMap: A map(string, list of date) to capture additional information.
    :var strToDoubleMap: A map(string, list of double)  to capture additional information.
    :var strToStrMap: A map(string, list of string)  to capture additional information.
    :var strToIntMap: A map(string, list of integer)  to capture additional information.
    :var strToObjMap: A map(string, list of business object) to capture additional information.
    """
    strToDateMap: StringToDateMap = None
    strToDoubleMap: StringToDoubleMap = None
    strToStrMap: StringToStringMap = None
    strToIntMap: StringToIntegerMap = None
    strToObjMap: StringToObjectMap = None


"""
A map(string, list of date) to capture additional information.
"""
StringToDateMap = Dict[str, List[datetime]]


"""
A map(string, list of double)  to capture additional information.
"""
StringToDoubleMap = Dict[str, List[float]]


"""
A map(string, list of integer)  to capture additional information.
"""
StringToIntegerMap = Dict[str, List[int]]


"""
A map(string, list of business object) to capture additional information.
"""
StringToObjectMap = Dict[str, List[BusinessObject]]


"""
A map(string, list of string)  to capture additional information.
"""
StringToStringMap = Dict[str, List[str]]
