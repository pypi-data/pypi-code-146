from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpansionResponse(TcBaseObj):
    """
    'ExpansionResponse' contains a map with key as parent Fnd0BomLineLite or BOMLine and values as 'ChildLineInfo'.
    Additionally it also contains 'DatasetInfo' and uids of undelivered Fnd0BomLineLite objects.
    
    :var parentChildInfo: Map with key as parent Fnd0BomLineLite or BOMLine and values as' ChildLineInfo'. 
    :var datasetInfo: 'DatasetInfo' contains name of GRM relation through which underlying object of Fnd0BomLineLite or
    BOMLine is attached to Dataset, Dataset object and list of 'NamedRefInfo'.
    :var undeliveredLines: Fnd0BomLineLite uids which are yet to be transferred to client. 
    :var serviceData: The service data containing partial errors.
    """
    parentChildInfo: ParentLineToChildLineInfo = None
    datasetInfo: List[DatasetInfo] = ()
    undeliveredLines: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class LineAndPaths(TcBaseObj):
    """
    'LineAndPaths' contains beginning Fnd0BomLineLite/BOMLine and list of 'Paths' which needs to configured as
    Fnd0BomLineLite.
    
    :var startingLine: Fnd0BomLineLite or BOMLine as starting line from which child Fnd0BomLineLite to be constructed
    based on 'Paths'.
    :var paths: List of 'Path' where each element has attribute and value for which Fnd0BomLineLite to be constructed.
    """
    startingLine: RuntimeBusinessObject = None
    paths: List[Path] = ()


@dataclass
class NamedRefInfo(TcBaseObj):
    """
    Contains details of named reference object of Dataset. 
    
    :var name: Name of reference object in Dataset. For example, JTPart.
    :var type: The type of the named reference object.
    :var object: Object reference corresponding to the named reference.
    :var fileTicket: FMS ticket used to retrieve the file in cases where named reference objects to be returned. 
    """
    name: str = ''
    type: str = ''
    object: BusinessObject = None
    fileTicket: str = ''


@dataclass
class PartialExpansionControls(TcBaseObj):
    """
    Contains preferences to control how much to expand and return. Also describes 'RelationAndTypesCriteria' specifying
    relation name and Dataset information to query related objects.
    
    :var expansionPrefValues: Contains payload and Dataset retrieval preferences.
    Supported key, values and meaning are:
    
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
    generated during operation are returned. Other valid value is positive integer.
    
    Key: wantSiblings
    Specifies whether to return siblings of Fnd0BomLineLite found based on 'Path'(s). 
    0 indicates to ignore sibling creation. This is default behavior.
    1 indicates return siblings Fnd0BomLineLite. Note that siblings are not expanded by this operation.
    
    Note that response is returned when either of minLinesWithRelatedObjects or outputPageSize criteria is satisfied.
    Siblings are also considered while calculating outputPageSize.
    
    
    
    
    
    
    
    :var relationCriteria: 'RelationAndTypesCriteria' contains GRM relation name, criteria to retrieve named reference
    objects and 'DatasetTypeAndNamedRefs'. This information is used to retrieve related Dataset, named reference
    objects and FMS tickets.
    """
    expansionPrefValues: StringKeyToIntValue = None
    relationCriteria: List[RelationTypesAndCriteria] = ()


@dataclass
class Path(TcBaseObj):
    """
    'Path' contains list of uids to be configured as Fnd0BomLineLite. The elements of the 'Path' must be in top to
    bottom order. The first value of elements must be associated to startingLine of 'LineAndPaths'. The last element of
    the path specifies end.
    
    :var pathId: Identifier of the path. 
    This is for future usage where client may request any one path with same id to be resolved.
    :var basedOn: List of string where string can be either AbsOccId, APN or CloneStableId. If length is not same as
    that of elements, last basedOn is assumed for remaining elements.
    :var elements: Contains list of AbsOccurrence puid, MEAppearancePathNode puid or clone stable occ uid of
    PSOccurrenceThread as identifier of PSOccurrence to configure as Fnd0BomLineLite.
    """
    pathId: str = ''
    basedOn: List[str] = ()
    elements: List[str] = ()


@dataclass
class RelationTypesAndCriteria(TcBaseObj):
    """
    Criteria to find Datasets and named reference objects associated to Fnd0BomLineLite objects.
    
    :var relationName: Name of GRM relation through Dataset is attached with underlying object of Fnd0BomLineLite or
    BOMLine. This field can not be empty.
    :var namedRefHandler: Describes criteria to retrieve named reference objects. 
    
    Default value is empty string, in such case named reference objects as specified in 'DatasetTypeAndNamedRefs' are
    retrieved.
    
    - No named reference objects are retrieved when specified as 'NoNamedRefs'. However, related Dataset as specified
    in attachmentTypeName of 'DatasetTypeAndNamedRefs' are retrieved. 
    - All named reference objects of Dataset to be retrieved when specified as 'AllNamedRefs'.  
    - Preferred JT will be returned when value is 'PreferredJT'.
    
    
    
    Note that namedReferencesNames of 'DatasetTypeAndNamedRefs' is ignored when value is 'NoNamedRefs', 'AllNamedRefs'
    or 'PreferredJT'.
    :var datasetTypeAndNamedRefs: A list of 'DatasetTypeAndNamedRefs'.
    """
    relationName: str = ''
    namedRefHandler: str = ''
    datasetTypeAndNamedRefs: List[DatasetTypeAndNamedRefs] = ()


@dataclass
class ChildLineInfo(TcBaseObj):
    """
    'ChildLineInfo' contains child line object, 'index to DatasetInfo' and configuration accuracy flag. 
    
    :var line: Child of BOMLine or Fnd0BomLineLite as key of 'ParentLineToChildLineInfo'. Child can be BOMLine or
    Fnd0BomLineLite.
    :var indexToAttachedObjInfos: Index to datasetInfos in 'ExpansionResponse'. 'DatasetInfos' at that index has
    information about  Dataset, named references objects etc for the line.
    :var configNotReliable: Indicates if configuration is not accurate. Set to true when there is Occurrence
    Effectivity or Incremental Change associated with PSOccurrence.
    """
    line: RuntimeBusinessObject = None
    indexToAttachedObjInfos: List[int] = ()
    configNotReliable: bool = False


@dataclass
class Controls(TcBaseObj):
    """
    'Controls' facilitates user to specify the payload and information to find related Dataset objects.
    
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
    """
    expansionPref: StringKeyToIntValue = None
    relationCriteria: List[RelationTypesAndCriteria] = ()


@dataclass
class DatasetInfo(TcBaseObj):
    """
    'DatasetInfo' describes GRM relation name through which Dataset is attached with underlying object of
    Fnd0BomLineLite or BOMLine. It also contains 'NamedRefInfo' for Dataset requested through' DatasetTypeAndNamedRefs'.
    
    :var relationName: Name of GRM relation through which underlying object of Fnd0BomLineLite or BOMLine is related to
    Dataset object.
    :var dataset: Dataset attached to Fnd0BomLineLite or BOMLine.
    :var namedRefInfo: Named reference objects details for Dataset.
    """
    relationName: str = ''
    dataset: Dataset = None
    namedRefInfo: List[NamedRefInfo] = ()


@dataclass
class DatasetTypeAndNamedRefs(TcBaseObj):
    """
    Contains DatasetType name and named reference names for Dataset to be retrieved.
    
    :var datasetTypeName: Type of Dataset to be retrieved.
    :var namedReferenceNames: List of named references names for Dataset. For example, JTPart.
    """
    datasetTypeName: str = ''
    namedReferenceNames: List[str] = ()


"""
Map with key as Fnd0BomLineLite or BOMLine and 'ChildLineInfo' as values.
"""
ParentLineToChildLineInfo = Dict[RuntimeBusinessObject, List[ChildLineInfo]]


"""
Map with string as key and integer as value.
"""
StringKeyToIntValue = Dict[str, int]
