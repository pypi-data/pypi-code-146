from __future__ import annotations

from tcsoa.gen.BusinessObjects import ItemRevision, Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileInfo(TcBaseObj):
    """
    File information
    
    :var clientId: The client id
    :var fileName: The file name
    :var namedReferencedName: The Dataset named reference information.
    :var isText: True means Text format, otherwise it is Binary format.
    :var allowReplace: Allow to replace or not.
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False


@dataclass
class FileTicketInfo(TcBaseObj):
    """
    File ticket information structure
    
    :var fileInfo: The file information.
    :var ticket: The FMS ticket.
    """
    fileInfo: FileInfo = None
    ticket: str = ''


@dataclass
class GetAdditionalFilesForCheckinInputs(TcBaseObj):
    """
    The structure contains the item revision and file names.
    
    :var itemRevision: The item revision
    :var filenames: The full file path and file names.
    """
    itemRevision: ItemRevision = None
    filenames: List[str] = ()


@dataclass
class GetAdditionalFilesForCheckinOutputs(TcBaseObj):
    """
    The structure contains the item revision and vector of CommitDatasetInfo structure.
    
    :var itemRevision: The item revision
    :var datasetInfos: The dataset information.
    """
    itemRevision: ItemRevision = None
    datasetInfos: List[CommitDatasetInfo] = ()


@dataclass
class GetAdditionalFilesForCheckinOutputsResponse(TcBaseObj):
    """
    The structure contains vector of GetAdditionalFilesForCheckinOutputs and the serviceData.
    
    :var outs: The vector of GetAdditionalFilesForCheckinOutputs.
    :var serviceData: The service data.
    """
    outs: List[GetAdditionalFilesForCheckinOutputs] = ()
    serviceData: ServiceData = None


@dataclass
class GetCheckinModeAndFilesOutputs(TcBaseObj):
    """
    The structure contains the ItemRevision and vector of file names and the check in mode.
    
    :var itemRevision: The ItemRevision business object
    :var filenames: The list of file names that are currently downloaded locally when the ItemRevision was checked out
    :var mode: The CheckIn mode
    """
    itemRevision: ItemRevision = None
    filenames: List[str] = ()
    mode: str = ''


@dataclass
class GetCheckinModeAndFilesOutputsResponse(TcBaseObj):
    """
    The structure contains vector of getCheckinModeAndFilesOutput structure and serviceData.
    
    :var outs: The list of Struct 'GetCheckinModeAndFilesOutputs'
    :var serviceData: The Service Data. Partial errors and failures are updated and returned through this object
    """
    outs: List[GetCheckinModeAndFilesOutputs] = ()
    serviceData: ServiceData = None


@dataclass
class PostCreateInfo(TcBaseObj):
    """
    Post create information
    
    :var itemRevision: The ItemRevision business object that is newly created
    :var commitInfos: The list of 'CommitDatasetInfo' struct
    """
    itemRevision: ItemRevision = None
    commitInfos: List[CommitDatasetInfo] = ()


@dataclass
class PostCreateInputs(TcBaseObj):
    """
    Document Management Post Create Inputs
    
    :var clientId: The client id
    :var itemRevision: The newly created ItemRevision
    :var fileNames: Attached file names
    """
    clientId: str = ''
    itemRevision: ItemRevision = None
    fileNames: List[str] = ()


@dataclass
class PostCreateResponse(TcBaseObj):
    """
    Post Create Response structure
    
    :var output: List of 'PostCreateInfo' struct
    :var serviceData: The Service Data. Partial errors and failures are updated and returned through this object
    """
    output: List[PostCreateInfo] = ()
    serviceData: ServiceData = None


@dataclass
class CommitDatasetInfo(TcBaseObj):
    """
    Commit dataset information
    
    :var dataset: The Dataset created.
    :var dsTypeName: The Dataset type name.
    :var fileTicketInfo: The file ticket information.
    """
    dataset: Dataset = None
    dsTypeName: str = ''
    fileTicketInfo: FileTicketInfo = None
