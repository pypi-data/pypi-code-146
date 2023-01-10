from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportObjectsToPLMXMLResponse(TcBaseObj):
    """
    The response for 'exportObjectsToPLMXML' operation. It holds the file ticket for the exported XML file, file ticket
    for the export log file, file tickets  for the dataset named reference files, and any partial failures.
    
    :var xmlFileTicket: The FMS ticket is used to get the generated PLMXML file.
    :var logFileTicket: The FMS ticket is used to get the generated export log file.
    :var namedRefFileTickets: The FMS tickets are used to get the dataset named  reference files. On Teamcenter
    Services client, the files must be loaded into the directory along with the PLMXML file. And the directory must
    have the same name as the PLMXML file without the file extension name.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors is used
    to report any partial failures.
    """
    xmlFileTicket: FileTicket = None
    logFileTicket: FileTicket = None
    namedRefFileTickets: List[FileTicket] = ()
    serviceData: ServiceData = None


@dataclass
class FileTicket(TcBaseObj):
    """
    To represent a  file ticket and its original file name.
    
    :var ticket: The FMS file Ticket.
    :var fileName: The original file name.
    """
    ticket: str = ''
    fileName: str = ''


@dataclass
class ImportObjectsFromPLMXMLResponse(TcBaseObj):
    """
    The response for 'importObjectsFromPLMXML' operation. It holds the file ticket for the import log file, and any
    partial failures.
    
    :var logFileTicket: The FMS ticket is used to get the generated import log file.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    logFileTicket: FileTicket = None
    serviceData: ServiceData = None
