from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    a generic structure to capture additional information.
    - intMap    A map of string to a list of integers. 
    - dblMap    A map of string to a list of doubles. 
    - strMap    A map of string to a list of strings. 
    - objMap    A map of string to a list of business objects.
    - dateMap    A map of string to a list of dates.
    
    
    
    :var intMap: A map (string/list of integers) of generic key to integer values.
    :var dblMap: A map (string/list of doubles) of generic key to double values.
    :var strMap: A map (string/list of strings) of generic key to string values.
    :var objMap: A map (string/list of BusinessObjects) of generic key to  BusinessObject values.
    :var dateMap: A map (string/list of dates) of generic key to date values.
    """
    intMap: StringToIntVectorMap = None
    dblMap: StringToDblVectorMap = None
    strMap: StringtoStrVectorMap = None
    objMap: StringToObjVectorMap = None
    dateMap: StringToDateVectorMap = None


@dataclass
class CreateOrUpdatePreviousEffResp(TcBaseObj):
    """
    CreateOrUpdatePreviousEffResp structure contains a list of AdditionalInfo elements, the size of which matches the
    input element list. It also includes the standard ServiceData object.
    
    :var info: A list of AdditionalInfo structures. The created or updated ConfigurationContext object representing the
    previous effectivity will appear under the objMap key "Effectivity".
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    info: List[AdditionalInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ConnectChangeNoticeToContextInElem(TcBaseObj):
    """
    ConnectChangeNoticeToContextInElem structure contains the details of a single element necessary for associating a
    changeObject ( currently, must be ChangeNoticeRevision) with the optional container ( currently, must be BOMWindow).
    
    :var changeObject: The ChangeNoticeRevision which is to be used to associate with the context. Currently, only
    BOMWindow object is supported for context.
    :var context: A context to which the changeNoticeRevision is to be associated. Currently, if specified must be
    BOMWindow object.
    :var shareMode: The mode to be used for determining how the revisions in the solution folder of the
    ChangeNoticeRevision are to be released. If this optional argument is not empty, it must be one of "Share", "None",
    "Clone", "ShareEffectivityOnly". 
    - Share: share the release status on revisions with the "preferred" release status On ChangeNoticeRevision that is
    a subset of the values given by preference "MEMCN_release_statues".
    - None: no release status on revisions.
    - Clone: new release statuses on revisions cloned from "preferred" release status.
    - ShareEffectivityOnly: new release statues on revisions with same type as the "preferred" release status on
    ChangeNoticeRevision, but with shared effectivity. If specified, will set the "cm0ChangeNoticeRevShareMode" runtime
    property on the BOMWindow.
    
    
    :var info: Currently, not used.
    """
    changeObject: BusinessObject = None
    context: BusinessObject = None
    shareMode: str = ''
    info: AdditionalInfo = None


@dataclass
class PreviousEffectivity(TcBaseObj):
    """
    PreviousEffectivity structure contains the details of a single element necessary for creating or updated a
    ConfigurationContext and associating with the ChangeNoticeRevision.
    
    :var changeObject: The ChangeNoticeRevision which is to be used to associate with the ConfigurationContext created
    representing previous effectivity.
    :var endItem: The Item or ItemRevision that is the endItem of the ConfigurationContext to be associated with
    ChangeNoticeRevision.
    :var unit: The text representing the unit of previous effectivity.
    :var date: The DateTime object representing the date of the previous effectivity.
    :var info: Currently, not used
    """
    changeObject: BusinessObject = None
    endItem: BusinessObject = None
    unit: str = ''
    date: datetime = None
    info: AdditionalInfo = None


@dataclass
class ConnectChangeNoticeToContextResp(TcBaseObj):
    """
    ConnectChangeNoticeToContextResp structure contains a list of AdditionalInfo elements, the size of which matches
    the input element list. It also includes the standard ServiceData object. The created ConfigurationContext object
    will be returned as the value of objMap key "Effectivity".
    
    :var info: Currently, not used. 
    :var serviceData: Service data capturing partial errors using the input array index as client id and any updated
    BOMWindow objects.
    """
    info: AdditionalInfo = None
    serviceData: ServiceData = None


@dataclass
class UpdateChangeNoticeRelationsIn(TcBaseObj):
    """
    UpdateChangeNoticeRelationsIn structure contains the details necessary for managing the secondary ItemRevision
    objects related to the ChangeNoticeRevision, which is associated with a BOMWindow.
    
    :var selectedLines: The selected BOMLine objects whose ItemRevision objects will be added to or removed from the
    ChangeNoticeRevision relations.
    :var action: Indicate if this is adding or removing ItemRevision objects. Current valid values are: "Add" and
    "Remove".
    :var isRecursive: Indicate if the children of the selectedLines will be considered as well. If true, the children
    of the selectedLines will be traversed based on a closure rule specified by preference
    MEMCN_solution_object_collection_rule. Otherwise, only the selectedLines will be considered by the closure rule. 
    :var additionalInfo: An AdditionalInfo structure. Currently, not used.
    """
    selectedLines: List[BusinessObject] = ()
    action: str = ''
    isRecursive: bool = False
    additionalInfo: AdditionalInfo = None


@dataclass
class UpdateChangeNoticeRelationsResp(TcBaseObj):
    """
    UpdateChangeNoticeRelationsResp structure contains a list of AdditionalInfo elements, the size of which matches the
    input element list. It also includes the standard ServiceData object. 
    
    :var info: A list of AdditionalInfo structures. Currently not used.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    info: List[AdditionalInfo] = ()
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
A map of string to vector of strings.
"""
StringtoStrVectorMap = Dict[str, List[str]]
