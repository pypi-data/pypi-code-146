from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileTicketsResponse(TcBaseObj):
    """
    Holds a 'ServiceData' object and a map (ImanFile, string) of read tickets.  If the request completes successfully,
    each input ImanFile object will appear as a key in the output map
    and the string value associated with each entry will be a valid FMS ticket associated with that ImanFile.  Returned
    from the 'getFileReadTickets' operation.
    
    :var tickets: A map of the input ImanFile objects to FMS tickets used to access files in the Teamcenter volume.
    :var serviceData: The Teamcenter Services structure used to return status of the operation.  Any errors that
    occurred during the operation are returned here.
    """
    tickets: TicketMap = None
    serviceData: ServiceData = None


@dataclass
class GetDatasetWriteTicketsInputData(TcBaseObj):
    """
    A vector of 'GetDatasetWriteTicketsInputData' structures which holds the Dataset objects and related
    'DatasetFileTicketInfo'.  The calling client must construct this input.
    
    :var dataset: The Dataset object to which the ImanFile object(s) representing the data files uploaded to the
    Teamcenter volume are associated.
    :var createNewVersion: If this flag is true, a new DatasetRevision will be created to reference the new set of
    files uploaded to the Teamcenter volume.  Any existing DatasetRevision will be unaltered, but the new
    DatasetRevision will have the files attached as named references.
    If this flag is false, the uploaded files are attached to the current most recent DatasetRevision of this Dataset
    as named references.
    
    :var datasetFileInfos: A vector of 'DatasetFileInfo' structures where each contains information specific to each
    Dataset to be created.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileInfos: List[DatasetFileInfo] = ()


@dataclass
class GetDatasetWriteTicketsResponse(TcBaseObj):
    """
    Holds a 'ServiceData' object and a vector of dataset commit information.  If the request completes successfully,
    the information in the vector can be used to commit the Dataset to the database.
    
    :var commitInfo: A vector of 'CommitDatasetFileInfo' structures.
    :var serviceData: The Teamcenter Services structure used to return status of the operation.  Any errors that
    occurred during the operation are returned here.
    """
    commitInfo: List[CommitDatasetFileInfo] = ()
    serviceData: ServiceData = None


@dataclass
class CommitDatasetFileInfo(TcBaseObj):
    """
    Used in the 'commitDatasetFiles' operation to pass information for committing ImanFile instances uploaded to a
    Teamcenter volume with the associated Dataset instances.
    
    :var dataset: The Dataset object to which the ImanFile object(s) representing the data files uploaded to the
    Teamcenter volume.
    :var createNewVersion: If this flag is true, a new DatasetRevision will be created to reference the new set of
    files uploaded to the Teamcenter volume.  Any existing DatasetRevision will be unaltered, but the new
    DatasetRevision will have the files attached as named references.
    If this flag is false, the uploaded files are attached to the current most recent DatasetRevision of this Dataset
    as named references.
    
    :var datasetFileTicketInfos: A vector of DatasetFileTicketInfo objects representing each ImanFile object attached
    to the given Dataset as a named reference.
    """
    dataset: Dataset = None
    createNewVersion: bool = False
    datasetFileTicketInfos: List[DatasetFileTicketInfo] = ()


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    The structure defining the basic information for a file to be uploaded to a Dataset.
    
    :var clientId: An identifier defined by the caller to track the related object.
    
    :var fileName: The name of the file to be uploaded. 
    This is the filename only and should not contain the path to the filename.
    Exception: When used with the 'FileManagementUtility::putFiles()' operation, this should contain the full path and
    file name.
    :var namedReferencedName: The named reference relation to the file.
    :var isText: A flag to indicate if the file is text (TRUE) or binary (FALSE).
    :var allowReplace: A flag to indicate if the file may be overwritten (TRUE) or not (FALSE).
    """
    clientId: str = ''
    fileName: str = ''
    namedReferencedName: str = ''
    isText: bool = False
    allowReplace: bool = False


@dataclass
class DatasetFileTicketInfo(TcBaseObj):
    """
    A structure representing an ImanFile object attached to a given Dataset as a named reference.
    
    :var datasetFileInfo: The structure defining the basic information for a file to be uploaded to a Dataset.
    :var ticket: The FMS write ticket used to transfer the file to the appropriate Teamcenter volume.
    """
    datasetFileInfo: DatasetFileInfo = None
    ticket: str = ''


"""
A map of the input ImanFile objects to FMS read tickets used to read the file from the Teamcenter volume.
"""
TicketMap = Dict[ImanFile, str]
