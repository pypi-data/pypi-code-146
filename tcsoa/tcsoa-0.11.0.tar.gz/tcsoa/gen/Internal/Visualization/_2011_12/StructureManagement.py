from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from tcsoa.gen.Internal.Visualization._2008_06.StructureManagement import ExpandPSRelatedObjectInfo, RelationAndTypesFilter
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandPSData1(TcBaseObj):
    """
     Through this structure, the child BOMLine , the object of the BOMLine and the object attached to the bom line
    object are returned.
    
    :var bomLine: BOMLine object reference of the children
    :var objectOfBOMLine: Object that the child represents
    :var indexOfrelatedObjectsInfo: The index into 'ExpandPSFromOccurrenceListOutput'::relatedObjects array that has the
     information about the related object and relation type.
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    indexOfrelatedObjectsInfo: List[int] = ()


@dataclass
class ExpandPSFromOccurrenceListInfo(TcBaseObj):
    """
    Input structure that defines the occurrences which are to be expanded into the BOM window
    
    :var occurListClientId: Identifier that helps the client track the object(s)
    :var occurrenceChainsByParent:  List of occurrences, each occurrence being a list of strings. If the
    useClientIdAsKey is true
     and when two OccurrenceChainList with same clientId is specified the second OccurrenceChainList  element will not
    be processed if the first OccurrenceChainList resolution is successful.
    """
    occurListClientId: str = ''
    occurrenceChainsByParent: List[OccurrenceChainList] = ()


@dataclass
class ExpandPSFromOccurrenceListOutput(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'OccurrenceListResults'.
    
    :var clientId: Identifier that helps the client track the object(s) created. This is the clientId specified  in the
    'ExpandPSFromOccurrenceListInfo'.
    :var occurrenceList: List of 'OccurrenceListResults' structs describing the occurrences that were expanded
    """
    clientId: str = ''
    occurrenceList: List[OccurrenceListResults] = ()


@dataclass
class ExpandPSFromOccurrenceListPref(TcBaseObj):
    """
    A structure that allows for filtering criteria to be specified.
    
    :var prefKeyValue: A map( key = string, value = string) in which the following preferences can be passed as
    KeyValue pairs
    wantDatasets - true/false , wantSiblings - true/false, wantPathToContextParentLine - true/false
    useClientIdAsKey - true/false, bomExpandExcludeFilter - None/ExcludeICHistory/ExcludeGDEs/ExcludeNonImanItemLines
    
    wantDatasets - When passed  as true  causes the item revision to expand further so that its Datasets can be found.
    
    wantSiblings - When  true expands one level the BOMLines that were expanded using occurrence list to  return the
    siblings.
    
    wantPathToContextParentLine - When true returns the path upto the context BOMLine when the occurrence list is
    expanded using bl_abs_occ_id or bl_absocc_uid_in_topline_context. 
    
    useClientIdAsKey - When true  indicates that the clientId is to be used as an identifier to consider two different
    elements in the occurrence list as same. In a list containing one or more occurrence list elements with same client
    id, if the first element resolves into a valid BOMLine then the rest of the occurrence list with that clientId is
    ignored for processing. This is useful when multiple NGID are recorded in the part in different product context and
    the client sends in all of them to get any of them resolved.
    
    bomExpandExcludeFilter- The filter that is applied when the BOM is expanded to return the sibling
    lines(wantSiblings=true)
    
    :var info: List of the relation name and the Dataset types to return along with the children.If info.size() == 0
    and wantDatasets == true then all dataset types are to be considered.
    """
    prefKeyValue: StringKeyToStringValueMap = None
    info: List[RelationAndTypesFilter] = ()


@dataclass
class ExpandPSFromOccurrenceListResponse(TcBaseObj):
    """
    Response structure for the 'expandPSFromOccurrenceList'() operation.
    
    :var output: List of 'ExpandPSFromOccurrenceListOutput' structures containing the objects corresponding to the
    parent and the child BOMLines,their siblings and their related objects as well.
    :var serviceData: The service data contains the plain objects and the error stack, if any.
    :var relatedObjects: List of objects attached to BOMLine with given relation
    :var childrenOfParent: A map(Key = BOMLine, Value = Array of 'ExpandPSData1') that contains the expanded parent
    BOMLine as the key and 'ExpandPSData1' of its children as value. This is populated only when the wantSiblings is
    true.
    """
    output: List[ExpandPSFromOccurrenceListOutput] = ()
    serviceData: ServiceData = None
    relatedObjects: List[ExpandPSRelatedObjectInfo] = ()
    childrenOfParent: ParentLineToChildrenDataMap = None


@dataclass
class OccurrenceChain(TcBaseObj):
    """
    Input structure that defines a single occurrence uid chain from the topline (but not including topline) to the
    BOMLine that this chains represents.
    
    :var ngidClientId: Identifier that helps the client track the object(s) and helps to identify if two
    OccurrenceChain are same with respect to same parent.
    :var attributeNames: A list of 1 or more attribute names that corresponds to the values that make up the
    occurrenceChainStr
    :var occurrenceChainStr: List of occurrence UIDs that make up the chain of UIDs from the parent BOMLine (but not
    including the parent) down to the last occurrence in the chain
    """
    ngidClientId: str = ''
    attributeNames: List[str] = ()
    occurrenceChainStr: List[str] = ()


@dataclass
class OccurrenceChainList(TcBaseObj):
    """
    Input structure that defines the parent context and a list of occurrence chains to expand within that context.
    
    :var listClientId: Identifier that helps the client track the object(s) and helps to identify if two
    'OccurrenceChainList' are same with differnet NGID.
    :var parentBomLine: Object reference for the parent BOMLine of the occurrences that are described in occurrenceList.
    :var occurrenceList: List of occurrences, each occurrence being a list of strings. The occurrence is described in
    the context of the parent BOMLine. If the useClientIdAsKey is true and when two 'OccurrenceChain' with same
    clientId is specified the second 'OccurrenceChain' element will not be processed if the first 'OccurrenceChain'
    resolution is successful.
    """
    listClientId: str = ''
    parentBomLine: BOMLine = None
    occurrenceList: List[OccurrenceChain] = ()


@dataclass
class OccurrenceChainResult(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'ExpandPSData1' structures for each occurrence in a
    given chain.
    
    :var clientId: Identifier that helps the client track the object(s) created. The client ID that was specified in
    the 
    'OccurrenceChain'.
    :var occurrenceChain: List of 'ExpandPSData1' structs describing the occurrences that were expanded in the given
    'OccurrenceChain'.
    """
    clientId: str = ''
    occurrenceChain: List[ExpandPSData1] = ()


@dataclass
class OccurrenceListResults(TcBaseObj):
    """
    This structure records the parent context and the occurrences expanded in that context.
    
    :var clientId: Identifier that helps the client track the object(s) created. The client ID that was specified in
    the 
    'OccurrenceChainList'.
    :var parent: 'ExpandPSData1' describing the parent BOM
    :var occurrenceList: List of 'OccurrenceChainResult' structs describing the occurrences that were expanded in the
    context of the given parent
    """
    clientId: str = ''
    parent: ExpandPSData1 = None
    occurrenceList: List[OccurrenceChainResult] = ()


"""
List of children for a given parent. This is returned when the wantSiblings is true.If the line is a leaf node then it would be found in the map.
"""
ParentLineToChildrenDataMap = Dict[BOMLine, List[ExpandPSData1]]


"""
This map holds the string value for a given string as key
"""
StringKeyToStringValueMap = Dict[str, str]
