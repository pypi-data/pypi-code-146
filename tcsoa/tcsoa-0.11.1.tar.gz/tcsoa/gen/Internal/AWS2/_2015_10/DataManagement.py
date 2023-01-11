from __future__ import annotations

from tcsoa.gen.BusinessObjects import DatasetType, ImanType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDatasetTypesWithDefaultRelOutput(TcBaseObj):
    """
    This GetDatasetTypesWithDefaultRelationOutput struct contains the list dataset type, their default paste relation
    for the given parent and reference information and Service Data.
    
    :var fileExtension: The fileExtension for each Dataset type specified in fileExtensions input.
    :var datasetTypesWithDefaultRelInfo: The matching list of named reference information and default paste relation
    for the Dataset type.
    """
    fileExtension: str = ''
    datasetTypesWithDefaultRelInfo: List[DatasetTypeInfoWithDefaultRelation] = ()


@dataclass
class ReferenceInfo(TcBaseObj):
    """
    The ReferenceInfo struct contains information for a given Dataset type
    
    :var referenceName: The reference name for the input dataset type.
    :var isObject: If true, signifies the reference is an object. False signifies the reference is a file.
    :var fileFormat: The format for reference object. Valid values are either TEXT, BINARY or OBJECT.
    :var fileExtension: The default extension for a file, such as *.gif or *.doc.
    """
    referenceName: str = ''
    isObject: bool = False
    fileFormat: str = ''
    fileExtension: str = ''


@dataclass
class DatasetTypeInfoWithDefaultRelation(TcBaseObj):
    """
    The DatasetTypeInfoWithDefaultRelation struct contains the dataset type object reference corresponding to the input
    dataset type name, default paste relation for the input parent and the reference information for each valid named
    reference of the dataset type.
    
    :var datasetType: The DatasetType object for the input dataset type
    :var refInfos: The list of valid named references for the input DatasetType.
    :var defaultRelationInfo: The default paste relation for the input DatasetType for the given input parent.
    """
    datasetType: DatasetType = None
    refInfos: List[ReferenceInfo] = ()
    defaultRelationInfo: DefaultRelationInfo = None


@dataclass
class DatasetTypesWithDefaultRelation(TcBaseObj):
    """
    This DatasetTypesWithDefaultRelation struct contains pair of file extension and the list of
    DatasetTypeInfoWithDefaultRelation structures.
    
    :var output: List of named reference information and default paste relation for the given input parent for each
    Dataset type specified in fileExtensions input.
    :var serviceData: The DatasetType objects that corresponds to fileExtensions input are added to the Plain object
    list.
    """
    output: List[GetDatasetTypesWithDefaultRelOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DefaultRelationInfo(TcBaseObj):
    """
    The DefaultRelationInfo struct contains information for a given dataset type.
    
    :var defaultRelation: The ImanType of the default paste relation for the Dataset for the given input parent.
    :var name: Internal name of the default paste relation for the Dataset for the given input parent.
    :var displayName: Display name of the default paste relation for the Dataset for the given input parent.
    """
    defaultRelation: ImanType = None
    name: str = ''
    displayName: str = ''
