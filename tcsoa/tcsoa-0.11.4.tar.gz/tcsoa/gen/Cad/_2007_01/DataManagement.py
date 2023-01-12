from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ListOfValues, CadAttrMappingDefinition, ImanRelation, Folder, Dataset, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandFolderForCADPref(TcBaseObj):
    """
    Contains list of RelationAndTypesFilter, number of latest revisions for further filtering and a flag to check
    whether item revision needs to be expanded.
    
    :var expItemRev: Flag to specify if item revisions are to be expanded ( TRUE ) or not ( FALSE ) if found as other
    side objects.
    :var latestNRevs: The number of latest revisions under an Item that should be considered for further filtering
    :var info: A list of RelationAndTypesFilter2
    """
    expItemRev: bool = False
    latestNRevs: int = 0
    info: List[RelationAndTypesFilter2] = ()


@dataclass
class ExpandFoldersForCADItemOutput(TcBaseObj):
    """
    Contains the item expanded and the list of item revisions for the item.
    
    :var outputItem: An item that is in the input folder.
    :var itemRevsOutput: A list of 'ExpandFolderForCADItemRevOutput' which contains information about any item
    revisions that belong to item as specified by 'latestNRevs'.
    """
    outputItem: Item = None
    itemRevsOutput: List[ExpandFoldersForCADItemRevOutput] = ()


@dataclass
class ExpandFoldersForCADItemRevOutput(TcBaseObj):
    """
    Contains the item revision expanded and the results of expanding the item revision.
    
    :var outputItemRevs: An item revision that is in the input folder.
    :var outputDatasets: A list of datasets related to the item revision as specified by the input filter.
    """
    outputItemRevs: ItemRevision = None
    outputDatasets: List[Dataset] = ()


@dataclass
class ExpandFoldersForCADOutput(TcBaseObj):
    """
    Contains the output data for ExpandFoldersForCAD operation.
    
    :var inputFolder: Folder object reference of the folder of interest
    :var fstlvlFolders: A list of Folder object references in the input folder
    :var itemsOutput: A list of ExpandFoldersForCADItemOutput for the item
    :var itemRevsOutput: A list of ExpandFoldersForCADItemRevOutput for the item revision
    """
    inputFolder: Folder = None
    fstlvlFolders: List[Folder] = ()
    itemsOutput: List[ExpandFoldersForCADItemOutput] = ()
    itemRevsOutput: List[ExpandFoldersForCADItemRevOutput] = ()


@dataclass
class ExpandFoldersForCADResponse(TcBaseObj):
    """
    Contains the response for ExpandFoldersForCAD operation.
    
    :var output: A list of ExpandFoldersForCADOutput which has information about the input folder and folders, items
    and itemRevs output found under this folder
    :var serviceData: SOA framework object containing objects that were created, deleted, or updated by the Service,
    plain objects, and service errors/failure information
    """
    output: List[ExpandFoldersForCADOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandGRMRelationsData(TcBaseObj):
    """
    Contains a list of related objects and the relation name used to relate to the input object.
    
    :var otherSideObjects: A list of object references of objects the object of interest is related to.
    :var relationName: The name of the relation used to relate the object of interest to the other otherSideObjects
    """
    otherSideObjects: List[BusinessObject] = ()
    relationName: str = ''


@dataclass
class ExpandGRMRelationsOutput(TcBaseObj):
    """
    Contains the output data for ExpandGRMRelations operation.
    
    :var inputObject: The object reference of the object of interest
    :var otherSideObjData: List of ExpandGRMRelationsData
    """
    inputObject: BusinessObject = None
    otherSideObjData: List[ExpandGRMRelationsData] = ()


@dataclass
class ExpandGRMRelationsPref(TcBaseObj):
    """
    Contains a list of RelationAndTypesFilter and a flag to check whether item revision needs to be expanded.
    
    :var expItemRev: Flag to specify if item revisions are to be expanded ( TRUE ) or not ( FALSE ) if found as other
    side objects.
    :var info: List of RelationAndTypesFilter2
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter2] = ()


@dataclass
class ExpandGRMRelationsResponse(TcBaseObj):
    """
    Top level response structure for ExpandGRMRelations operations.
    
    :var output: A list of ExpandGRMRelationsOutput which has information about the input object and it's filtered
    related object list
    :var serviceData: SOA framework object containing objects that were created, deleted, or updated by the Service,
    plain objects, and service errors/failure information
    """
    output: List[ExpandGRMRelationsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExpandPrimaryObjectsData(TcBaseObj):
    """
    Contains a list of related objects and the relation name or property used to relate to the input object.
    
    :var otherSideObjects: A list of object references of objects the object of interest is related to.
    :var relationName: The name of the relation used to relate the object of interest to the other otherSideObjects
    """
    otherSideObjects: List[BusinessObject] = ()
    relationName: str = ''


@dataclass
class ExpandPrimaryObjectsOutput(TcBaseObj):
    """
    Contains the output data for ExpandPrimaryObjects operation.
    
    :var inputObject: The object reference of the object of interest
    :var otherSideObjData: List of ExpandPrimaryObjectsData
    """
    inputObject: BusinessObject = None
    otherSideObjData: List[ExpandPrimaryObjectsData] = ()


@dataclass
class ExpandPrimaryObjectsPref(TcBaseObj):
    """
    Contains list of RelationAndTypesFilter and a flag to check whether item revision needs to be expanded .
    
    :var expItemRev: Flag to specify if item revisions are to be expanded ( TRUE ) or not ( FALSE ) if found as other
    side objects.
    :var info: List of RelationAndTypesFilter2
    """
    expItemRev: bool = False
    info: List[RelationAndTypesFilter2] = ()


@dataclass
class ExpandPrimaryObjectsResponse(TcBaseObj):
    """
    Contains the response structure for ExpandPrimaryObjects operation.
    
    :var output: A list of ExpandPrimaryObjectsOutput
    :var serviceData: SOA framework object containing objects that were found by the service and service errors/failure
    information
    """
    output: List[ExpandPrimaryObjectsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ExtraObjectInfo(TcBaseObj):
    """
    Form objects that can be created or updated and related to an item, item revision or dataset.
    
    :var object: Object reference for existing object
    :var clientId: Identifier defined by user to track the related object.
    :var relationTypeName: Name of the relation type to the parent object
    :var typeName: Object Type name
    :var attrNameValuePairs: List of AttributeInfos.
    """
    object: BusinessObject = None
    clientId: str = ''
    relationTypeName: str = ''
    typeName: str = ''
    attrNameValuePairs: List[AttributeInfo] = ()


@dataclass
class ExtraObjectOutput(TcBaseObj):
    """
    Form objects that can be created or updated and related to an item, item revision or dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var object: Object reference of the created/updated object
    """
    clientId: str = ''
    object: BusinessObject = None


@dataclass
class GenerateAlternateIdsProperties(TcBaseObj):
    """
    Holds the input structure of 'GenerateAlternateIdsProperties'
    
    :var idContext: Object reference of the id context used to generate the alternate id of that context
    :var pattern: Pattern type used to generate the alternate id of that pattern
    :var altIdType: Type of the alternate id to generate
    :var parentAltId: Object reference of the parent alternate id
    :var count: Number of the alternate id to be generated.
    """
    idContext: BusinessObject = None
    pattern: str = ''
    altIdType: str = ''
    parentAltId: BusinessObject = None
    count: int = 0


@dataclass
class GenerateAlternateIdsResponse(TcBaseObj):
    """
    Holds the response for 'generateAlternateIds'
    
    :var inputIndexToAltId: Key is the index of the input, data is a list of alternate IDs generated.
    :var serviceData: Service data contains any partial errors and exceptions. No objects are created, deleted,
    modified or returned by this service.
    """
    inputIndexToAltId: IndexToAltId = None
    serviceData: ServiceData = None


@dataclass
class GetAllAttrMappingsResponse(TcBaseObj):
    """
    Contains the response for getAllAttrMappings operation.
    
    :var attrMappingInfos: A list of AttrMappingInfo
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information. CadAttrMappingDefinition objects are returned as plain objects.
    """
    attrMappingInfos: List[AttrMappingInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetAttrMappingsForDatasetTypeCriteria(TcBaseObj):
    """
    Input criteria for the data returned from the 'getAttrMappingsForDatasetType' operation.
    
    :var datasetTypeName: The type name of a dataset.  This input is required.
    :var itemTypeName: The type name of an item.  This input is optional.
    :var exact: The input flag indicating that the mappings to be returned are for a specific dataset type and item
    type combination when the value is true.
    """
    datasetTypeName: str = ''
    itemTypeName: str = ''
    exact: bool = False


@dataclass
class GetAttrMappingsForDatasetTypeOutput(TcBaseObj):
    """
    Contains the output data for the 'getAttrMappingsForDatasetType' operation.
    
    :var criteria: The dataset and item type criteria used to find the attribute mapping definitions.
    :var attrMappingInfos: The list of attribute mapping information that matches the 'criteria'.
    """
    criteria: GetAttrMappingsForDatasetTypeCriteria = None
    attrMappingInfos: List[AttrMappingInfo] = ()


@dataclass
class GetAttrMappingsForDatasetTypeResponse(TcBaseObj):
    """
    The response from the 'getAttrMappingsForDatasetType' operation.
    
    :var output: A list of input dataset and item type criteria and the found attribute mapping definitions.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' plain objects with
    'CadAttrMappingDefinition' objects and property descriptor LOV objects.
    """
    output: List[GetAttrMappingsForDatasetTypeOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GetAvailableTypesResponse(TcBaseObj):
    """
    Holds the response for 'getAvailableTypes', which the map of input objects (class names) and for each input object,
    the object references of found Types (NULL, if none found), along with the 'ServiceData'.
    
    :var inputClassToTypes: Map where the key is the class type and the value is a list of strings representing the
    types available for the class.
    :var serviceData: Contains objects that are returned by the service, and error information. The actual type objects
    are returned as 'PlainObjects'. This service does not define any of its own errors, but will return any errors from
    the subsystem in the list of partial errors.
    """
    inputClassToTypes: ClassToTypesMap = None
    serviceData: ServiceData = None


@dataclass
class ItemInfo(TcBaseObj):
    """
    The ItemInfo struct represents all of the data necessary to construct the item object.
    The basic attributes that are required are passed as named elements in the struct.
    All other attributes are passed as name/value pairs in the AttributeInfo struct.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Item.
    
    :var item: Item object reference for update, can be null for creation
    :var itemId: ID for create, generated if null
    :var itemType: Type, default is Item if null
    :var name: Name, defaulted to id if null
    :var description: Description, can be null
    :var attrList: List of AttributeInfos
    :var extraObject: List of ExtraObjectInfos
    :var folder: Folder to attach Item to, if null then default used
    """
    item: Item = None
    itemId: str = ''
    itemType: str = ''
    name: str = ''
    description: str = ''
    attrList: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()
    folder: Folder = None


@dataclass
class ItemRevInfo(TcBaseObj):
    """
    The ItemRevInfo structure represents all of the data necessary to construct the item revision object.
    The basic attributes that are required are passed as named elements in the struct.
    All other attributes are passed as name/value pairs in the AttributeInfo struct.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Item
    Revision.
    
    :var itemRevision: ItemRevision object reference, null for creation, otherwise update
    :var revId: ID, if null then generated
    :var attrList: List of AttributeInfos
    :var extraObject: List ofr ExtraObjectInfos
    """
    itemRevision: ItemRevision = None
    revId: str = ''
    attrList: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()


@dataclass
class AttrMappingInfo(TcBaseObj):
    """
    Contains CadAttrMappingDefinition object reference and the PropDescriptor structure used in the response of get
    attribute mapping operations.
    
    :var cadAttrMappingDefinition: CadAttrMappingDefinition object reference
    :var propDesc: PropDescriptor structure containing property information for mapping definition property.
    """
    cadAttrMappingDefinition: CadAttrMappingDefinition = None
    propDesc: PropDescriptor = None


@dataclass
class MappedDatasetAttrProperty(TcBaseObj):
    """
    Contains the found resolved object and property name mapped to specific input values.
    
    :var attrTitle: The CadAttrMappingDefinition object title. This is generally the client application attribute
    display name.
    :var datasetTypeName: The Teamcenter defined type name of a dataset.
    :var itemTypeName: The Teamcenter defined type name of an item
    :var resolvedObject: Object reference of object holding mapped attribute value
    :var resolvedPropertyName: The property name of the mapped object holding the attribute value of interest resulting
    from evaluation of a dataset CAD attribute mapping definition.
    """
    attrTitle: str = ''
    datasetTypeName: str = ''
    itemTypeName: str = ''
    resolvedObject: BusinessObject = None
    resolvedPropertyName: str = ''


@dataclass
class NamedReferenceObjectInfo(TcBaseObj):
    """
    Contains information regarding named refernce type value, Object reference, Object type name and list of Attribute
    infos.
    
    :var clientId: Identifier defined by user to track the related object.
    :var object: Object reference of the object for update, null for create
    :var namedReferenceName: The Named Reference from the dataset to this object, required. NamedReference values  are
    defined for each Dataset type. The customer can add more values as needed. To get a current list of valid Named
    Reference values the programmer can either use BMIDE or can call the SOA Core service getDatasetTypeIno.
    :var typeName: Type of the object to be created. Required for object creation only.
    :var attrNameValuePairs: List of AttributeInfos.
    """
    clientId: str = ''
    object: BusinessObject = None
    namedReferenceName: str = ''
    typeName: str = ''
    attrNameValuePairs: List[AttributeInfo] = ()


@dataclass
class AttributeInfo(TcBaseObj):
    """
    This structure allows the caller to define or update named attributes.
    The name member represents the property name for the related object and the value is the value to set.
    
    :var name: Text for Attribute Name
    :var value: Text for Attribute Value
    """
    name: str = ''
    value: str = ''


@dataclass
class PartInfo(TcBaseObj):
    """
    The PartInfo struct is the main input to the createOrUpdateParts service.
    This struct refers to the Item, ItemRevision, and one or more Dataset structures used to create those objects.
    
    :var clientId: Identifier defined by user to track the related object.
    :var itemInput: Member of type ItemInfo
    :var itemRevInput: Member of type ItemRevInfo
    :var datasetInput: List of DatasetInfos
    """
    clientId: str = ''
    itemInput: ItemInfo = None
    itemRevInput: ItemRevInfo = None
    datasetInput: List[DatasetInfo] = ()


@dataclass
class PropDescriptor(TcBaseObj):
    """
    The PropDescriptor struct describes information about the Teamcenter property
    
    :var propName: Name of the property
    :var displayName: Display name of the property
    :var isModifiable: Specifies whether the property is modifiable
    :var attachedSpecifier: attachedSpecifier
    :var maxLength: maxLength
    :var interdependentProps: interdependentProps
    :var defaultValue: Default value for the property
    :var propValueType: Value type for the property in integer form: PROP_untyped (0) No Value
    PROP_char (1) Value is a single character
    PROP_date (2) Value is a date
    PROP_double (3) Value is a double
    PROP_float (4) Value is a float
    PROP_int (5) Value is an integer
    PROP_logical (6) Value is a logical
    PROP_short (7) Value is a short
    PROP_string (8) Value is a character string
    PROP_typed_reference (9) Value is a typed reference
    PROP_untyped_reference (10) Value is an untyped reference
    PROP_external_reference (11) Value is an external reference
    PROP_note (12) Value is a note
    PROP_typed_relation (13) Value is a typed relation
    PROP_untyped_relation (14) Value is an untyped relation
    :var propType: Type for the property in integer form: PROP_unknown (0) Property type is Unknown
    PROP_attribute (1)  Based on a POM Attribute (int, string, ...)
    PROP_reference (2)  Based on a POM Reference
    PROP_relation (3) Based on an ImanRelation
    PROP_compound (4) Based on a property from another Type
    PROP_runtime (5) Based on a computed value
    :var isDisplayable: isDisplayable
    :var isArray: Specifies whether the property is an array or single value
    :var lov: ListOfValues object attached to the property (if any)
    :var isRequired: Specifies whether the property is required
    :var isEnabled: Specifies whether the property is enabled
    """
    propName: str = ''
    displayName: str = ''
    isModifiable: bool = False
    attachedSpecifier: int = 0
    maxLength: int = 0
    interdependentProps: List[str] = ()
    defaultValue: str = ''
    propValueType: int = 0
    propType: int = 0
    isDisplayable: bool = False
    isArray: bool = False
    lov: ListOfValues = None
    isRequired: bool = False
    isEnabled: bool = False


@dataclass
class RelationAndTypesFilter2(TcBaseObj):
    """
    Structure contains relation name and vector of related object types of interest, which will used for filtering
    purpose.
    
    :var relationName: The name of the relation of interest.
    :var objectTypeNames: A list of related object types of interest.
    """
    relationName: str = ''
    objectTypeNames: List[str] = ()


@dataclass
class ResolveAttrMappingsForDatasetInfo(TcBaseObj):
    """
    Contains dataset, item revision and list of 'CadAttrMappingDefinition' object references to be used in the resolve.
    
    :var dataset: Dataset object reference for which to get mapped attribute values.
    :var itemRev: ItemRevision object reference, helps resolve ambiguity in the mapping traversal.
    :var cadAttrMappingDefinitions: List of 'CadAttrMappingDefinition' object references
    """
    dataset: Dataset = None
    itemRev: ItemRevision = None
    cadAttrMappingDefinitions: List[CadAttrMappingDefinition] = ()


@dataclass
class ResolveAttrMappingsForDatasetOutput(TcBaseObj):
    """
    Contains the output data for 'resolveAttrMappingsForDataset'.
    
    :var dataset: Dataset object reference for which mapped attribute property information is desired.
    :var mappedProperties: A list of 'MappedDatasetAttrProperty'
    """
    dataset: Dataset = None
    mappedProperties: List[MappedDatasetAttrProperty] = ()


@dataclass
class ResolveAttrMappingsForDatasetResponse(TcBaseObj):
    """
    Contains the response for 'resolveAttrMappingsForDataset'.
    
    :var output: A list of 'ResolveAttrMappingsForDatasetOutput'
    :var serviceData: 'ServiceData' contains any partial errors and exceptions.
    The objects holding the mapped attributes, resulting from successfully resolved mappings, are returned as plain
    objects.
    The mapped attribute properties are returned as 'ServiceData' properties.
    """
    output: List[ResolveAttrMappingsForDatasetOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CommitDatasetFileInfo(TcBaseObj):
    """
    Holds the basic info for a file to be uploaded to a dataset.
    
    :var dataset: Dateset object reference.
    :var createNewVersion: Flag to create new version ( TRUE ) or not ( FALSE ).
    :var datasetFileTicketInfos: A list of DatasetFileTicketInfos.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileTicketInfos: List[DatasetFileTicketInfo] = ()


@dataclass
class CreateOrUpdatePartsOutput(TcBaseObj):
    """
    Intermediate level output structure for createOrUpdateParts operation.
    
    :var clientId: Identifier defined by user to track the related object.
    :var item: Item object reference of the created/updated item
    :var itemRev: ItemRevision object reference of the created/updated item revision
    :var datasetOutput: List of DatasetOutputs
    :var extraItemObjs: List of ExtraObjectOutputs for the item extra objects
    :var extraItemRevObjs: List of ExtraObjectOutputs for the item revision extra objects
    """
    clientId: str = ''
    item: Item = None
    itemRev: ItemRevision = None
    datasetOutput: List[DatasetOutput] = ()
    extraItemObjs: List[ExtraObjectOutput] = ()
    extraItemRevObjs: List[ExtraObjectOutput] = ()


@dataclass
class CreateOrUpdatePartsResponse(TcBaseObj):
    """
    Holds the response for createOrUpdateParts
    
    :var output: List of CreateOrUpdatePartsOutputs.
    :var serviceData: The SOA framework object containing objects that were created, deleted, or updated by the
    Service, plain objects, and error information.
    """
    output: List[CreateOrUpdatePartsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateRelationsInfo(TcBaseObj):
    """
    Contains input information for 'createdOrUpdateRelations' operation.
    
    :var clientId: Identifier defined by user to track the related object.
    :var relationType: Realtion of interest, required for create or update
    :var primaryObject: object reference of primary object of interest, required for create or update
    :var secondaryObject: object reference of secondary object of interest, required for create or update
    :var relation: ImanRelation object reference of existing relation, used for update if provided
    :var userData: object reference to an object that can be attached to the relation (optional)
    """
    clientId: str = ''
    relationType: str = ''
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    relation: ImanRelation = None
    userData: BusinessObject = None


@dataclass
class CreateOrUpdateRelationsOutput(TcBaseObj):
    """
    Contains the output response structure for 'createdOrUpdateRelations' operation.
    
    :var clientId: Identifier defined by user to track the related object.
    :var relation: ImanRelation object reference of relation created or updated
    """
    clientId: str = ''
    relation: ImanRelation = None


@dataclass
class CreateOrUpdateRelationsPref(TcBaseObj):
    """
    Contains a list of RelationAndTypesFilter structures for other side object filtering.
    
    :var info: A list of 'RelationAndTypesFilter2'
    """
    info: List[RelationAndTypesFilter2] = ()


@dataclass
class CreateOrUpdateRelationsResponse(TcBaseObj):
    """
    Contains the response for 'createOrUpdateRelations'
    
    :var output: A list of 'CreateOrUpdateRelationsOutput'
    :var serviceData: The SOA framework object containing objects that were created or updated by the service and error
    information. Errors are identified by the 'clientID' which is supplied in the input data.
    """
    output: List[CreateOrUpdateRelationsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    Holds the basic info for a file to be uploaded to a dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var fileName: Name of file to be uploaded.  Filename only, should not contain path to filename.
    :var namedReferencedName: Named Reference relation to file.
    :var isText: Flag to indicate if file is text ( TRUE ) or binary (FALSE ).
    :var allowReplace: Flag to indicate if file can be overwritten ( TRUE ) or not ( FALSE ).
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False


@dataclass
class DatasetFileTicketInfo(TcBaseObj):
    """
    Holds the basic info for a file to be uploaded to a dataset.
    
    :var datasetFileInfo: Member of type DatasetFileInfo.
    :var ticket: ID of ticket.
    """
    datasetFileInfo: DatasetFileInfo = None
    ticket: str = ''


@dataclass
class DatasetInfo(TcBaseObj):
    """
    Contains all of the data necessary to construct the dataset object.
    The basic attributes that are required are passed as named elements in the structure.
    All other attributes are passed as name/value pairs in the AttributeInfo structure.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var dataset: Dataset object reference for update, null for creation
    :var attrList: List of AttributeInfos for attributes
    :var mappingAttributes: List of AttributeInfos for mapped attributes. Mapped atributes are attributes that are
    applied to other objects. Refere to the ITK manual for a definition of attribute mapping.
    :var extraObject: List of ExtraObjectInfos
    :var datasetFileInfos: List of DatasetFileInfos
    :var namedReferenceObjectInfos: List of NamedReferenceObjectInfos
    :var name: Name attribute value
    :var description: Description attribute value
    :var type: Type attribute value
    :var id: ID attribute value
    :var datasetRev: Revision attribute value
    :var itemRevRelationName: Required input, may not be null, not defaulted
    :var createNewVersion: Flag to create new version ( TRUE ) or not (FALSE )
    :var namedReferencePreference: Preference name which holds the list of named references to delete from one Dataset
    version to the next.
    """
    clientId: str = ''
    dataset: Dataset = None
    attrList: List[AttributeInfo] = ()
    mappingAttributes: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()
    datasetFileInfos: List[DatasetFileInfo] = ()
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo] = ()
    name: str = ''
    description: str = ''
    type: str = ''
    id: str = ''
    datasetRev: str = ''
    itemRevRelationName: str = ''
    createNewVersion: bool = False
    namedReferencePreference: str = ''


@dataclass
class DatasetOutput(TcBaseObj):
    """
    Structure contains created/updated dataset objects.
    
    :var clientId: Identifier defined by user to track the related object.
    :var dataset: Dataset object reference of the created/updated dataset
    :var commitInfo: List of CommitDatasetFileInfos
    :var extraObjs: List of ExtraObjectOutputs for the extra objects
    :var namedRefObjs: List of ExtraObjectOutputs for the named references
    """
    clientId: str = ''
    dataset: Dataset = None
    commitInfo: List[CommitDatasetFileInfo] = ()
    extraObjs: List[ExtraObjectOutput] = ()
    namedRefObjs: List[ExtraObjectOutput] = ()


"""
Map of integer index of the input to vector of string alternate id values (string, vector).
"""
IndexToAltId = Dict[int, List[str]]


"""
Map of string class names to vector of type string values (string, vector).
"""
ClassToTypesMap = Dict[str, List[str]]
