from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetTransientTicketsDownloadInput(TcBaseObj):
    """
    GetTransientTicketsDownloadInput structure contains a transient file write ticket for which a read ticket is to be
    obtained. If deleteFlag is true then the file is deleted from temporary storage after it is read.
    
    :var transientFileWriteTicket: Transient file write ticket.
    :var deleteFlag: If true, the file is deleted from temporary storage after it is read.
    """
    transientFileWriteTicket: str = ''
    deleteFlag: bool = False


@dataclass
class GetTransientTicketsDownloadResponse(TcBaseObj):
    """
    GetTransientTicketsDownloadResponse structure contains transient file read tickets and corresponding failure codes
    and error strings.
    
    :var transientFileReadTickets: A list of transient file read tickets.
    :var serviceData: Service Data in which the partial errors are communicated to the client.
    """
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None
