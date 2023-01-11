from __future__ import annotations

from tcsoa.gen.Cad._2008_06.DataManagement import AttributeInfo
from tcsoa.gen.BusinessObjects import BusinessObject, Folder
from tcsoa.gen.Cad._2010_09.DataManagement import DatasetFileInfo
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExtraObjectInfo(TcBaseObj):
    """
    Form objects that can be created or updated and related to an item, item revision or dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var createOrUpdateInput: CreateOrUpdateInput object which contains attributes to create an extra object.
    createOrUpdateInput can be null for update.
    :var relationTypeName: Name of the relation type to the parent object
    """
    clientId: str = ''
    createOrUpdateInput: CreateOrUpdateInput = None
    relationTypeName: str = ''


@dataclass
class ItemInfo(TcBaseObj):
    """
    The 'ItemInfo' structure represents all of the data necessary to construct the item object. The basic attributes
    that are required are passed as named elements in the structure. All other attributes are passed as name/value
    pairs in the 'AttributeInfo' structures: 'attrList' and 'formAttrList'. The 'extraObject' field allows for the
    creation of an object(s) that will be related to this newly created Item.
    
    :var createOrUpdateInput: 'CreateOrUpdateInput' object which contains attributes to create an Item.
    'createOrUpdateInput' can be null for update.
    :var itemExtraObject: List of extra objects to be used or created and related to the Item.
    :var itemRevisionExtraObject: List of extra objects to be used or created and related to the Item Revision.
    :var folder: Folder to attach the Item to. If null, then the Teamcenter preference WsoInsertNoSelectionsPref is
    used to get the default location.
    """
    createOrUpdateInput: CreateOrUpdateInput = None
    itemExtraObject: List[ExtraObjectInfo] = ()
    itemRevisionExtraObject: List[ExtraObjectInfo] = ()
    folder: Folder = None


@dataclass
class NamedReferenceObjectInfo(TcBaseObj):
    """
    Contains information regarding named reference type value, object reference, object type name and list of attribute
    information to set on the object.
    
    :var clientId: Identifier defined by client to track the related object.
    :var createOrUpdateInput: Object that contains 'attributes' to create a named reference object.
    'createOrUpdateInput' can be null for update.
    :var namedReferenceName: The named reference from the dataset to this object and a required input. Named reference
    name values  are defined for each dataset type. The customer can add more values as needed. To get a current list
    of valid named reference name values the programmer can either use the Business Modeler IDE or can call the Core
    service 'getDatasetTypeInfo'.
    :var namedReferenceType: The reference type name from the dataset to this object, must be either AE_ASSOCIATION or
    AE_PART_OF.
    """
    clientId: str = ''
    createOrUpdateInput: CreateOrUpdateInput = None
    namedReferenceName: str = ''
    namedReferenceType: str = ''


@dataclass
class PartInfo(TcBaseObj):
    """
    The 'PartInfo' struct is the main input to the 'createOrUpdateParts' service for boundingbox. This structure refers
    to the item and one or more dataset structures used to create those objects.
    
    :var clientId: Identifier defined by the user to track the related object.
    :var itemInput: Member of type 'ItemInfo'.
    :var datasetInput: List of 'DatasetInfos'.
    """
    clientId: str = ''
    itemInput: ItemInfo = None
    datasetInput: List[DatasetInfo] = ()


@dataclass
class CreateOrUpdateInput(TcBaseObj):
    """
    The 'CreateOrUpdateInput' structure represents all of the data necessary to construct a business object. All
    attributes are passed in as name/value pairs for the corresponding value type map.
    The 'compoundCreateOrUpdateInput' field allows for the creation of a secondary object(s) for the newly created
    primary object.
    
    :var boName: Business Object type name. This field must be specified for create.
    :var boReference: Existing object reference. This field must be specified for update.
    :var boolProps: A map (string/boolean) of property names to a single value.
    :var boolArrayProps: A map (string/list of booleans) of property names to a list of values.
    :var dateProps: A map (string/datetime) of property names to a single value.
    :var dateArrayProps: A map (string/list of datetimes) of property names to a list of values.
    :var tagProps: A map (string/business object) of property names to a single value.
    :var tagArrayProps: A map (string/list of business objects) of property names to a list of values.
    :var compoundCreateOrUpdateInput: 'CreateOrUpdateInput' for secondary (compounded) objects
    :var stringProps: A map (string/string) of property names to a single value.
    :var stringArrayProps: A map (string/list of strings) of property names to a list of values.
    :var doubleProps: A map (string/double) of property names to a single value.
    :var doubleArrayProps: A map (string/list of doubles) of property names to a list of values.
    :var floatProps: A map (string/float) of property names to a single value.
    :var floatArrayProps: A map (string/list of floats) of property names to a list of values.
    :var intProps: A map (string/integer) of property names to a single value.
    :var intArrayProps: A map (string/list of integers) of property names to a list of values.
    """
    boName: str = ''
    boReference: BusinessObject = None
    boolProps: BoolMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    tagProps: TagMap = None
    tagArrayProps: TagVectorMap = None
    compoundCreateOrUpdateInput: CreateOrUpdateInputMap = None
    stringProps: StringMap = None
    stringArrayProps: StringVectorMap = None
    doubleProps: DoubleMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None


@dataclass
class DatasetInfo(TcBaseObj):
    """
    The 'DatasetInfo' struct represents all of the data necessary to construct the Dataset object. The basic attributes
    that are required are passed as named elements in the structure. All other attributes are passed as name/value
    pairs in the 'AttributeInfo' structure: 'attrList'. The extraObject field allows for the creation of an object(s)
    that will be related to this newly created Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var createOrUpdateInput: 'CreateOrUpdateInput' object which contains attributes to create a Dataset.
    'createOrUpdateInput' can be null for update.
    :var datasetFileInfos: List of 'DatasetFileInfos', which holds the basic information for a file to be uploaded to a
    Dataset.
    :var namedReferenceObjectInfos: List of 'NamedReferenceObjectInfos', contains information regarding named reference
    type value, object reference, object type name and list of attribute information to set on the object.
    :var basisName: Basis name attribute value. When the dataset name is blank, the basis name is used to call
    USER_new_dataset_name to generate a new name.
    :var lastModifiedOfDataset: If not null, the date and time that the Dataset was last modified. If the actual
    modified date and time is later, then an error is thrown.
    :var itemRevRelationName: The relation name for the Dataset to ItemRevision relation. Can be null, but is required
    if an ItemRevision is specified.
    :var createNewVersion: Flag to create new version ( TRUE ) or not (FALSE ).
    :var mapAttributesWithoutDataset: Flag to indicate whether 'DatasetInfo' should be used for mapping attributes or
    for create.
    :var namedReferencePreference: Preference name which holds the list of named references to delete from one Dataset
    version to the next.
    :var mappingAttributes: List of 'AttributeInfos' for mapped attributes. Mapped attributes are attributes that are
    applied to other objects. Refer to the ITK manual for a definition of attribute mapping.
    :var extraObject: List of 'ExtraObjectInfos', the extra objects to be created and related to the Dataset.
    """
    clientId: str = ''
    createOrUpdateInput: CreateOrUpdateInput = None
    datasetFileInfos: List[DatasetFileInfo] = ()
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo] = ()
    basisName: str = ''
    lastModifiedOfDataset: datetime = None
    itemRevRelationName: str = ''
    createNewVersion: bool = False
    mapAttributesWithoutDataset: bool = False
    namedReferencePreference: str = ''
    mappingAttributes: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()


"""
Map of string client ids to vector of 'CreateOrUpdateInput' values (string, vector).
"""
CreateOrUpdateInputMap = Dict[str, List[CreateOrUpdateInput]]


"""
Map of DateTime property names to values (string, < DateTime>).
"""
DateMap = Dict[str, datetime]


"""
Map of DateTime array property names to values (string, vector< DateTime>).
"""
DateVectorMap = Dict[str, List[datetime]]


"""
DoubleMap
"""
DoubleMap = Dict[str, float]


"""
Map of double array property names to values (string, vector).
"""
DoubleVectorMap = Dict[str, List[float]]


"""
Map of float property names to values (string, float).
"""
FloatMap = Dict[str, float]


"""
Map of float array property names to values (string, vector).
"""
FloatVectorMap = Dict[str, List[float]]


"""
Map of int property names to values (string, int).
"""
IntMap = Dict[str, int]


"""
IntVectorMap
"""
IntVectorMap = Dict[str, List[int]]


"""
Map of boolean property names to values (string, bool).
"""
BoolMap = Dict[str, bool]


"""
Map of string property names to values (string, string).
"""
StringMap = Dict[str, str]


"""
Map of bool array property names to values (string, vector< bool >).
"""
BoolVectorMap = Dict[str, List[bool]]


"""
Map of string array property names to values (string, vector).
"""
StringVectorMap = Dict[str, List[str]]


"""
Map of BusinessObject property names to values (string, BusinessObject).
"""
TagMap = Dict[str, BusinessObject]


"""
Map of BusinessObject array property names to values (string, vector).
"""
TagVectorMap = Dict[str, List[BusinessObject]]
