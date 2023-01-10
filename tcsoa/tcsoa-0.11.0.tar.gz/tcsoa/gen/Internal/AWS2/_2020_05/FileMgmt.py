from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetFilesAndTicketsInfoResponse(TcBaseObj):
    """
    The GetFilesAndTicketsInfoResponse holds the list of names and their FMS tickets for the first file as primary
    named reference associated with the Dataset and ServiceData.
    
    The response array will have a structure of file name and FMS Ticket that corresponds to every input Dataset object
    array in the same order. In case an element in the input array does not have an associated file name and ticket
    information , the response array will have a structure of blank string for that input and this input object will be
    passed in the partialError.
    
    :var serviceData: ServiceData for the operation.
    :var output: Response object containing a list of file name and its corresponding FMS ticket .
    """
    serviceData: ServiceData = None
    output: List[FileNameTicketOut] = ()


@dataclass
class FileNameTicketOut(TcBaseObj):
    """
    The FileNameTicketOut structure holds the file name and its corresponding FMS ticket for the first file of the
    primary named reference associated with the Dataset.
    
    :var fileName: The file name of the first file against the primary named reference associated with every Dataset
    :var fileTicket: FMS ticket of the first file against the primary named reference associated with every Dataset.
    """
    fileName: str = ''
    fileTicket: str = ''
