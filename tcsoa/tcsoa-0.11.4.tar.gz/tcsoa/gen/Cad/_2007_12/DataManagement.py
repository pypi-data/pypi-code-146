from __future__ import annotations

from tcsoa.gen.Cad._2007_01.DataManagement import ItemInfo, ExtraObjectInfo, ItemRevInfo, DatasetFileInfo, AttributeInfo
from tcsoa.gen.BusinessObjects import BusinessObject, Dataset
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NamedReferenceObjectInfo2(TcBaseObj):
    """
    Contains information for object named references to apply to the Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var object: Object reference of the object for update, null for create
    :var namedReferenceName: The Named Reference from the dataset to this object, required. NamedReference values  are
    defined for each Dataset type. The customer can add more values as needed. To get a current list of valid Named
    Reference values the programmer can either use BMIDE or can call the SOA Core service getDatasetTypeIno.
    :var namedReferenceType: The reference type name from the dataset to this object, must be either AE_ASSOCIATION or
    AE_PART_OF.
    :var typeName: Type of the object to be created. Required for object creation only.
    :var attrNameValuePairs: List of AttributeInfos.
    """
    clientId: str = ''
    object: BusinessObject = None
    namedReferenceName: str = ''
    namedReferenceType: str = ''
    typeName: str = ''
    attrNameValuePairs: List[AttributeInfo] = ()


@dataclass
class PartInfo2(TcBaseObj):
    """
    The PartInfo2 struct is the main input to the createOrUpdateParts service.
    This structure refers to the Item, ItemRevision, and one or more Dataset structures used to create those objects.
    
    :var clientId: Identifier defined by user to track the related object.
    :var itemInput: Member of type ItemInfo
    :var itemRevInput: Member of type ItemRevInfo
    :var datasetInput: List of DatasetInfo2
    """
    clientId: str = ''
    itemInput: ItemInfo = None
    itemRevInput: ItemRevInfo = None
    datasetInput: List[DatasetInfo2] = ()


@dataclass
class CreateOrUpdatePartsPref(TcBaseObj):
    """
    Input structure for CreateOrUpdatePartsPref
    
    :var overwriteForLastModDate: Flag to check whether dataset needs to be modified, if input last modified date is
    different from actual.
    """
    overwriteForLastModDate: bool = False


@dataclass
class DatasetInfo2(TcBaseObj):
    """
    The DatasetInfo2 struct represents all of the data necessary to construct the dataset object.
    The basic attributes that are required are passed as named elements in the struct.
    All other attributes are passed as name/value pairs in the AttributeInfo struct.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var dataset: Dataset object reference for update, null for creation
    :var createNewVersion: Flag to create new version ( TRUE ) or not (FALSE )
    :var namedReferencePreference: Preference name which holds the list of named references to delete from one Dataset
    version to the next
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
