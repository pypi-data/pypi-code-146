from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReplaceFileInput(TcBaseObj):
    """
    This structure contains the input to the 'replaceFiles' operation.  This includes the transient volume write ticket
    used to upload the new file.  This is the FMS write ticket issued by the 'getTransientFileTicketsForUpload'
    operation.  The 'replaceFiles' operation uses this ticket to locate the data file in the transient volume.  This
    structure also includes a flag to indicate if the original file name should be updated.
    
    :var imanFile: The ImanFile object whose file is to be replaced.
    :var newFileTicket: The transient file write ticket that was used to upload the new file to the transient volume.
    :var retainOriginalFileName: If set to true, the original file name of the ImanFile object will not be changed.  If
    false, the original file name will be changed to the file name of the new file as set in 'newFileTicket'.
    """
    imanFile: ImanFile = None
    newFileTicket: str = ''
    retainOriginalFileName: bool = False
