from __future__ import annotations

from tcsoa.gen.Cad._2008_06.DataManagement import ItemInfo, ExtraObjectInfo, ItemRevInfo, AttributeInfo, NamedReferenceObjectInfo, BoundingBox
from tcsoa.gen.BusinessObjects import ImanVolume, Dataset
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PartInfo(TcBaseObj):
    """
    The PartInfo struct is the main input to the createOrUpdateParts service for boundingbox. This structure refers to
    the Item, ItemRevision, and one or more Dataset structures used to create those objects.
    
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
class DatasetFileInfo(TcBaseObj):
    """
    Holds the basic info for a file to be uploaded to a Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var fileName: Name of file to be uploaded.  Filename only, should not contain path to filename.
    :var namedReferencedName: Named Reference relation to file.
    :var isText: Flag to indicate if file is text ( TRUE ) or binary (FALSE ).
    :var allowReplace: Flag to indicate if file can be overwritten ( TRUE ) or not ( FALSE ).
    :var boundingBoxesAvailable: Flag to indicate 'BoundingBoxes' are available.
    :var destinationVolume: Destination volume into which the file will be uploaded. If null tag the current default
    volume of the user will be used.
    :var boundingBoxes: List of 'BoundingBoxes'.
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False
    boundingBoxesAvailable: bool = False
    destinationVolume: ImanVolume = None
    boundingBoxes: List[BoundingBox] = ()


@dataclass
class DatasetInfo(TcBaseObj):
    """
    The DatasetInfo struct represents all of the data necessary to construct the dataset object.
    The basic attributes that are required are passed as named elements in the structure.
    All other attributes are passed as name/value pairs in the AttributeInfo structure.
    The extraObject field allows for the creation of an object(s) that will be related to this newly created Dataset.
    
    :var clientId: Identifier defined by user to track the related object.
    :var dataset: Dataset object reference for update, null for creation
    :var createNewVersion: Flag to create new version ( TRUE ) or not (FALSE )
    :var mapAttributesWithoutDataset: Flag to indicate whether DatasetInfo should be used for mapping attributes or for
    create.
    :var namedReferencePreference: Preference name which holds the list of named references to delete from one Dataset
    version to the next
    :var attrList: List of AttributeInfos for attributes
    :var mappingAttributes: List of AttributeInfos for mapped attributes. Mapped atributes are attributes that are
    applied to other objects. Refere to the ITK manual for a definition of attribute mapping.
    :var extraObject: List of ExtraObjectInfos
    :var datasetFileInfos: List of DatasetFileInfos
    :var namedReferenceObjectInfos: List of NamedReferenceObjectInfos
    :var datasetTool: The dataset tool for the dataset. If not specified then the default tool will be used.
    :var name: Name attribute value
    :var basisName: basisName
    :var description: Description attribute value
    :var type: Type attribute value
    :var lastModifiedOfDataset: lastModifiedOfDataset
    :var id: ID attribute value
    :var datasetRev: Revision attribute value
    :var itemRevRelationName: Can be null, defaulted
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
    namedReferenceObjectInfos: List[NamedReferenceObjectInfo] = ()
    datasetTool: str = ''
    name: str = ''
    basisName: str = ''
    description: str = ''
    type: str = ''
    lastModifiedOfDataset: datetime = None
    id: str = ''
    datasetRev: str = ''
    itemRevRelationName: str = ''
