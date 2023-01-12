from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, Dataset
from typing import Dict, List
from tcsoa.gen.Internal.StructureManagement._2013_05.StructureExpansionLite import RelationTypesAndCriteria
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpansionResponse3(TcBaseObj):
    """
    'ExpansionResponse3' contains a map with key as parent Fnd0BomLineLite or BOMLine and values as 'ChildLineInfo'.
    Additionally it also contains 'DatasetInfo' and UIDs of undelivered Fnd0BomLineLite objects.
    
    :var parentChildInfo: A map (business object, list of 'ChildLineInfo') the Key either a Fnd0BOMLineLite or BOMLine 
    parent line and values a list of 'ChildLineInfo' which contains child line object,' index to DatasetInfo 'and
    configuration accuracy information.
    :var datasetInfo: 'DatasetInfo' contains name of GRM relation through which underlying object of Fnd0BOMLineLite or
    BOMLine is attached to Dataset, Dataset object and list of 'NamedRefInfo'.
    :var parentUndeliveredChildrenUids: A map (business object, list of string) Parent BOMLine or Fnd0BOMLineLite and
    its children UIDs which are yet to be transferred to client.
    :var serviceData: The service data containing partial errors.
    """
    parentChildInfo: ParentLineToChildLineInfo3 = None
    datasetInfo: List[DatasetInfo3] = ()
    parentUndeliveredChildrenUids: ParentLineToChildrenLineUidValues2 = None
    serviceData: ServiceData = None


@dataclass
class NamedRefInfo3(TcBaseObj):
    """
    Contains details of named reference object of Dataset.
    
    :var name: Name of reference object in Dataset. For example, JTPart.
    :var type: The type of the named reference object.
    :var namedReference: The named reference object. Some common named reference objects are of type ImanFile and Form.
    :var originalFileName: The original_file_name attribute value of the file in case the named reference object is a
    file.
    :var fileTicket: FMS ticket used to retrieve the file.
    """
    name: str = ''
    type: str = ''
    namedReference: BusinessObject = None
    originalFileName: str = ''
    fileTicket: str = ''


@dataclass
class AbsoccDataIncludeList(TcBaseObj):
    """
    This List contains Absoccdata overrides type that would be considered during "LWB Configuration".
    
    :var absoccDataTypeInclusionList: List of AbsoccDataOverrideInfo.
    """
    absoccDataTypeInclusionList: List[AbsoccDataOverrideInfo] = ()


@dataclass
class AbsoccDataOverrideInfo(TcBaseObj):
    """
    'AbsoccDataOverrideInfo' structure contains the Absoccdata Override info.
    
    :var absoccDataType: Type of AbsoccData.
    :var additionalInfo: Additional Infomation about AbsoccData.
    """
    absoccDataType: int = 0
    additionalInfo: str = ''


@dataclass
class ChildLineInfo2(TcBaseObj):
    """
    'ChildLineInfo' contains child line object, index to 'DatasetInfo' and configuration accuracy flag.
    
    :var line: Line can be BOMLine or Fnd0BomLineLite. This object is added into the service data response, hence
    depending on the Business Object type, the respective properties will be loaded from the property policy.
    :var indexToAttachedObjInfos: A list of index to datasetInfos in 'ExpansionResponse'. 'DatasetInfos' at that index
    has information about Dataset, named references objects and relation name for the line.
    :var unSupportedInfo: 0 indicates that line has all supported data. This is default value.
    1 indicates that line has Modular Variants.
    2 indicates that line has Incremental Change.
    3 indicates that line has Modular Variants and Incremental Change.
    4 indicate that line has Classic Variants (pre 8.2 format) .
    5 indicates that line has Classic Variants (pre 8.2 format) and Modular Variants.
    6 indicates that line has Classic Variants (pre 8.2 format) and Incremental Change.
    7 indicates that line has Classic Variants (pre 8.2 format) and Modular Variants &amp; Incremental Change.
    """
    line: RuntimeBusinessObject = None
    indexToAttachedObjInfos: List[int] = ()
    unSupportedInfo: int = 0


@dataclass
class Controls2(TcBaseObj):
    """
    'Controls2' facilitates user to specify the payload and information to find related Dataset objects.
    
    :var expansionPref: Contains payload and Dataset retrieval preferences.
    Supported key, values and meaning are:
    
    Key: maxLevel
    Number of levels to be expanded for a expansion request. If not specified next immediate level is expanded. This is
    the default behavior.
    Other valid value is positive integer.
    
    Key: fetchRelatedObjects
    Specifies whether to return related Dataset objects as specified in relationCriteria. Valid values are 0 and 1.
    0 indicates do not return any related objects. This is the default value.
    1 indicates to return related objects as per relationCriteria.
    
    Key: minLinesWithRelatedObjects
    Specifies minimum lines to accumulate with related Dataset objects based on relationCriteria. This preference has
    significance only when fetchRelatedobjects is set 1.
    If not specified or specified as 0 related object check is not performed. Other valid value is positive integer.
    
    Key: outputPageSize
    Specifies number of child lines to return in response. When preference is not specified or passed as 0, all lines
    generated during operation are returned. Other valid value is any positive integer.
    
    Note that response is returned when either of maxLevel, minLinesWithRelatedObjects or outputPageSize criteria is
    satisfied.
    :var relationCriteria: 'RelationAndTypesCriteria' contains GRM relation name, criteria to retrieve named reference
    objects and 'DatasetTypeAndNamedRefs'. This information is used to retrieve related Dataset, named reference
    objects and FMS tickets.
    :var processLeafNodesFirst: Setting this control parameter will consider Leaf nodes first for processing till the
    level of expansion achieved in expansion operation.
    :var absoccFilterList: This lists the Absocc properties that should be considered (included) during Configuration.
    :var configurationSolveType: Setting this control parameter will evaluate following LWB properties during Expansion:
    &bull;   bl_variant_state
    &bull;   bl_is_occ_configured
    &bull;   bl_is_suppressed
    0 indicates above properties will not be evaluated during Expansion.
    1 indicates above properties will be evaluated during Expansion.
    Note: This parameter is not considered if the "Show Un Configured By Variants" and "Show UnConfigured By Occurrence
    Effectivity" on the BOMWindow are FALSE.
    """
    expansionPref: StringKeyToIntValue2 = None
    relationCriteria: List[RelationTypesAndCriteria] = ()
    processLeafNodesFirst: bool = False
    absoccFilterList: AbsoccDataIncludeList = None
    configurationSolveType: int = 0


@dataclass
class Controls3(TcBaseObj):
    """
    'Controls3' facilitates user to specify the payload and information to find related Dataset objects.
    
    :var expansionPref: Contains payload and Dataset retrieval preferences.
    
    Supported key, values and meaning are:
    
    Key: maxLevel
    Number of levels to be expanded for a expansion request. If not specified next immediate level is expanded. This is
    the default behavior.
    Other valid value is positive integer.
    
    Key: fetchRelatedObjects
    Specifies whether to return related Dataset objects as specified in relationCriteria. Valid values are 0 and 1.
    0 indicates do not return any related objects. This is the default value.
    1 indicates to return related objects as per relationCriteria.
    
    Key: outputPageSize
    Specifies number of child lines to return in response. When preference is not specified or passed as 0, all lines
    generated during operation are returned. Other valid value is any positive integer.
    
    Note that response is returned when either of maxLevel, minLinesWithRelatedObjects or outputPageSize criteria is
    satisfied.
    :var relationCriteria: 'RelationAndTypesCriteria' contains GRM relation name, criteria to retrieve named reference
    objects and 'DatasetTypeAndNamedRefs'. This information is used to retrieve related Dataset, named reference
    objects and FMS tickets.
    :var processLeafNodesFirst: Setting this control parameter will consider Leaf nodes first for processing till the
    level of expansion achieved in this operation.
    """
    expansionPref: StringKeyToIntValue2 = None
    relationCriteria: List[RelationTypesAndCriteria] = ()
    processLeafNodesFirst: bool = False


@dataclass
class DatasetInfo3(TcBaseObj):
    """
    'DatasetInfo' describes GRM relation name through which Dataset is attached with underlying object of
    Fnd0BOMLineLite or BOMLine. It also contains 'NamedRefInfo' for Dataset requested through 'DatasetTypeAndNamedRefs'.
    
    :var relationName: Name of GRM relation through which underlying object of Fnd0BOMLineLite or BOMLine is related to
    Dataset object.
    :var dataset: Dataset attached to Fnd0BOMLineLite or BOMLine.
    :var namedRefInfo: A list of named reference objects details for Dataset.
    """
    relationName: str = ''
    dataset: Dataset = None
    namedRefInfo: List[NamedRefInfo3] = ()


"""
Map with key as Fnd0BOMLineLite or BOMLine and 'ChildLineInfo' as values.
"""
ParentLineToChildLineInfo3 = Dict[RuntimeBusinessObject, List[ChildLineInfo2]]


"""
Map with key as Fnd0BOMLineLite or BOMLine and uids of the children lines as values.
"""
ParentLineToChildrenLineUidValues2 = Dict[RuntimeBusinessObject, List[str]]


"""
Map with string as key and integer as value.
"""
StringKeyToIntValue2 = Dict[str, int]
