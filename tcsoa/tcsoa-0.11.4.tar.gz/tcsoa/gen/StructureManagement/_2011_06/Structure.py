from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, Item, ItemRevision
from tcsoa.gen.StructureManagement._2008_06.Structure import NewItemInfo, DefaultNaming
from enum import Enum
from typing import List
from tcsoa.gen.StructureManagement._2010_09.Structure import ProjectInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandOrUpdateDuplicateItemsOutput2(TcBaseObj):
    """
    The 'ExpandOrUpdateDuplicateItemsOutput2' represents the collection of all related data objects with the structure
    ItemRevision object(s) or part family masters ItemRevision object(s).
    
    :var object: The BOM structure ItemRevision or a part family master ItemRevision.
    :var relatedObjInfo: List of all dependent objects that are related to the object.
    """
    object: ItemRevision = None
    relatedObjInfo: List[RelatedItemsInfo2] = ()


@dataclass
class ExpandOrUpdateDuplicateItemsResponse2(TcBaseObj):
    """
    The 'ExpandOrUpdateDuplicateItemsResponse2' structure represents the results of the structure dependent data search.
    
    :var outputs: List of 'ExpandOrUpdateDuplicateItemsOutput2' which contains information about the BOM structure
    ItemRevision to its related data relationships.
    :var serviceData: The error information will be recorded here.
    """
    outputs: List[ExpandOrUpdateDuplicateItemsOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class RelatedItemsInfo2(TcBaseObj):
    """
    The RelatedItemsInfo represents the dependent data found and how it is related to a structure ItemRevision.
    RelatedItemsInfo also can represent a family table member to a family table master.
    
    :var relObj: An ItemRevision  - it is the related data.
    :var relationshipName: The GRM relationship used to find the related data.
    :var depType: The cad dependency types to use for the operation.
    :var mandatory: Is dependent type mandatory or not - If it is mandatory that cad dependent type will come in
    pre-checked and the user will not be able to de-select it.
    """
    relObj: ItemRevision = None
    relationshipName: str = ''
    depType: DependencyType3 = None
    mandatory: bool = False


@dataclass
class ValidateStructureItemIdsInfo3(TcBaseObj):
    """
    Input to ValidateStructureItemIds3. It contains top BOMLine, structure of oldItemComponent to
    'NewItemInfo'(NewItemId, NewItemName), default naming pattern and list of dependency types specified by the user.
    
    :var topLine: Top BOMLine or the selected BOMLine of the structure or sub structure to be cloned.
    :var clonedIdStructure: Structure of OldItem components to the 'NewItemInfo' struct that contains the proposed New
    ItemId and New ItemName
    :var defaultName: Pattern to form a new ItemId.
    :var options: The list of dependency types.
    :var projects: The list of user defined projects to which the duplicated Item objects will be added.
    """
    topLine: BOMLine = None
    clonedIdStructure: List[DuplicateIdStructure] = ()
    defaultName: DefaultNaming = None
    options: List[DependencyType3] = ()
    projects: ProjectInfo = None


@dataclass
class ValidateStructureItemIdsResponse3(TcBaseObj):
    """
    response from ValidateStructureItemIds, containing Structure of OldItem component, NewItemInfo, list of
    itemrevisions failed validation and Service Data object.
    
    :var clonedIdStructure: Structure of OldItem components to the Structure NewItemInfo that contains the proposed New
    ItemId and New ItemName.
    :var serviceData: 'ServiceData' object.  The error stack will contain those ItemRevision objects that failed
    cloning and the reason.
    """
    clonedIdStructure: List[DuplicateIdStructure] = ()
    serviceData: ServiceData = None


@dataclass
class ClosureRuleVariableInfo(TcBaseObj):
    """
    Contains variable name and value pair where the variable is a part of the ClosureRule. The values are to be
    replaced with variable during ClosureRule evaluation.
    
    :var name: Variable name used in ClosureRule.
    :var value: Value for the variable.
    """
    name: str = ''
    value: str = ''


@dataclass
class DuplicateIdStructure(TcBaseObj):
    """
    Structure of oldItem component and NewItemInfo structure.
    
    :var oldItemComponent: The original Item
    :var newItemInfo: The proposed new ItemId and ItemName
    """
    oldItemComponent: Item = None
    newItemInfo: NewItemInfo = None


@dataclass
class DuplicateInputInfo3(TcBaseObj):
    """
    Input for Duplicate SOA API
    
    :var topLine: The top BOMLine or selected BOMLine of the structure to be cloned.  The user can select a sub
    assembly from the original structure to clone.  This input cannot be NULL.  If it is the duplicate dialog will not
    come up at all.
    :var clonedIdStructure: A structure of oldItem which points to the NewItemInfo.  The newItemInfo is made up of the
    proposed new ItemId and the proposed new ItemName
    :var defaultName: The pattern to form the new ItemId
    :var renameCadFile: Whether to rename the CAD files or not
    :var options: The list of dependency types.  This defines the cad traversal.
    :var projects: The user selected projects to add the duplicated Item objects to
    :var duplicateOption: A bitmap for the duplicate option. 1 means smart selection. It can be used for future
    extension.
    """
    topLine: BOMLine = None
    clonedIdStructure: List[DuplicateIdStructure] = ()
    defaultName: DefaultNaming = None
    renameCadFile: bool = False
    options: List[DependencyType3] = ()
    projects: ProjectInfo = None
    duplicateOption: int = 0


class DependencyType3(Enum):
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


class UnloadType(Enum):
    """
    This is an enum which tells whether the unloaded BOM can be recovered or not.
    """
    unrecoverable = 'unrecoverable'
    recoverable = 'recoverable'
