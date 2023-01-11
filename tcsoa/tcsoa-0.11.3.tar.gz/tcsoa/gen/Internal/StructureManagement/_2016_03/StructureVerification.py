from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindMatchingCandidatesResp(TcBaseObj):
    """
    FindMatchingCandidatesResp structures contains a list of MatchingCandidateElems capturing the matching pairs of
    source BOMLine objects and target BOMLine objects, and serviceData to return partial errors. The size of the list
    of MatchingCandidateElems will be the same as the size of input list to findMatchingCandidates operation.
    
    :var matchedCandidates: A list of MatchingCandidateElems element.
    :var serviceData: Service data capturing partial errors.
    """
    matchedCandidates: List[MatchingCandidateElems] = ()
    serviceData: ServiceData = None


@dataclass
class MatchingCandidateElemForSingleObj(TcBaseObj):
    """
    A structure representing response for each BOMLine object in the source BOMLine objects in input.
    
    :var objectToSearchFor: The BOMLine object for which equivalent target BOMLine objects were requested.
    :var matchingCandidates: The list of target objects matching the source object.
    :var howMatched: A string providing details of how the target match was found. This is for future and will be empty
    in current implementation.
    """
    objectToSearchFor: BusinessObject = None
    matchingCandidates: List[BusinessObject] = ()
    howMatched: List[str] = ()


@dataclass
class MatchingCandidateElems(TcBaseObj):
    """
    A list of MatchingCandidateElemForSingleObj elements used to group them per input element - MatchingCandidateElem
    
    :var matches: A list of MatchingCandidateElemForSingleObj elements.
    """
    matches: List[MatchingCandidateElemForSingleObj] = ()


@dataclass
class SearchCandidateElems(TcBaseObj):
    """
    A structure to capture the details of searching for matched targetlines for given source lines. If both
    searchCandidates and scopesToSearchIn are specified, the searchCandidates will take priority. Typically, only one
    of either searchCandidates or scopesToSearchIn will be specified.
    
    :var objectsToSearchFor: The list of source objects for which target candidates need to be found.
    :var searchCandidates: The list of target objects from which the matching candidates are to be found.
    :var scopesToSearchIn: The list of target scope elements to be used for finding matching candidates.
    """
    objectsToSearchFor: List[BusinessObject] = ()
    searchCandidates: List[BusinessObject] = ()
    scopesToSearchIn: List[TargetScopeElem] = ()


@dataclass
class TargetScopeElem(TcBaseObj):
    """
    A structure representing the scopes and the closure rule to collect possible candidates for alignment with source
    lines. If the closure rule is empty, it is assumed that all children under the scopes are to be used for finding
    candidates.
    
    :var scopes: A list of objects to be used as scopes for searching for suitable candidate lines.
    :var closureRule: Name of closure rule to be used for collecting all possible below the scopes.
    """
    scopes: List[BusinessObject] = ()
    closureRule: str = ''


@dataclass
class AdditionalData(TcBaseObj):
    """
    A structure to capture addition information in a generic manner.
    
    :var intMap: map of string to vector or integers.
    :var dblMap: map of string to vector of doubles.
    :var strMap: map of string to vector of strings.
    :var objMap: map of string to vector of objects.
    :var dateMap: map of string to vector of dates
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringToStrVectorMap = None
    objMap: StringToObjVectorMap = None
    dateMap: StringToDateVectorMap = None


@dataclass
class AlignMatchedCandidateElem(TcBaseObj):
    """
    A structure to capture the information necessary to align matching target BOMLine objects.
    
    :var sourceObject: The Engineering BOMLine object.
    :var targetObject: The Manufacturing BOMLine object to be synced or replaced by the Engineering BOMLine objects'
    item.
    :var alignAction: The specific action to take for alignment. Possible values are: empty  "" -just align the two
    BOMLine objects ( sync bl_abs_occ_id property ), "replace" - the manufacturing BOMLine object is to be replaced
    with the Engineering BOMLine object. "propagate" - propagate the property values from sourceObject to targetObject.
    Any other custom values are passed to custom handlers registered against user_exit - USER_BOMLine_repair_bomlines.
    """
    sourceObject: BusinessObject = None
    targetObject: BusinessObject = None
    alignAction: str = ''


@dataclass
class AlignMatchedCandidatesResp(TcBaseObj):
    """
    AlignMatchedCandidatesResp structure contains a generic additionalInfo structure and serviceData to return partial
    errors. Currently, the additionalInfo is unused.
    
    :var additionalInfo: A generic structure of type AdditionalData containing keys and list of values (integer,
    double, object, string, date types) for passing additional metadata. Currently this is not used.
    :var serviceData: Service data capturing partial errors.
    """
    additionalInfo: AdditionalData = None
    serviceData: ServiceData = None


"""
a map of string to vector of dates
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
String to vector of doubles map.
"""
StringToDblVectorMap = Dict[str, List[float]]


"""
map of string to vector of integers.
"""
StringToIntVectorMap = Dict[str, List[int]]


"""
a map of string to vector of objects.
"""
StringToObjVectorMap = Dict[str, List[BusinessObject]]


"""
a map of String to vector of strings.
"""
StringToStrVectorMap = Dict[str, List[str]]
