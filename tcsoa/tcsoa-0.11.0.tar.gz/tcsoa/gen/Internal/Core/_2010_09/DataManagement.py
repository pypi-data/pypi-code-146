from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DatasetAttrInfo(TcBaseObj):
    """
    This structure stores the criteria to query for datasets.
    
    :var attrName: The attribute name on the Dataset.
    :var attrValues: List of the Dataset attributes
    """
    attrName: str = ''
    attrValues: List[str] = ()


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    This structure contains the dataset instance and reference file ticket.
    
    :var dataset: The Dataset object.
    :var referenceFileTicket: The file ticket to download the reference file.
    """
    dataset: Dataset = None
    referenceFileTicket: str = ''


@dataclass
class DatasetFileQueryInfo(TcBaseObj):
    """
    Stores the information to query for Dataset reference files.
    
    :var clientID: A unique string used to identify return data elements and partial errors associated with this input
    structure.
    :var datasetType: The Dataset type name
    :var referenceTypes: A list of Dataset reference type names
    :var attrInfo: The criteria to query for Dataset objects
    """
    clientID: str = ''
    datasetType: str = ''
    referenceTypes: List[str] = ()
    attrInfo: List[DatasetAttrInfo] = ()


@dataclass
class DatasetFilesOutput(TcBaseObj):
    """
    This structure stores the Dataset files for the given Dataset type and reference type.
    
    :var clientID:  The unmodified value from the input clientId. This can be used by the caller to indentify this data
    structure with the source input data.
    :var datasetType: The Dataset type name for which the file is being returned.
    :var datasetReferenceFileInfo: The list of Dataset files with their reference type information.
    """
    clientID: str = ''
    datasetType: str = ''
    datasetReferenceFileInfo: List[DatasetReferenceFileInfo] = ()


@dataclass
class DatasetFilesResponse(TcBaseObj):
    """
    The Dataset reference files returned from the server.
    
    :var datasetFilesOutput: The list of Dataset reference files.
    :var serviceData: Standard 'ServiceData' member
    """
    datasetFilesOutput: List[DatasetFilesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class DatasetReferenceFileInfo(TcBaseObj):
    """
    This structure stores the dataset files for the reference type for 'DatasetFilesOutput' structure.
    
    :var datasetReferenceTypeName: The Dataset reference type name for which the file is being returned.
    :var datasetFiles: The list of Dataset files.
    """
    datasetReferenceTypeName: str = ''
    datasetFiles: List[DatasetFileInfo] = ()
