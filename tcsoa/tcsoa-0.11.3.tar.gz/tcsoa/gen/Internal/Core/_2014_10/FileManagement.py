from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPlmdFileTicketResponse(TcBaseObj):
    """
    Return structure for the getPlmdFileTicketForUpload and getPlmdFileTicketForDownload operations.
    
    :var ticket: The requested plmd file transient ticket.
    :var serviceData: Holds any partial errors that may have occurred during the operation.
    """
    ticket: str = ''
    serviceData: ServiceData = None


@dataclass
class DatashareManagerDownloadInfo(TcBaseObj):
    """
    Information about a file to be downloaded asynchronously via Datashare Manager 
    
    :var dataset: The Dataset object from which the ImanFile object(s) representing the data files that need to be
    downloaded from the Teamcenter volume.
    :var imanFile: A ImanFile object that need to be downloaded from a Teamcenter volume.
    :var absoluteFilePath: The absolute file path of the file being downloaded on the client host.The value can be set
    to an empty  string("") to download the file to the default staging directory on the client host.
    """
    dataset: Dataset = None
    imanFile: ImanFile = None
    absoluteFilePath: str = ''


@dataclass
class DatashareManagerUploadInfo(TcBaseObj):
    """
    Information about a file to be uploaded asynchronously via Datashare Manager.
    
    :var dataset: The Dataset object from which the ImanFile object(s) representing the data files that need to be
    uploaded from the Teamcenter volume.
    :var namedReferenceName: The named reference realtion to the ImanFile object file.
    :var absoluteFilePath: The absolute file path of the file being uploaded on the client host
    """
    dataset: Dataset = None
    namedReferenceName: str = ''
    absoluteFilePath: str = ''
