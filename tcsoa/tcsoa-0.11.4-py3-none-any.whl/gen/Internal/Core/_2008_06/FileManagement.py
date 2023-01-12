from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import ImanFile


@dataclass
class FileInfo(TcBaseObj):
    """
    File Info
    
    :var clientFileId: Unique Identifier defined by user to track files
    :var refName: Named Reference relation to file.
    :var isText: Flag to indicate if file is text(TRUE) or binary(FALSE).
    :var fileName: Name of file to be uploaded. Filename with extension only.
    """
    clientFileId: str = ''
    refName: str = ''
    isText: bool = False
    fileName: str = ''


@dataclass
class FileInfoTicket(TcBaseObj):
    """
    Structure containing FMS ticket
    
    :var clientFileId: unique Identifier defined by user to track files
    :var ticket: FMS write ticket for the file uploaded.
    """
    clientFileId: str = ''
    ticket: str = ''


@dataclass
class FileTicketsResponse(TcBaseObj):
    """
    Holds a 'ServiceData' object and a map of write tickets information.  If the request completes successfully, the
    information in the vector can be used to upload the files to  the Teamcenter volume.  Returned from the
    'getWriteTickets' operation.
    
    :var tickets: A map of the 'FileInfoTicket' struct to the clientId.
    :var serviceData: The Teamcenter Services structure used to return status of the operation.  Any errors that
    occurred during the operation are returned here.
    """
    tickets: TicketMap = None
    serviceData: ServiceData = None


@dataclass
class GetFileTransferTicketsResponse(TcBaseObj):
    """
    Holds a 'ServiceData' object, a map (ImanFile, string) of read tickets, and a map (ImanFile, string) of write
    tickets.  If the request completes successfully, each input ImanFile object will appear as a key in both the
    'readTickets' and 'writeTickets' output maps, and the string values associated with each of those entries will be
    valid FMS tickets associated with that ImanFile.
    
    :var readTickets: A map of the input ImanFile objects to FMS read tickets used to read the file from the Default
    Local Volume.  If the ImanFile object is not eligible for StoreAndForward, then this map will not contain a read
    ticket for the ImanFile object.  The map returned may contain no elements.
    :var writeTickets: A map of the input ImanFile objects to FMS write tickets used to write the file to the Default
    Volume.  If the ImanFile object is not eligible for StoreAndForward, then this map will not contain a write ticket
    for the ImanFile object.  The map returned may contain no elements.
    :var serviceData: The Teamcenter Services structure used to return status of the operation.  Any errors that
    occurred during the operation are returned here.
    """
    readTickets: TransferTicketMap = None
    writeTickets: TransferTicketMap = None
    serviceData: ServiceData = None


@dataclass
class GetRegularFileWriteTicketsInput(TcBaseObj):
    """
    Used to input information to the getRegularFileTicketsForUpload()
    function.  The struct holds the array of RegularFileInfo and
    a string client id information.
    
    :var regularFileInfos: The structure holds the file name and text/binary file information for each file to be
    uploaded to a Teamcenter volume.
    :var clientId: The calling client can supply a string to identify each individual file in the maps returned from
    this and related operations.  The 'clientId' should be unique for each ImanFile instance, but this is apparently
    not enforced by this operation.
    """
    regularFileInfos: List[RegularFileInfo] = ()
    clientId: str = ''


@dataclass
class GetRegularFileWriteTicketsResponse(TcBaseObj):
    """
    Used to return information from the getRegularFileTicketsForUpload()
    function.  The struct holds the Servicedata and a map of (string)
    file names and (string) write tickets.
    
    :var writeTickets: Map of (string) file names (from the 'RegularFileInfo' input) to (string) write tickets (output).
    :var serviceData: serviceData
    """
    writeTickets: WriteTicketsMap = None
    serviceData: ServiceData = None


@dataclass
class RegularFileInfo(TcBaseObj):
    """
    Used to input information to the getRegularFileTicketsForUpload()
    function.  The struct holds the file name and text/binary file information.
    
    :var fileName: File name of the file which needs to be uploaded.  This is typically a full path to the file being
    uploaded.
    :var isText: Boolean to define if the file is binary or text file. True if the file is a text file, false otherwise.
    """
    fileName: str = ''
    isText: bool = False


@dataclass
class UpdateImanFileCommitsResponse(TcBaseObj):
    """
    Holds a 'ServiceData' object, a map (ImanFile, integer) of delays, and a map (ImanFile, string) of write tickets
    used to cleanup the files from the initial Store and Forward volume.  If the request completes successfully, an
    ImanFile object corresponding to each input file GUID will appear as a key in both the delays and writeTickets
    output maps, and the string values associated with each of the writeTickets entries will be valid FMS read tickets
    associated with that ImanFile.  See the structure description for more information.
    
    :var delays: A mapping of ImanFile objects to the time delay before the tickets corresponding to that ImanFile
    object times out.  If the corresponding data file has not been successfully transferred to the new volume and
    committed to the new volume, then this map will not contain a delay value for the ImanFile object.  The map
    returned may contain no elements.
    :var writeTickets: A mapping of ImanFile objects to FMS write tickets used to remove the transferred file from the
    Default Local Volume in the cleanup dispatcher task.  If the corresponding data file has not been successfully
    transferred to the new volume and committed to the new volume, then this map will not contain a write ticket for
    the ImanFile object.  The map returned may contain no elements.
    :var serviceData: The Teamcenter Services structure used to return status of the operation.  Any errors that
    occurred during the operation are returned here.
    """
    delays: DelayMap = None
    writeTickets: TransferTicketMap = None
    serviceData: ServiceData = None


@dataclass
class WriteTicketsInput(TcBaseObj):
    """
    Holds information about the Dataset (datasettype, version) and the list of files (marked by unique identifier) to
    be uploaded in the desired datasetType.
    
    :var clientId: Unique identifier defined by user to track each file.
    :var datasetTypeName: Desired datasetType of the Dataset to upload the files.
    :var version: Set this value to one(1) in the use case where a new Dataset is going to be created.  Otherwise, it
    should be set to one more than the current highest version number of the existing Dataset, which must be determined
    by the caller. This value is used for filename generation in the Teamcenter volume. (Note that the version number
    and the version limit are not necessarily the same.)
    :var fileInfos: A vector of 'FileInfo' structures where each contains information specific to each file that will 
    be uploaded to the Dataset via Visualization services.
    """
    clientId: str = ''
    datasetTypeName: str = ''
    version: int = 0
    fileInfos: List[FileInfo] = ()


@dataclass
class CommitUploadedRegularFilesInput(TcBaseObj):
    """
    Used to input information to the commitRegularFiles()
    function.  The struct holds string file name, string file ticket and
    a string client id information.
    
    :var fileName: fileName
    :var fileTicket: fileTicket
    :var clientId: clientId
    """
    fileName: str = ''
    fileTicket: str = ''
    clientId: str = ''


@dataclass
class CommitUploadedRegularFilesResponse(TcBaseObj):
    """
    Used to return information from the commitRegularFiles()
    function.  The struct holds the Servicedata and a map of (string)
    file names and ImanFileImpl objects.
    
    :var files: files
    :var serviceData: serviceData
    """
    files: ImanFilesMap = None
    serviceData: ServiceData = None


"""
A mapping of ImanFile objects to the time delay before the tickets corresponding to that ImanFile object times out.  If the corresponding data file has not been successfully transferred to the new volume and committed to the new volume, then this map will not contain a delay value for the ImanFile object.  The map returned may contain no elements.
"""
DelayMap = Dict[ImanFile, int]


"""
Map of (string) file names and ImanFile objects.
"""
ImanFilesMap = Dict[str, ImanFile]


"""
A map of the 'FileInfoTicket' struct to the clientId.
"""
TicketMap = Dict[str, List[FileInfoTicket]]


"""
A map of the input ImanFile objects to FMS read tickets used to read the file from the Default Local Volume or write tickets used to write the file to the Default Volume, or write tickets used to remove the transferred file from the Default Local Volume in the cleanup dispatcher task (depending on the context in which this map is used).  If the ImanFile object is not eligible for StoreAndForward, or has not been successfully transferred to the new volume and committed to the new volume, then this map will not contain a read or write ticket for the ImanFile object.  The map returned may contain no elements.
"""
TransferTicketMap = Dict[ImanFile, str]


"""
Map of (string) file names (from the 'RegularFileInfo' input) to (string) write tickets (output).
"""
WriteTicketsMap = Dict[str, str]
