from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0Message, Awb0Element, Awb0ProductContextInfo
from tcsoa.gen.Internal.ActiveWorkspaceBom._2018_05.Compare import CompareResultsCursor
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompareContentData2(TcBaseObj):
    """
    Input containing Awb0Element objects, configuration information and depth describing how deep traversal and compare
    to be performed.
    
    :var source: 'CompareContentInfo'2 for source object to compare.
    :var target: 'CompareContentInfo'2 for target object to compare.
    :var startFreshCompare: If true, a fresh compare is initiated.
    :var compareInBackground: If true, compare will be initiated in background.
    :var notificationMessage: Notification message containing the compare results.
    :var sourceCursor: 'CompareResultsCursor' for source.
    :var targetCursor: 'CompareResultsCursor' for target.
    :var compareOptions: A map (string, list of strings) containing an option for compare as key and list of its
    associated attributes as values. The following supported key/values are:
    
    Key "FilteringRule" with following list of values.
    - AccountabilityAll - Includes all lines.
    - AccountabilityLeavesOnly - Includes only leaf nodes; excludes all hierarchy nodes.
    - AccountabilityLinkedAssmOrLeaves - Includes assigned assembly nodes but excludes their children. If an assembly
    is not assigned, includes its leaf nodes.
    - AccountabilityMOA - To compare source and destination BOMs, traversing or skipping occurrences in the source
    structure based on the occurrence type of the linked occurrences in the destination structure.
    - DesignToBomAll - To validate completeness between part BOM and CAD BOM.
    
    
    
    Key "DisplayOptions" with following list of valid values.
    - PartialMatch &ndash; Compare specific set of properties for a match between source and target structure.
    - FullMatch &ndash; Compare for exact match between source and target structure.
    
    """
    source: CompareContentInfo2 = None
    target: CompareContentInfo2 = None
    startFreshCompare: bool = False
    compareInBackground: bool = False
    notificationMessage: Fnd0Message = None
    sourceCursor: CompareResultsCursor = None
    targetCursor: CompareResultsCursor = None
    compareOptions: CompareOptionsMap = None


@dataclass
class CompareContentInfo2(TcBaseObj):
    """
    Input structure for storing source and target information for content comparison.
    
    :var element: Awb0Element whose children are to be compared.
    :var productContextInfo: Awb0ProductContextInfo containing configuration information for the element.
    :var visibleUids: A list of unique ID for element for which compare differences values to be returned.
    :var depth: Level to which the source or target is to be expanded for compare.
    Value greater than 0 means level to which the source or target is to be expanded.
    Value -1 means all levels of structure will be compared.
    Value 0 means only leaf nodes to be compared.
    Value -2 means it is expected to get saved results if exists any.
    :var filteringRule: A list of filtering rules to be used for compare. This can contain AccountabilityAll ,
    AccountabilityLeavesOnly, AccountabilityLinkedAssmOrLeaves etc.
    """
    element: Awb0Element = None
    productContextInfo: Awb0ProductContextInfo = None
    visibleUids: List[str] = ()
    depth: int = 0
    filteringRule: str = ''


@dataclass
class CompareOptionsResponse(TcBaseObj):
    """
    Contains response of operation getCompareOptions.
    
    :var compareOptions: A map (string, list of strings) containing an option for compare as key and list of its
    associated attributes as values. The following supported key/values are:
    
    Key "FilteringRule" with following list of values.
    - AccountabilityAll - Includes all lines.
    - AccountabilityLeavesOnly - Includes only leaf nodes; excludes all hierarchy nodes.
    - AccountabilityLinkedAssmOrLeaves - Includes assigned assembly nodes but excludes their children. If an assembly
    is not assigned, includes its leaf nodes.
    - AccountabilityMOA - To compare source and destination BOMs, traversing or skipping occurrences in the source
    structure based on the occurrence type of the linked occurrences in the destination structure.
    - DesignToBomAll - To validate completeness between part BOM and CAD BOM.
    
    
    
    Key "DisplayOptions" with following list of valid values.
    - PartialMatch &ndash; Compare specific set of properties for a match between source and target structure.
    - FullMatch &ndash; Compare for exact match between source and target structure.
    
    """
    compareOptions: CompareOptionsMap = None


@dataclass
class CompareResp2(TcBaseObj):
    """
    Structure to store response of content comparison.
    
    :var sourceDifferences: A map( string, int ) of unique identifer and status for source. The map comprises of unique
    identifier of Awb0Element and its integer status in the source structure as compared to the target structure.UID of
    Awb0Element is followed by list of unique identifiers (UID) of equivalent Awb0Elements if any. The Awb0Element
    object can have one or more equivalent objects identified using equivalence and partial match criteria.The
    equivalent objects&rsquo; unique identifiers are populated when diff has status 2.
    Integer value indicates below:
    2 (Modified) &ndash; The object represented by the unique identifier has one or more property value differences
    when compared to target.
    3 (Missing from Target) - The object represented by the unique identifier is missing in target.
    :var targetDifferences: A map( string, int ) of unique identifer and status for target. The map comprises of unique
    identifier of Awb0Element and its integer status in the target structure as compared to the source structure.UID of
    Awb0Element is followed by list of unique identifiers (UID) of equivalent Awb0Elements if any. The Awb0Element
    object can have one or more equivalent objects identified using equivalence and partial match criteria.The
    equivalent objects&rsquo; unique identifiers are populated when diff has status 2.
    Integer value indicates below:
    1 (Missing from Source) &ndash; The object represented by the unique identifier is missing from source.
    2 (Modified) &ndash; The object represented by the unique identifier has one or more property value differences
    when compared to source.
    :var sourceDepth: Level to which comparison of source structure is done.
    Value greater than 1 means the level till which structure was compared.Value -1 means all levels of structures were
    compared.Value 0 means only leaf nodes were compared.
    :var totalNoOfSourceDifferences: Number of total source differences found for the given input.
    :var totalNoOfTargetDifferences: Number of total target differences found for the given input.
    :var serviceData: The service data.
    :var pagedSourceDifferences: Compare results data for source.
    :var pagedTargetDifferences: Compare results data for target.
    :var sourceCursor: 'CompareResultsCursor' for source.
    :var targetCursor: 'CompareResultsCursor' for target.
    :var timestampOfStoredResults: Time stamp of stored compare results if found any for the given compare input
    options.
    :var compareOptions: A map (string, list of strings) containing an option for compare as key and list of its
    associated attributes as values. The following supported key/values are:
    
    Key "FilteringRule" with following list of values.
    - AccountabilityAll - Includes all lines.
    - AccountabilityLeavesOnly - Includes only leaf nodes; excludes all hierarchy nodes.
    - AccountabilityLinkedAssmOrLeaves - Includes assigned assembly nodes but excludes their children. If an assembly
    is not assigned, includes its leaf nodes.
    - AccountabilityMOA - To compare source and destination BOMs, traversing or skipping occurrences in the source
    structure based on the occurrence type of the linked occurrences in the destination structure.
    - DesignToBomAll - To validate completeness between part BOM and CAD BOM.
    
    
    
    Key "DisplayOptions" with following list of valid values.
    - PartialMatch &ndash; Compare specific set of properties for a match between source and target structure.
    - FullMatch &ndash; Compare for exact match between source and target structure.
    
    
    :var targetDepth: Level to which comparison of target structure is done.
    Value greater than 1 means the level till which structure was compared.Value -1 means all levels of structures were
    compared.Value 0 means only leaf nodes were compared.
    """
    sourceDifferences: CompareContentOutputMap2 = None
    targetDifferences: CompareContentOutputMap2 = None
    sourceDepth: int = 0
    totalNoOfSourceDifferences: int = 0
    totalNoOfTargetDifferences: int = 0
    serviceData: ServiceData = None
    pagedSourceDifferences: List[CompareResultsRespData2] = ()
    pagedTargetDifferences: List[CompareResultsRespData2] = ()
    sourceCursor: CompareResultsCursor = None
    targetCursor: CompareResultsCursor = None
    timestampOfStoredResults: datetime = None
    compareOptions: CompareOptionsMap = None
    targetDepth: int = 0


@dataclass
class CompareResultsRespData2(TcBaseObj):
    """
    Output structure for compare results.
    
    :var uids: Unique identifier (UID) of Awb0Element followed by list of unique identifiers (UID) of equivalent
    Awb0Elements if any. The Awb0Element object can have one or more equivalent objects identified using equivalence
    and partial match criteria.The equivalent objects&rsquo; unique identifiers are populated when diff has status 2.
    :var diff: Status of Awb0Element in comparison results. Integer value indicates below:
    1 (Missing from Source) &ndash; The object represented by the unique identifier is missing from source.
    2 (Modified) &ndash; The object represented by the unique identifier has one or more property value differences
    when compared to source. 
    3 (Missing from Target) - The object represented by the unique identifier is missing in target.
    """
    uids: str = ''
    diff: int = 0


"""
Map( string , int ) to store output from content comparision.
"""
CompareContentOutputMap2 = Dict[str, int]


"""
A map (string, list of strings) containing an option for compare as key and list of its associated attributes as values.
"""
CompareOptionsMap = Dict[str, List[str]]
