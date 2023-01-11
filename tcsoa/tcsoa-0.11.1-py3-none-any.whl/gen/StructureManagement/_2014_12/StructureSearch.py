from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, IncrementalChangeElement, ItemRevision
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ICFilterCriteria(TcBaseObj):
    """
    ICFilterCriteria structure captures information about filtering criteria of incremental change contexts.
    
    :var owningUser: The owning user of the incremental change revision object(s) to search for.
    :var owningGroup: The owning group of the incremental change revision object(s) to search for.
    :var statuses: The details for status names and their start date.
    :var intents: A list of intents associated with Incremental Change contexts that should included in the search.
    These strings must be valid Intent names in Teamcenter.
    :var includedICRevs: A list of ItemRevision objects representing preselected incremental change contexts to be used
    for seaching incremental change elements. This list is merged with the results of the other search parameters.
    :var excludedICRevs: A list of ItemRevision objects representing preselected incremental change contexts to be
    excluded from the search
    """
    owningUser: str = ''
    owningGroup: str = ''
    statuses: StatusData = None
    intents: List[str] = ()
    includedICRevs: List[ItemRevision] = ()
    excludedICRevs: List[ItemRevision] = ()


@dataclass
class ICSearchInfo(TcBaseObj):
    """
    ICSearchInfo structure contains information for scoping the Incremental Change contexts to be intersected while
    searching for Incremental Change Elements tracking the changes in the structure. 
    
    :var isUnitData: If true unit data is being provided as opposed to date information.
    :var unitData: The details for searching changes based on unit information ( start Unit, end Unit and the end Item
    for the Unit effectivity).
    :var dateEffectivityData: The details for searching changes based on date (start Date and end Date).
    :var icFilterCriteria: The details for searching Incremental change contexts. It is only relevant for Incremental
    Change
    """
    isUnitData: bool = False
    unitData: EndItemUnitData = None
    dateEffectivityData: DateEffectivityData = None
    icFilterCriteria: ICFilterCriteria = None


@dataclass
class LineIceInfo(TcBaseObj):
    """
    LineIceInfo structure details the changes in Incremental Change context for each BOMLine. 
    
    :var line: The configured changed line. 
    :var iceChanges: A list of changes in the line based on Incremental Change.
    :var configuredCompetingIces: A list of incremental change elements that are configured - yet not selectable. The
    best candidate appears in iceChanges. Currently not supported and all ice elements appear under iceChanges.
    """
    line: BOMLine = None
    iceChanges: List[BaseIceInfo] = ()
    configuredCompetingIces: List[BaseIceInfo] = ()


@dataclass
class LineOccInfo(TcBaseObj):
    """
    Details the changes in Occurrence Effectivity context for each BOMLine.
    
    :var line: The line affected by OccurrenceEffectivity.
    :var occChanges: Details of changes in the line based on OccurrenceEffectivity.
    """
    line: BOMLine = None
    occChanges: OccEffInfo = None


@dataclass
class LineRevInfo(TcBaseObj):
    """
    Details the changes in Revision Effectivity context for each BOMLine.
    
    :var line: The line affected by RevisionEffectivity.
    :var revChanges: Details of changes in the line based on RevisionEffectivity.
    """
    line: BOMLine = None
    revChanges: RevEffInfo = None


@dataclass
class OccEffInfo(TcBaseObj):
    """
    OccEffInfo structure details the changes in OccurrenceEffectivity context for each PSOccurrence configured by
    OccurrenceEffectivity.
    
    :var changeType: Type of occurrence change. Currently, there is only one type of change supported.
    - 1 means data has been configured based on OccurrenceEffectivity.
    
    
    :var occurrence: The object which is configured by OccurrenceEffectivity.
    :var effectivity: detail of occurrence effectivity.
    :var auxiliaryData: A generic structure of keys and vectors of values (integer,double,object,string,date types) for
    passing additional metadata regarding the nature of incremental change.
    """
    changeType: int = 0
    occurrence: BusinessObject = None
    effectivity: str = ''
    auxiliaryData: AdditionalInfo = None


@dataclass
class OccurrenceEffectivitySearchInfo(TcBaseObj):
    """
    OccurrenceEffectivitySearchInfo structure contains information for scoping the Occurrence Effectivity parameters
    used for tracking changes in structure based on OccurrenceEffectivity.
    
    :var isUnitData: If true unit data is being provided as opposed to date information.
    :var unitData: The details for searching changes based on unit information ( start Unit, end Unit and the end Item
    for the Unit effectivity).
    :var dateEffectivityData: The details for searching changes based on date (start Date and end Date).
    """
    isUnitData: bool = False
    unitData: EndItemUnitData = None
    dateEffectivityData: DateEffectivityData = None


@dataclass
class RevEffInfo(TcBaseObj):
    """
    RevEffInfo structure details the changes in RevisionEffectivity context for each ItemRevision configured by
    RevisionEffectivity.
    
    :var changeType: Type of revision change. Currently, there is only one type of change supported.
    - 1 means data has been configured based on RevisionEffectivity.
    
    
    :var revision: The object which is configured by RevisionEffectivity.
    :var howConfigured: detail of how the revision is configured.
    :var unitRange: unit range text if unit effectivity is used.
    :var dateRange: date range text if date effectivity is used.
    :var auxiliaryData: A generic structure of keys and vectors of values (integer,double,object,string,date types) for
    passing additional metadata regarding the nature of incremental change.
    """
    changeType: int = 0
    revision: BusinessObject = None
    howConfigured: str = ''
    unitRange: str = ''
    dateRange: str = ''
    auxiliaryData: AdditionalInfo = None


@dataclass
class RevisionEffectivitySearchInfo(TcBaseObj):
    """
    RevisionEffectivitySearchInfo structure contains information for scoping the Revision Effectivity  parameters used
    for tracking changes in structure based on RevisionEffectivity.
    
    :var owningUser: The owning user of the incremental change revision object(s) to search for.
    :var owningGroup: The owning group of the incremental change revision object(s) to search for.
    :var statuses: The details for status names and their start date.
    :var isUnitData: If true unit data is being provided as opposed to date information.
    :var unitData: The details for searching changes based on unit information ( start Unit, end Unit and the end Item
    for the Unit effectivity).
    :var dateEffectivityData: The details for searching changes based on date (start Date and end Date).
    """
    owningUser: str = ''
    owningGroup: str = ''
    statuses: StatusData = None
    isUnitData: bool = False
    unitData: EndItemUnitData = None
    dateEffectivityData: DateEffectivityData = None


@dataclass
class BaseIceInfo(TcBaseObj):
    """
    BaseIceInfo structure details the changes in Incremental Change context for each Incremental Change Element.
    
    :var typeOfIce: Type of incremental change.
    - 1 means data has been added in context of incremental change.
    - 2 means data has been removed in context of incremental change.
    
    
    :var howConfigured: detail of how the incremental change is configured. If 'howConfigured' is empty, it means the
    incremental change element is not configured.
    :var unitRange: unit range text. Empty if not unit effectivity.
    :var dateRange: date range text if date effectivity is used.
    :var absoccRootLine: The context line name in which the change occurred
    :var auxiliaryData: A generic structure of keys and vectors of values (integer,double,object,string,date types) for
    passing additional metadata regarding the nature of incremental change.
    :var icRev: incremetal change revision object which is referenced by the incremental change element associated with
    the change.
    :var ice: incremental change element associated with the change on the bomline. This change can be because of
    structural changes, attachment changes, predecessor changes or activity changes associated with the bomline.
    :var affectedObject: The object affected by the change. It can be one of the following types (not full list):
    - PSOccurrence
    - Datasets
    - Folders
    - Forms
    - Activities
    - AbsOccData
    
    
    :var attributeName: Name of the attribute associated with the change
    :var attributeDisplayName: Display name of the attribute whose value changed.
    :var attributeValue: Value of the attribute after change in Incremental change context.
    :var predecessorName: name of predecessor.
    :var predecessorSequence: Sequence number of predecessor.
    """
    typeOfIce: int = 0
    howConfigured: str = ''
    unitRange: str = ''
    dateRange: str = ''
    absoccRootLine: str = ''
    auxiliaryData: AdditionalInfo = None
    icRev: ItemRevision = None
    ice: IncrementalChangeElement = None
    affectedObject: BusinessObject = None
    attributeName: str = ''
    attributeDisplayName: str = ''
    attributeValue: str = ''
    predecessorName: str = ''
    predecessorSequence: str = ''


@dataclass
class StatusData(TcBaseObj):
    """
    StatusData structure contains filtering criterion for release status objects associated with the change.
    
    :var listOfStatus: A list of status names like Pending, TCM Released etc. to be used to filter based on status names
    :var sinceDate: The date on or after which the status objects are created.
    """
    listOfStatus: List[str] = ()
    sinceDate: datetime = None


@dataclass
class StructureChangesResponse(TcBaseObj):
    """
    StructureChangesResponse structure contains a vector of structureChangesResponseElement, the size of which matches
    the input ChangeTrackerInput vector
    
    :var responseElements: A list of StructureChangesResponseElement structures.
    :var serviceData: Service data capturing partial errors using the input array index as client id.
    """
    responseElements: List[StructureChangesResponseElement] = ()
    serviceData: ServiceData = None


@dataclass
class StructureChangesResponseElement(TcBaseObj):
    """
    StructureChangesResponseElement returns the changed lines and removed lines. The removed lines are configured in
    removed lines. Should treat the removed lines with caution as they won't show up in the configured bom. 
    
    :var addedLines: A list of changed lines.
    :var removedLines: A list of configured removed lines. This is separate even though it is a change, to allow the
    clients to treat the removed lines carefully ( no selection synchronization for example).
    :var visibleLinesByOccEff: A list of changed lines in context of Occurrence Effectivity.
    :var invisibleLinesByOccEff: A list of unconfigured changed lines in context of Occurrence Effectivity.
    :var visibleLinesByRevEff: A list of changed lines in context of Revision Effectivity.
    :var invisibleLinesByRevEff: A list of unconfigured changed lines in context of Revision Effectivity.
    """
    addedLines: List[LineIceInfo] = ()
    removedLines: List[LineIceInfo] = ()
    visibleLinesByOccEff: List[LineOccInfo] = ()
    invisibleLinesByOccEff: List[LineOccInfo] = ()
    visibleLinesByRevEff: List[LineRevInfo] = ()
    invisibleLinesByRevEff: List[LineRevInfo] = ()


@dataclass
class ChangeTrackerInput(TcBaseObj):
    """
    ChangeTrackerInput structure contains a vector of ChangeTrackerDataTypes representing the type of change to track
    (any unique combination of IncrementalChange, RevisionEffectivity, OccurrenceEffectivity), a vector of BOMLine
    objects that are used for scoping the data (only lines below the scope are considered for change tracking), and a
    structure representing the selection criteria for Incremental Change. Currently, only Incremental Change based
    changes are trackable.
    
    :var dataTypes: Types of changes to be tracked. A unique of set of ChangeTrackerDataTypes
    (IncrementalChange,RevisionEffectivity,OccurrenceEffectivity). Currently, only IncrementalChange is supported.
    :var selectedLines: A list of scope lines below which the changes are to be tracked. Currently, must be BOMLine
    objects or their subtypes.
    :var occEffInfo: Occurrence effectivity selection criterion. Captures information about range of units/dates to be
    considered while searching for Occurrence effectivities.
    :var revEffInfo: Revision effectivity selection criterion. Captures information about range of units/dates/statuses
    to be considered while searching for Revision effectivities.
    :var icInfo: Incremental change context selection criterion. Captures information about range of
    units/dates/intents/statuses to be considered while searching for IncrementalChanges.
    """
    dataTypes: List[ChangeTrackerDataType] = ()
    selectedLines: List[BusinessObject] = ()
    occEffInfo: OccurrenceEffectivitySearchInfo = None
    revEffInfo: RevisionEffectivitySearchInfo = None
    icInfo: ICSearchInfo = None


@dataclass
class DateEffectivityData(TcBaseObj):
    """
    DateEffectivtyData structure captures information about date based effectivity. The search will track changes
    between the start Date and end Date. End Date must be greater than start Date.
    
    :var startDate: The start date of the range to search in.
    :var endDate: The end date of the range to search in.
    """
    startDate: datetime = None
    endDate: datetime = None


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    a generic structure to capture additional information.
    
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
class EndItemUnitData(TcBaseObj):
    """
    EndItemUnitData structure captures information about unit based effectivity. The search will track changes between
    the start Unit and end Unit for the specified End Item. All 3 must be valid for successful usage.
    
    :var startUnit: The start unit. Valid values must be 0 or greater.
    :var endUnit: The end Unit. Valid values must be greater than startUnit.
    :var endItem: Item or ItemRevision representing the end item corresponding to the start and end unit range.
    """
    startUnit: int = 0
    endUnit: int = 0
    endItem: BusinessObject = None


class ChangeTrackerDataType(Enum):
    """
     enum  ChangeTrackerDataType {IncrementalChange, RevisionEffectivity, OccurrenceEffectivity, Time};
    
    - Incremental Change     Track incremental Change based changes.
    - RevisionEffectivity         Track RevisionEffectivity based changes ( currently not supported ).
    - OccurrenceEffectivity     Track OccurrencEffectivity based changes ( currently not supported).
    - Time                         Track changes given a date range based on modified times of objects in that range (
    Currently not supported ).
    
    """
    IncrementalChange = 'IncrementalChange'
    RevisionEffectivity = 'RevisionEffectivity'
    OccurrenceEffectivity = 'OccurrenceEffectivity'
    Time = 'Time'


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
