from __future__ import annotations

from tcsoa.gen.GlobalMultiSite._2010_04.ImportExport import FileTicket
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportObjectsFromPLMXMLWithDSMResp(TcBaseObj):
    """
    The response for importObjectsFromPLMXMLWithDSM operation. It holds the file read tickets for uploading the Dataset
    named reference files, the file read ticket for the import log file, and any partial failures.
    
    :var namedRefPLMDFileTickets: The FMS read tickets are used to upload the Dataset named reference files. These
    files are in .plmd format. On Teamcenster services client, files must be uploaded using these tickets thru Data
    Share Manager system after the calling of this operation. The API DownloadFilesWithDM from IFileManager class can
    be used to perform the upload.
    :var logFileTicket: The FMS read ticket is used to download the generated import log file from the FMS transient
    volume. The API DownLoadTransientFile from FmsFileCacheProxy can be used to perform the download.
    :var serviceData: The service data contains the errors.
    """
    namedRefPLMDFileTickets: List[str] = ()
    logFileTicket: FileTicket = None
    serviceData: ServiceData = None
