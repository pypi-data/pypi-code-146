from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetTransientFileTicketsResponse(TcBaseObj):
    """
    Holds the response returned from the 'getTransientFileTicketsForUpload' operation.
    
    :var transientFileTicketInfos: The requested transient files ticket information.
    :var serviceData: This contains the status of the operation.
    """
    transientFileTicketInfos: List[TransientFileTicketInfo] = ()
    serviceData: ServiceData = None


@dataclass
class TransientFileInfo(TcBaseObj):
    """
    Holds the basic information for a file to be uploaded.
    
    :var fileName: The name of the file. Path of the file should not be supplied.
    :var isBinary: True if the file is of binary type, false for text files.
    :var deleteFlag: True if the file should be deleted from temporary storage after it is read.
    """
    fileName: str = ''
    isBinary: bool = False
    deleteFlag: bool = False


@dataclass
class TransientFileTicketInfo(TcBaseObj):
    """
    Holds the file information with a ticket added.
    
    :var transientFileInfo: The unique identifier of the file to be uploaded.
    :var ticket: Holds the basic information for a file to be uploaded.
    """
    transientFileInfo: TransientFileInfo = None
    ticket: str = ''
