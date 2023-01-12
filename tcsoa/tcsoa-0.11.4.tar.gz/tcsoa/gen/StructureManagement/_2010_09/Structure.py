from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, TC_Project
from tcsoa.gen.StructureManagement._2008_06.Structure import DefaultNaming
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NewItemInfo2(TcBaseObj):
    """
    The proposed new ItemIds and new ItemNames.
    
    :var newItemId: The proposed new ItemId
    :var newItemName: The proposed new ItemName
    """
    newItemId: str = ''
    newItemName: str = ''


@dataclass
class ProjectInfo(TcBaseObj):
    """
    Project Information for Structure Clone
    
    :var assign: Flag that indicates if assigning projects
    :var validate: Flag that indicates if project needs validation
    :var projects: Vector of user selected projects
    """
    assign: bool = False
    validate: bool = False
    projects: List[TC_Project] = ()


@dataclass
class ValidateStructureItemIdsInfo2(TcBaseObj):
    """
    Input to ValidateStructureItemIds2. It contains the top BOMLine, map of oldItemId to NewItemInfo(NewItemId,
    NewItemName), default naming pattern and list of dependency types specified by the user.
    
    :var topLine: Top BOMLine or the selected bom line of the structure or sub structure to be cloned.
    :var inputMap: Map of OldItemIDs to  NewItemInfo2 that contains the proposed New ItemId and New ItemName.
    :var defaultName: Pattern to form a new ItemId.
    :var projects: List of user defined projects to which the duplicated Item objects will be added.
    :var options: List of dependency types.
    """
    topLine: BOMLine = None
    inputMap: DuplicateIdMap2 = None
    defaultName: DefaultNaming = None
    projects: ProjectInfo = None
    options: List[DependencyType2] = ()


@dataclass
class ValidateStructureItemIdsResponse2(TcBaseObj):
    """
    The response from ValidateStructureItemIds, containing a map of OldItemID to 'NewItemInfo', list of ItemRevision
    objects failed validation and a 'ServiceData' object.
    
    :var clonedIdMap: Map of OldItemID to 'NewItemInfo' that contains the proposed New ItemId and New ItemName
    :var serviceData: 'ServiceData' object.  The error stack will contain those ItemRevision objects that failed
    cloning and the reason.
    """
    clonedIdMap: DuplicateIdMap2 = None
    serviceData: ServiceData = None


@dataclass
class DuplicateInputInfo2(TcBaseObj):
    """
    Input for Duplicate2 SOA API
    
    :var topLine: The top BOMLine or selected BOMLine of the structure to be cloned.  The user can select a sub
    assembly from the original structure to clone.  This input cannot be NULL.  If it is the duplicate dialog will not
    come up at all.
    :var duplicateIdMap: A map of oldItemId and NewItemInfo structure. The newItemInfo is made up of the proposed new
    ItemId and the proposed new ItemName
    :var defaultName: The pattern to form a new ItemId
    :var projects: The user selected projects to add the duplicated Item objects to
    :var renameCadFile: Whether to rename the cad files or not
    :var options: The list of dependency types.  This defines the cad traversal.
    :var duplicateOption:  A bitmap for duplicate option. 1 means smart selection.
    """
    topLine: BOMLine = None
    duplicateIdMap: DuplicateIdMap2 = None
    defaultName: DefaultNaming = None
    projects: ProjectInfo = None
    renameCadFile: bool = False
    options: List[DependencyType2] = ()
    duplicateOption: int = 0


class DependencyType2(Enum):
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
OldItemIds mapped to the NewItemInfo2 structure.
"""
DuplicateIdMap2 = Dict[str, NewItemInfo2]
