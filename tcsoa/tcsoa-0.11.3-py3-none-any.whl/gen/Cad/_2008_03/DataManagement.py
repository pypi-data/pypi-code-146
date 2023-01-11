from __future__ import annotations

from tcsoa.gen.Cad._2007_01.DataManagement import ItemInfo, ExtraObjectInfo, ItemRevInfo, DatasetFileInfo, AttributeInfo
from tcsoa.gen.BusinessObjects import BusinessObject, CadAttrMappingDefinition, ItemRevision, Dataset
from typing import Dict, List
from tcsoa.gen.Cad._2007_12.DataManagement import NamedReferenceObjectInfo2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MappedDatasetAttrPropertyInfo(TcBaseObj):
    """
    Contains resolved object and property name along with CadAttrMappingDefinition object reference associated with the
    resolved property object.
    
    :var cadAttrMappingDefinition: CadAttrMappingDefinition object reference associated with the resolved property
    Object.
    :var resolvedObject: Object reference of object holding mapped attribute value
    :var resolvedPropertyName: The property name of the mapped object holding the attribute value of interest resulting
    from evaluation of a dataset CAD attribute mapping definition.
    """
    cadAttrMappingDefinition: CadAttrMappingDefinition = None
    resolvedObject: BusinessObject = None
    resolvedPropertyName: str = ''


@dataclass
class PartInfo3(TcBaseObj):
    """
    The PartInfo3 struct is the main input to the createOrUpdateParts service.
    This structure refers to the Item, ItemRevision, and one or more Dataset structures used to create those objects.
    
    :var clientId: Identifier defined by user to track the related object.
    :var itemInput: Member of type ItemInfo
    :var itemRevInput: Member of type ItemRevInfo
    :var datasetInput: List of DatasetInfo3
    """
    clientId: str = ''
    itemInput: ItemInfo = None
    itemRevInput: ItemRevInfo = None
    datasetInput: List[DatasetInfo3] = ()


@dataclass
class ResolveAttrMappingsInfo(TcBaseObj):
    """
    Contains dataset, item revision and list of 'CadAttrMappingDefinition' object references to use to resolve the
    mapping.
    
    :var dataset: Dataset object reference to use as starting point to get mapped attribute values.
    :var itemRev: ItemRevision object reference helps resolve ambiguity in the mapping traversal for the dataset or can
    be the starting point for the traversal as well.
    :var mappingDefinitionInfos: List of CadAttrMappingDefinitionInfo objects
    """
    dataset: Dataset = None
    itemRev: ItemRevision = None
    mappingDefinitionInfos: List[CadAttrMappingDefinitionInfo] = ()


@dataclass
class ResolveAttrMappingsResponse(TcBaseObj):
    """
    Holds the response for resolveAttrMappings. The processing of the input is as follows :
    1.    Process the ResolveAttrMappingsInfo first. This will validate the dataset and item revision inputs are valid.
    If this validation fails, then an error will be returned with the index of the ResolveMappinsInfo being the
    identifier with the error. 
    2.    Process the list of CadAttrMappingDefinitionInfo. If this results in an error then the identifier for the
    error will be the clientId specified in the CadAttributeMappingDefinition.
    When processing the output, if a key with thte clientId is not found, the application should first look for an
    error with an identifier of the cleintId. If no error is found then the index of the input that contained the
    clientId should be found.
    
    
    :var resolvedMappingsMap: Member of type 'ResolveAttrMappingsOutputMap'. This is a map containing the successfully
    mapped property information. The keys are the input 'clientIds' and the values are the output
    'MappedDatasetAttrPropertyInfo' structures.
    :var serviceData: Service data contains any partial errors and exceptions. The objects holding the mapped
    attributes, resulting from successfully resolved mappings, are returned as plain objects. The mapped attribute
    properties are returned as 'ServiceData' properties.
    """
    resolvedMappingsMap: ResolveAttrMappingsOutputMap = None
    serviceData: ServiceData = None


@dataclass
class CadAttrMappingDefinitionInfo(TcBaseObj):
    """
    Contains unique 'clientId' and 'CadAttributeMappingDefinition' object reference associated with the resolved
    property object.
    
    :var clientId: Unique client side identifier. This is a required input parameter If the 'ClientId' is not provided
    or not unique a partial error is reported and the property for the particular 'CADAttrMappingDefinition' will not
    resolved.
    :var cadAttrMappingDefinition: CadAttributeMappingDefinition object reference associated with the resolved property
    object
    """
    clientId: str = ''
    cadAttrMappingDefinition: CadAttrMappingDefinition = None


@dataclass
class DatasetInfo3(TcBaseObj):
    """
    The DatasetInfo3 struct represents all of the data necessary to construct the dataset object.
    The basic attributes that are required are passed as named elements in the struct.
    All other attributes are passed as name/value pairs in the AttributeInfo struct.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var dataset: Dataset object reference for update, null for creation
    :var createNewVersion: Flag to create new version ( TRUE ) or not (FALSE )
    :var mapAttributesWithoutDataset: Flag to indicate whether DatasetInfo should be used for mapping attributes or for
    create.
    :var namedReferencePreference: Preference name which holds the list of named references to delete from one Dataset
    version to the next.
    :var attrList: List of AttributeInfos for attributes
    :var mappingAttributes: List of AttributeInfos for mapped attributes. Mapped atributes are attributes that are
    applied to other objects. Refere to the ITK manual for a definition of attribute mapping.
    :var extraObject: List of ExtraObjectInfos
    :var datasetFileInfos: List of DatasetFileInfos
    :var namedReferenceObjectInfos: List of NamedReferenceObjectInfos
    :var name: Name attribute value
    :var basisName: Basis Name attribute value, used when the name is null or blank
    :var description: Description attribute value
    :var type: Type attribute value
    :var lastModifiedOfDataset: Last Modified Date of dataset
    :var id: ID attribute value
    :var datasetRev: Revision attribute value
    :var itemRevRelationName: Required input, may not be null, not defaulted
    """
    clientId: str = ''
    dataset: Dataset = None
    createNewVersion: bool = False
    mapAttributesWithoutDataset: bool = False
    namedReferencePreference: str = ''
    attrList: List[AttributeInfo] = ()
    mappingAttributes: List[AttributeInfo] = ()
    extraObject: List[ExtraObjectInfo] = ()
    datasetFileInfos: List[DatasetFileInfo] = ()
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo2] = ()
    name: str = ''
    basisName: str = ''
    description: str = ''
    type: str = ''
    lastModifiedOfDataset: datetime = None
    id: str = ''
    datasetRev: str = ''
    itemRevRelationName: str = ''


"""
ResolveAttrMappingsOutputMap
"""
ResolveAttrMappingsOutputMap = Dict[str, MappedDatasetAttrPropertyInfo]
