from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandOrUpdateDuplicateItemsInfo(TcBaseObj):
    """
    The 'ExpandOrUpdateDuplicateItemsInfo' contains the BOMLine objects, list of ItemRevision objects and list of
    Dependency types.
    
    :var bomline: If it is not null, expand it and get its dependencies based on the depTypes.  The BOMLine can be any
    line in the structure that the user picks for expansion.
    :var itemRevs: The ItemRevision objects to perform search dependencies on. If empty, the ItemRevision objects to be
    used will be from the expansion of the BOMLine.
    :var depTypes: The dependency types to use for the operation.
    """
    bomline: BOMLine = None
    itemRevs: List[ItemRevision] = ()
    depTypes: List[DependencyType] = ()


@dataclass
class ExpandOrUpdateDuplicateItemsOutput(TcBaseObj):
    """
    The 'ExpandOrUpdateDuplicateItemsOutput' represents the collection of all related data objects with the structure
    ItemRevision object(s) or part family masters ItemRevision object(s).
    
    :var object: The BOM structure ItemRevision.
    :var relatedObjInfo: List of all dependent objects that are related to the object.
    """
    object: ItemRevision = None
    relatedObjInfo: List[RelatedItemsInfo] = ()


@dataclass
class ExpandOrUpdateDuplicateItemsResponse(TcBaseObj):
    """
    The 'ExpandOrUpdateDuplicateItemsResponse' structure represents the the results of the structure dependent data
    search.
    
    :var outputs: List of 'ExpandOrUpdateDuplicateItemsOutput' which contains information about the BOM structure
    ItemRevision to its related data relationships.
    :var serviceData: The error information will be recorded here.
    """
    outputs: List[ExpandOrUpdateDuplicateItemsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class NewItemInfo(TcBaseObj):
    """
    The proposed new ItemIds and new ItemNames.
    
    :var newItemId: The proposed new ItemId.
    :var newItemName: The proposed new ItemName.
    """
    newItemId: str = ''
    newItemName: str = ''


@dataclass
class RelatedItemsInfo(TcBaseObj):
    """
    The RelatedItemsInfo represents the dependent data found and how it is related to a structure ItemRevision.
    RelatedItemsInfo also can represent a family table member to a family table master.
    
    :var relObj: An ItemRevision  - it is the related data.
    :var relationshipName: The GRM relationship used to find the related data.
    :var depType: The cad dependency types to use for the operation.
    """
    relObj: ItemRevision = None
    relationshipName: str = ''
    depType: DependencyType = None


@dataclass
class ValidateStructureItemIdsInfo(TcBaseObj):
    """
    Input to ValidateStructureItemIds. It contains top BOM line, map of oldItemId to NewItemInfo(NewItemId,
    NewItemName), default naming pattern and list of dependency types specified by the user.
    
    :var topLine: Top BOMLine of the structure to be cloned.
    :var inputMap: Map of oldItemId and NewItemInfo structure.
    :var defaultName: The pattern to form new ItemIds.
    :var options: A list of dependency types.
    """
    topLine: BOMLine = None
    inputMap: DuplicateIdMap = None
    defaultName: DefaultNaming = None
    options: List[DependencyType] = ()


@dataclass
class ValidateStructureItemIdsResponse(TcBaseObj):
    """
    Response from 'ValidateStructureItemIds', containing map of OldItemID to 'NewItemInfo', list of ItemRevision
    objects that failed validation and the 'ServiceData' object.
    
    :var clonedIdMap: A map of OldItemID to NewItemInfo that contains the proposed New ItemId and New ItemName.
    :var serviceData: 'ServiceData' object.  The error stack will contain those ItemRevision objects that failed
    cloning and the reason.
    """
    clonedIdMap: DuplicateIdMap = None
    serviceData: ServiceData = None


@dataclass
class DefaultNaming(TcBaseObj):
    """
    prefix/suffix/replace-with/autoAssign to form new Item IDs.
    
    :var autogen: auto assign new item IDs.
    :var prefix: substring to be prefixed to the old item ID to form a new item ID.
    :var suffix: substring to be sufficed to the old item ID to form a new item ID.
    :var from: substring to be replaced from the old item ID by another substring to form a new item ID.
    :var to: substring to replace with a substring from the old item ID to form a new item ID.
    """
    autogen: bool = False
    prefix: str = ''
    suffix: str = ''
    from_: str = ''
    to: str = ''


@dataclass
class DuplicateInputInfo(TcBaseObj):
    """
    Input for Duplicate SOA API
    
    :var topLine: The top BOMLine of the structure to be cloned.
    :var clonedIdMap: A map of oldItemId and NewItemInfo structure.  The newItemInfo is made up of the proposed new
    ItemId and the proposed new ItemName.
    :var defaultName: A pattern to form a new ItemId.
    :var renameCadFile: Whether to rename the CAD files or not.
    :var options: A list of dependency types. This defines the cad traversal.
    """
    topLine: BOMLine = None
    clonedIdMap: DuplicateIdMap = None
    defaultName: DefaultNaming = None
    renameCadFile: bool = False
    options: List[DependencyType] = ()


@dataclass
class DuplicateResponse(TcBaseObj):
    """
    response from the Duplicate SOA.
    
    :var clonedItemRev: Top ItemRevision of the Cloned structure.
    :var serviceData: 'ServiceData' object - The service data object consists of the   top ItemRevision of the cloned
    structure.  The error stack will contain those ItemRevision objects that failed cloning and the reason.  Those
    ItemRevision objects that fail to get cloned are referenced.
    """
    clonedItemRev: ItemRevision = None
    serviceData: ServiceData = None


class DependencyType(Enum):
    """
    Dependency Types
    """
    NoDep = 'NoDep'
    Drawing = 'Drawing'
    PartFamilyMaster = 'PartFamilyMaster'
    PartFamilyMember = 'PartFamilyMember'
    Required = 'Required'
    AllDep = 'AllDep'
    ExcludeFromBom = 'ExcludeFromBom'


"""
OldItemIds mapped to the NewItemInfo structure.
"""
DuplicateIdMap = Dict[str, NewItemInfo]
