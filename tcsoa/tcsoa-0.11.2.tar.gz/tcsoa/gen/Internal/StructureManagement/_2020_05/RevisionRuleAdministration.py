from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RevRuleEntryInfo(TcBaseObj):
    """
    Structure representing an entry\clause in a Revision Rule.
    
    :var entryType: Indicates type of the entry inside RevisionRule.A RevisionRule is made up of a sequential list of
    entries. Evaluation of the rule involves evaluating each of the entries, in order, until a configured revision of
    the Item is successfully obtained. A rule is made up of entries of the following types.
    0 - Working
    1 - Status
    2 - Override
    3 - Date
    4 - Unit No.
    5 - Group
    6 - Precise
    7 - Latest
    8 - End Item
    9 - GroupByItemType
    10 &amp;ndash; Branch.
    :var displayText: Display text of the entry.
    :var revRuleEntryKeyToValue: A map (string, string) pairs of entry name and its value. For example: 1: For entry
    type Working, the map will contain "user", and "group" as keys and UIDs of User and Group as values respectively.
    2: For entry type Status, the map will contain "status_type" as key and UID of attached status i.e TaskType as
    value. 3: For entry type Override, the map will contain "folder" as key and UID of Folder as value.
    :var groupEntryInfo: Information about group entry.This structure is populated only in case of entry type is any of
    the supported group type entries.i.e. CFMGroupEntry, CFMGroupItemTypeEntry and Fnd0CFMGroupOccTypeEntry.
    """
    entryType: int = 0
    displayText: str = ''
    revRuleEntryKeyToValue: MapOfRevRuleEntryKeyToValue = None
    groupEntryInfo: RevRuleGroupEntryInfo = None


@dataclass
class RevRuleGroupEntryInfo(TcBaseObj):
    """
    Structure to hold an information about group entry.
    
    :var groupByTypes: A list containing display names of types of Item or PSOccurrence on which this rule entry is to
    be evaluated. This will be populated in cases of entry type is CFMGroupItemTypeEntry or Fnd0CFMGroupOccTypeEntry.
    Example: For CFMGroupItemTypeEntry, it can contain display names of item types as AllocationMap, CAEBCItem,
    CAEConnItem, CAEItem.
    :var listOfSubEntries: A list of entries that are grouped together.
    """
    groupByTypes: List[str] = ()
    listOfSubEntries: List[RevRuleSubEntryInfo] = ()


@dataclass
class RevRuleInfoResponse(TcBaseObj):
    """
    This structure contains all information about input RevisionRule like description, all clauses of RevisionRule,
    Boolean if RevisionRule supports nested effectivity.
    
    :var entriesInfo: A list containing rule entries in a RevisionRule.
    :var nestedEffectivity: If true, nested effectivity is added to RevisionRule. If nested effectivity is added,
    Teamcenter evaluates nested effectivities as per effectivity mappings.
    :var description: Description of a RevisionRule.
    """
    entriesInfo: List[RevRuleEntryInfo] = ()
    nestedEffectivity: bool = False
    description: str = ''


@dataclass
class RevRuleSubEntryInfo(TcBaseObj):
    """
    Structure represents a sub entry\clause in a group entry.
    
    :var mapOfSubEntryKeyToValue: A map (string, string) pairs of entry name and its value. For example, 
    1: For entry type Working, the map will contain "user", and "group" as keys and UIDs of User and Group as values
    respectively.
    2: For entry type Status, the map will contain "status_type" as key and UID of attached status i.e TaskType as
    value.
    3: For entry type Override, the map will contain "folder as key and UID of Folder as value.
    :var subEntryType: Indiactes type of the subentry inside group entry.A group entry is made up of a sequential list
    of sub entries. Evaluation of the group entry involves evaluating each of the sub-entries in a given order.Valid
    types of sub-entries are:
    0 - Working 
    1 - Status
    2 - Override
    3 - Date
    4 - Unit No. 
    6 - Precise 
    7 - Latest
    8 - End Item 
    10 - Branch.
    :var displayText: Display text of the sub entry.
    """
    mapOfSubEntryKeyToValue: MapOfRevRuleEntryKeyToValue = None
    subEntryType: int = 0
    displayText: str = ''


@dataclass
class RevisionRuleInfo(TcBaseObj):
    """
    Structure containing information about RevisionRule's name, description,clauses using which RevisionRule will be
    created or updated.
    
    :var uid: Unique Identifier (UID) of a RevisionRule to be created or updated.
    :var name: Name of the RevisionRule.
    :var description: Description of a RevisionRule.
    :var entriesInfo: A list containing entries in a RevisionRule.
    :var nestedEffectivity: If true, nested effectivity is added to RevisionRule. If nested effectivity is added,
    Teamcenter evaluates nested effectivities as per effectivity mappings.
    :var isPrivate: If true, RevisionRule is available only to the user who has logged-in. In this case, a runtime
    property suppressed on a RevisionRule will be set. A combination of properties suppressed and owning user will be
    used to decide if a RevisionRule is available to the user or not.
    """
    uid: str = ''
    name: str = ''
    description: str = ''
    entriesInfo: List[RevRuleEntryInfo] = ()
    nestedEffectivity: bool = False
    isPrivate: bool = False


@dataclass
class CreateOrUpdateRevRuleResp(TcBaseObj):
    """
    Returns information on created or updated RevisionRule along with service data containing created or updated
    objects.
    
    :var revisionRuleInfo: Information about created or updated RevisionRule.
    :var serviceData: ServiceData with created or updated objects.
    The following partial errors may be returned as part of service data:
    710001 An internal error has occurred in the Configuration Management module. Please report this error to your
    system administrator.
    710041 Revision Rule does not exist.
    710042 Revision Rule with name already exists.
    710052 Revision Rule already has a Date Entry - only one allowed per rule.
    710053 Revision Rule already has a Unit No Entry - only one allowed per rule.
    710055 An Override Entry must contain a valid Override Folder.
    710056 Invalid date : must be set either to today or to a valid date.
    710057 Invalid unit number : must be zero or positive.
    """
    revisionRuleInfo: RevisionRuleInfo = None
    serviceData: ServiceData = None


@dataclass
class CreateUpdateRevRuleInput(TcBaseObj):
    """
    Input structure required to create or update RevisionRule.
    
    :var updateExisting: If true, an existing RevisionRule with the same name will be updated else a new RevisionRule
    will be created.
    :var isPrivate: If true, RevisionRule is avaliable only to the user who has logged-in.In this case, a runtime
    property 'suppressed' on a RevisionRule will be set.A combination of properties 'suppressed' and 'owning_user' will
    be used to decide if a RevisionRule is avaiable to the user or not.
    :var revisionRuleInfo: Information on RevisionRule to be created or updated.
    """
    updateExisting: bool = False
    isPrivate: bool = False
    revisionRuleInfo: RevisionRuleInfo = None


"""
A map (string, string) pairs of entry name and its value. For example,
1: For entry type Working, the map will contain "user", and "group" as keys and UIDs of User and Group as values respectively.
2: For entry type Status, the map will contain "status_type" as key and UID of attached status i.e TaskType as value. 
3: For entry type Override
"""
MapOfRevRuleEntryKeyToValue = Dict[str, str]
