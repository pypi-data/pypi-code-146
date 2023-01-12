from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Awb0Element, Awb0ProductContextInfo, WorkspaceObject
from typing import List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2017_12.OccurrenceManagement import OccurrenceCursor, OccurrenceInfo6
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class OccurrenceSortInput(TcBaseObj):
    """
    OccurrenceSortInput specifies the internal property name and sorting order to sort the occurrences. Sorting order
    can be "ASC" or "DESC".
    
    :var propertyName: Internal property name on which sorting is to be done.
    :var sortingOrder: Order of sorting e.g. "ASC" or "DESC".
    """
    propertyName: str = ''
    sortingOrder: str = ''


@dataclass
class ParentChildrenInfo(TcBaseObj):
    """
    ParentChildrenInfo specifies parent and its children information. The parent and children are associated through
    PSBOMViewRevision and PSOccurrence objects.
    
    :var parentInfo: Information of parent occurrence.
    :var childrenInfo: Information of children occurrences corresponding to parentInfo.
    :var cursor: Cursor that represents point to which the results have been fetched. This field is used for subsequent
    calls.
    """
    parentInfo: OccurrenceInfo6 = None
    childrenInfo: List[OccurrenceInfo6] = ()
    cursor: OccurrenceCursor = None


@dataclass
class RemoveSubstitutesData(TcBaseObj):
    """
    Contains element (BusinessObject) for which input substitute objects (WorkspaceObject) are to be removed.
    
    :var element: The object for which substitute objects are to be removed. Valid types are PartUsage,
    PartBreakdownElement, Awb0DesignElement, Fgb0PartUsage, Fgb0PartUsageLine, Fgb0PartBreakdownElement, etc.
    :var substitutesToBeRemoved: A list of substitutes to be removed. Valid types are : ItemRevision, Bom0Part.
    :var productContextInfo: Business Object of type Awb0ProductContextInfo that contains the product as well as all
    the configuration information.
    """
    element: BusinessObject = None
    substitutesToBeRemoved: List[WorkspaceObject] = ()
    productContextInfo: Awb0ProductContextInfo = None


@dataclass
class AddSubstitutesData(TcBaseObj):
    """
    Contains the element (BusinessObject) and list of substitutes to be added (WorkspaceObject).
    
    :var element: The object for which new substitutes are to be added. Valid types are PartUsage,
    PartBreakdownElement, Awb0DesignElement, Fgb0PartUsage, Fgb0PartUsageLine, Fgb0PartBreakdownElement, etc.
    :var substitutesToBeAdded: A list of objects to be added as substitutes. Valid types are ItemRevision, Bom0Part.
    """
    element: BusinessObject = None
    substitutesToBeAdded: List[WorkspaceObject] = ()


@dataclass
class DefaultName(TcBaseObj):
    """
    Contains the pattern to form the new IDs of the input Awb0Element objects.
    
    :var autogen: If true, IDs generated automatically; otherwise, not.
    :var prefix: The prefix to be attached to the ID. This field is ignored if autogen is true.
    :var suffix: The suffix to be attached to the ID. This field is ignored if autogen is true.
    :var fromString: The string to be replaced by "toString" variable. This field is ignored if autogen is true.
    :var toString: The string which replaces the fromString in the ID of the object. This field is ignored if autogen
    is true.
    """
    autogen: bool = False
    prefix: str = ''
    suffix: str = ''
    fromString: str = ''
    toString: str = ''


@dataclass
class DuplicateAndReplaceData(TcBaseObj):
    """
    Contains all the information needed to duplicate the input structures.
    
    :var productContextInfo: The Awb0ProductContextInfo object containing configuration information.
    :var elements: The selected Awb0Element objects to be duplicated and replaced with new component. The selection can
    be a leaf element or a sub assembly.
    :var defaultName: Contains the pattern to form the new IDs of the input Awb0Element objects.
    :var duplicateFlags: A bitmap for the duplicate flags set.
    1 &ndash; Smart selection using TopLine assigned projects
    2 &ndash; Rename CAD files
    4 &ndash; Return cloned object map information
    8 &ndash; run duplicate in Background mode
    16 &ndash; run duplicate in validate mode.
    """
    productContextInfo: Awb0ProductContextInfo = None
    elements: List[Awb0Element] = ()
    defaultName: DefaultName = None
    duplicateFlags: int = 0
