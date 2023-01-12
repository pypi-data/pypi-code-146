from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CommitReplacedFileInfo(TcBaseObj):
    """
    The FMS write ticket with which the replacement data file was uploaded to the transient volume.  This is the FMS
    write ticket issued by the 'FileManagementService::getTransientFileTicketsForUpload'() operation.  The
    'FileManagementService::commitReplacedFiles'() operation uses this ticket to locate the data file in the transient
    volume.
    
    :var replaceFileTicket: File write ticket.
    :var newOriginalFileName: If specified, this is a name for the new file.  If this filename is an empty string, the
    existing filename in the volume is used.
    :var imanFile: This is the ImanFile object with which the transient volume data file should be associated.
    """
    replaceFileTicket: str = ''
    newOriginalFileName: str = ''
    imanFile: ImanFile = None
