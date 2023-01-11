from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, DatasetType, WorkspaceObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandGRMRelationsData(TcBaseObj):
    """
    This structure contains information for 'ExpandGRMRelationsData'.
    
    :var otherSideObjects: Objects on the other side of the relationship
    :var relationName: Input GRM relation name
    """
    otherSideObjects: List[BusinessObject] = ()
    relationName: str = ''


@dataclass
class ExpandGRMRelationsOutput(TcBaseObj):
    """
    This structure contains information for Expand GRM Relations Output.
    
    :var inputObject: Object that was expanded
    :var otherSideObjData: List of 'ExpandGRMRelationsData'
    """
    inputObject: BusinessObject = None
    otherSideObjData: List[ExpandGRMRelationsData] = ()


@dataclass
class ExpandGRMRelationsPref(TcBaseObj):
    """
    Expand GRM Relations Pref
    
    :var expItemRev: Flag to expand any Item Revisions that are in the return data
    :var info: List of RelationAndTypesFilter2
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter2] = ()


@dataclass
class ExpandGRMRelationsResponse(TcBaseObj):
    """
    Expand GRM Relations Response
    
    :var output: List of SaveQueryCriteriaInfo
    :var serviceData: Standard ServiceData member
    """
    output: List[ExpandGRMRelationsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetAvailableTypesResponse(TcBaseObj):
    """
    The GetAvailableTypesResponse struct resprents return repsonse of all types implemented by the given class.
    
    :var inputClassToTypes: A map of given class names and all according AvailableTypeInfo objects.
    :var serviceData: ServiceData contains any parital error if any failure happens.
    """
    inputClassToTypes: ClassToTypesMap = None
    serviceData: ServiceData = None


@dataclass
class AvailableTypeInfo(TcBaseObj):
    """
    This structure represents string  instance of type and its hierarchy.
    
    :var type: The name of instance type
    :var hierarchies: hierarchies
    """
    type: str = ''
    hierarchies: List[str] = ()


@dataclass
class PurgeSequencesInfo(TcBaseObj):
    """
    The data structure represents all of the data necessary to purge sequences. The structure contains the selected
    object and a flag indicating whether to validate that the selected sequences is the active sequence.
    
    :var validateLatestFlag: A flag indicating if 'inputObject' should be validated that it is the latest sequence of
    the ItemRevision. To purge all previous sequences, set 'validateLatestFlag' true and set 'inputObject' to the
    latest sequence of the ItemRevision.  To purge a specific sequence, set 'validateLatestFlag' false and set
    'inputObject' to the specific sequence of the ItemRevision that should be purged.
    :var inputObject: A business object representing the ItemRevision sequence that should be purged.
    """
    validateLatestFlag: bool = False
    inputObject: WorkspaceObject = None


@dataclass
class ReferenceInfo(TcBaseObj):
    """
    This structure contains information for a given Dataset type.
    
    :var referenceName: Reference name for the input Dataset type
    :var isObject: Flag that signifies the reference is an object if the value is true.  False signifies the reference
    is a file.
    :var fileFormat: The format for reference object.  Valid values are either TEXT, BINARY or OBJECT.
    :var fileExtension: The default extension for a file, such as *.gif or *.doc.
    """
    referenceName: str = ''
    isObject: bool = False
    fileFormat: str = ''
    fileExtension: str = ''


@dataclass
class RelationAndTypesFilter(TcBaseObj):
    """
    This structure contains the relation name to traverse for the given operation and a list of other side object types
    that are valid to return.
    
    :var relationTypeName: Name of relation to traverse
    :var otherSideObjectTypes: List of names of valid other side object types to return
    """
    relationTypeName: str = ''
    otherSideObjectTypes: List[str] = ()


@dataclass
class RelationAndTypesFilter2(TcBaseObj):
    """
    This structure contains the relation name to traverse for the given operation and a list of other side object types
    that are valid to return.
    
    :var relationName: Types of relationships allowed
    :var objectTypeNames: Types of other objects allowed
    """
    relationName: str = ''
    objectTypeNames: List[str] = ()


@dataclass
class BaseClassInput(TcBaseObj):
    """
    The baseClassInput structure represents input data structure to get available Business Objects.
    
    :var baseClass: This is the name of the Business Object for which this operation returns the descendant Business
    Objects.
    :var exclusionTypes: Names of Business Objects (and its secondary Business Objects) to be excluded from returned
    list.
    """
    baseClass: str = ''
    exclusionTypes: List[str] = ()


@dataclass
class SetOrRemoveImmunityInfo(TcBaseObj):
    """
    The data structure represents all of the data necessary to toggle the immunity of an ItemRevision sequence. It
    contains a reference to the ItemRevision sequence whose immunity will be is modified and a flag indicating whether
    immunity will be revoked or applied.
    
    :var setOrRemoveFlag: Flag indicating if immunity should be set or removed on the 'inpoutObject'.  To set immunity,
    the 'setOrRemoveImmunityFlag' should be true.  To remove immunity, the' setOrRemoveImmunityFlag' should be false.
    :var inputObject: ItemRevision sequence object which should be made immune or have immunity removed.
    """
    setOrRemoveFlag: bool = False
    inputObject: WorkspaceObject = None


@dataclass
class ValidateIdsInfo(TcBaseObj):
    """
    The 'ValidateIdsInfo' struct contains the input ids for item and revision and the item type.
    
    :var itemId: Item ID to be validated
    :var revId: Revision ID to be validated
    :var itemType: Item type to validate against, can be null
    """
    itemId: str = ''
    revId: str = ''
    itemType: str = ''


@dataclass
class ValidateIdsOutput(TcBaseObj):
    """
    This structure contains the modified item and revision ids and enum status of the ids respectively.  Valid values
    for the enums are Valid (ids are valid), Invalid (ids are not valid), Modified (ids are not ideal but can be used
    if the user really wants them), Override (ids are not valid, silently replace with modified ones), and Duplicate
    (ids are already allocated in the system).
    
    :var modItemId: Modified item id if specified by Naming Rules
    :var itemIdStatus: Status of the item id represented as a 'ValidateIdsStatus' enum
    :var modRevId: Modified rev id if specified by Naming Rules
    :var revIdStatus: Status of the revision id represented as a 'ValidateIdsStatus' enum
    """
    modItemId: str = ''
    itemIdStatus: ValidateIdsStatus = None
    modRevId: str = ''
    revIdStatus: ValidateIdsStatus = None


@dataclass
class ValidateItemIdsAndRevIdsResponse(TcBaseObj):
    """
    The list of 'ValidateIdsOutput' structures and the 'ServiceData'.
    
    :var output: List of 'ValidateIdsOutput' structures
    :var serviceData: ServiceData contains only error information returned by this operation.
    """
    output: List[ValidateIdsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class WhereReferencedByRelationNameInfo(TcBaseObj):
    """
    The data structure contains the object to perform the where referenced operation on and the filters to narrow the
    list of referencing objects returned.
    
    :var object: Desired business object to find referencing objects of
    :var filter: A list of filters to limit the search of referencing objects
    """
    object: BusinessObject = None
    filter: List[RelationAndTypesFilter] = ()


@dataclass
class WhereReferencedByRelationNameOutput(TcBaseObj):
    """
    This structure contains the object that the where referenced operation was performed on and list of
    'WhereReferencedRelationNameOutputInfo' structures.
    
    :var inputObject: Input object for which referencers were found
    :var info: List of 'WhereReferencedByRelationNameOutputInfo' structures
    """
    inputObject: BusinessObject = None
    info: List[WhereReferencedByRelationNameOutputInfo] = ()


@dataclass
class WhereReferencedByRelationNameOutputInfo(TcBaseObj):
    """
    This structure contains the referencer object, the corresponding relation name, and the level at which the
    referencer was found.
    
    :var referencer: Referencer object of the input object
    :var relationTypeName: Relation type name of how referencer is related to input object
    :var level: Integer value for the level depth where referencer found
    """
    referencer: BusinessObject = None
    relationTypeName: str = ''
    level: int = 0


@dataclass
class WhereReferencedByRelationNameResponse(TcBaseObj):
    """
    The data structure contains the list of the referencing objects that meet the filter criteria for each of the input
    objects.
    
    :var output: A list of filtered referencing objects for each input object
    :var serviceData: Service data
    """
    output: List[WhereReferencedByRelationNameOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetTypeInfo(TcBaseObj):
    """
    This structure contains the Dataset type object reference corresponding to the input Dataset type name and the
    reference information for each valid named reference of the Dataset type.
    
    :var tag: Dataset type reference object for the Dataset type
    :var refInfos: List of valid references for the Dataset type
    """
    tag: DatasetType = None
    refInfos: List[ReferenceInfo] = ()


@dataclass
class DatasetTypeInfoResponse(TcBaseObj):
    """
    The response from 'getDatasetTypeInfo' operation.
    
    :var infos: List of named reference information for each dataset type specified in 'datasetTypeNames' input.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData 'plain objects with the dataset
    type object that corresponds to the input dataset type name.
    """
    infos: List[DatasetTypeInfo] = ()
    serviceData: ServiceData = None


class ValidateIdsStatus(Enum):
    """
    A map of enum of the status for validating ids.
    """
    Valid = 'Valid'
    Invalid = 'Invalid'
    Modified = 'Modified'
    Override = 'Override'
    Duplicate = 'Duplicate'


"""
ClassToTypesMap
"""
ClassToTypesMap = Dict[str, List[AvailableTypeInfo]]
