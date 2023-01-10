from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, Awb0ProductContextInfo, Awb0SavedBookmark
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class BOMLineSelectionPath(TcBaseObj):
    """
    This is the ordered list of BOMLines that represents the selection path from the first level child to the selected
    BOMLine.
    
    :var selectionPath: An ordered list of BOMLines that represents the selection path from the first level child (the
    first index in the list) to the selected BOMLine (the last index in the list).  The top level is not included.
    """
    selectionPath: List[BOMLine] = ()


@dataclass
class ProductContextBOMWindowResponse(TcBaseObj):
    """
    This is the response for the createBOMWindowsFromContexts operation that creates BOMWindow objects from
    Awb0ProductContextInfo objects.
    
    :var bomWindowsAndSelections: A map (Awb0ProductContextInfo/BOMWindowAndSelections) of the input
    Awb0ProductContextInfo objects to the BOMWindowAndSelections objects created from the Awb0ProductContextInfo.
    :var serviceData: The SOA framework object containing objects that were created by the operation and error
    information.
    """
    bomWindowsAndSelections: ProductContextInfoBOMWindowMap = None
    serviceData: ServiceData = None


@dataclass
class BOMWindowAndSelections(TcBaseObj):
    """
    This is the container for a BOMWindow and the list of selected BOMLineSelectionPaths for the BOMLines on the
    BOMWindow.
    
    :var bomWindow: The BOMWindow object created from an Awb0SavedBookmark or Awb0ProductContextInfo.
    :var selections: A list of BOMLineSelectionPaths for the selected BOMLines on the BOMWindow.
    """
    bomWindow: BOMWindow = None
    selections: List[BOMLineSelectionPath] = ()


@dataclass
class SavedBookmarksBOMWindowsResponse(TcBaseObj):
    """
    This is the response for the createBOMWindowsFromBookmarks operation that creates BOMWindow objects from
    Awb0ProductSavedBookmark objects.
    
    :var bomWindowsAndSelections: A map (Awb0SavedBookmark/list of BOMWindowAndSelections objects)  of the input
    Awb0SavedBookmark objects to the list of BOMWindowAndSelections object that contains the BOMWindow and selected
    BOMLines created from the Awb0SavedBookmark.  Each saved Awb0SavedBookmark may contain muliple products, and each
    product will cause a unique BOMWindowAndSelections object to be created.  A list of BOMWindowAndSelections objects
    is supplied for each Awb0SavedBookmark.
    :var serviceData: The SOA framework object containing objects that were created by the operation and error
    information.
    """
    bomWindowsAndSelections: SavedBookmarkBOMWindowsMap = None
    serviceData: ServiceData = None


"""
A map of Awb0SavedBookmark objects to a list of BOMWindowAndSelections objects (Awb0SavedBookmark, list of BOMWindowAndSelections objects).
"""
SavedBookmarkBOMWindowsMap = Dict[Awb0SavedBookmark, List[BOMWindowAndSelections]]


"""
A map of Awb0ProductContextInfo objects to BOMWindowAndSelections objects (Awb0ProductContextInfo, BOMWindowAndSelections).
"""
ProductContextInfoBOMWindowMap = Dict[Awb0ProductContextInfo, BOMWindowAndSelections]
