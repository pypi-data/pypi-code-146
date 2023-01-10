from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awb0Element
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OccurrenceCursor(TcBaseObj):
    """
    OccurrenceCursor is a cursor that is returned for use in subsequent call to retrieve the next page of configured
    occurrences.
    
    :var startReached: If true, the first page of the results has been reached.
    :var endReached: If true, the last page of the results has been reached.
    :var startIndex: Indicates the Cursor start position for the result occurrences returned so far.
    :var endIndex: Indicates the Cursor end position for the result occurrences returned so far.
    :var pageSize: Indicates the maximum number of occurrences that can be returned in one service call.
    :var startOccUid: Indicates the cursor start object for the result occurrences returned so far. This is used for
    flat mode only.
    :var endOccUid: Indicates the cursor end object for the result occurrences returned so far. This is used for flat
    mode only.
    :var cursorData: The cursor data.
    """
    startReached: bool = False
    endReached: bool = False
    startIndex: int = 0
    endIndex: int = 0
    pageSize: int = 0
    startOccUid: str = ''
    endOccUid: str = ''
    cursorData: List[str] = ()


@dataclass
class OccurrenceInfo6(TcBaseObj):
    """
    OccurrenceInfo6 is the information about occurrence that is part of the configuration result and passing the filter
    critiera.
    
    :var occurrence: Instance of the Awb0Element.
    :var occurrenceId: Session Recoverable UID of the configured occurrence.
    :var stableId: Stable UID of Awb0Element. This  strictly used for maintaining expansion state of nodes in tree view.
    :var displayName: Display name of the configured occurrence.
    :var numberOfChildren: Number of children of the configured occurrence.
    :var underlyingObjectType: Internal name of the underlying object that occurrence presents.
    """
    occurrence: Awb0Element = None
    occurrenceId: str = ''
    stableId: str = ''
    displayName: str = ''
    numberOfChildren: int = 0
    underlyingObjectType: str = ''


@dataclass
class PackedOccurrenceCSIDsResponse(TcBaseObj):
    """
    Represents the response for getPackedOccurrenceCSIDs operation. PackedOccurrenceCSIDsResponse contains the clone
    stable ids of packed occurrences.
    
    :var csids: The clone stable ids for the input packed occurrences.
    :var serviceData: The Service Data.
    """
    csids: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class UserContextInfo(TcBaseObj):
    """
    UserContextInfo contains user's working state information like active page, last saved session time for the opened
    product.
    
    :var autoSavedSessiontime: The auto saved session time for the opened product and the logged in user.
    :var sublocationAttributes: A map (string,list of strings) of client state attribute name/value pairs. The
    following keys are supported: 'awb0ActiveSublocation'. &lsquo;awb0ActiveSublocation&rsquo; refers to name of tabs
    like &lsquo;Overview&rsquo;, &lsquo;Viewer&rsquo;.
    """
    autoSavedSessiontime: datetime = None
    sublocationAttributes: SublocationAttributes2 = None


@dataclass
class FocusOccurrenceInput(TcBaseObj):
    """
    Contains input information required to set the focusChildOccurrence.
    
    :var element: The focus child Business Object for which sibling occurrences are desired. Valid Business Objects
    types are Awb0Element, Cpd0DesignElement, Ptn0Partition.
    :var cloneStableIdChain: Clone stable id of child occurrence in top-down fashion. The chain is separated by "/".
    This field is considered only when focusChildOccurrence is empty.
    """
    element: BusinessObject = None
    cloneStableIdChain: str = ''


"""
Map (string, list of string) of client state attribute name and value pairs. At this time only one (key) attribute name is supported: "activeSublocation". Supported values are: (tab names like) "overview", "viewer" . Keys and values are case in-sensitive.
"""
SublocationAttributes2 = Dict[str, List[str]]
