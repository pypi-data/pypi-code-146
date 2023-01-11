from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportConfiguredNXAssemblyInfo(TcBaseObj):
    """
    Contains the BOMLine object reference and naming format.
    
    :var bomline: Object reference of the BOMLine.
    :var namingFormat: The naming format can be defined by the user in the User Interface.  The option is to Add a
    Prefix or to Auto translate.
    """
    bomline: BOMLine = None
    namingFormat: str = ''


@dataclass
class ExportConfiguredNXAssemblyOutput(TcBaseObj):
    """
    Contains zipfileticket, logfileticket, and a list of 'ExportConfiguredNXAssemblyInfo' structures.  The
    'ExportConfiguredNXAssemblyInfo' structure contains the input BOMLine object and the naming format
    
    :var transientZipFileReadTicket: Exported zip file ticket.
    :var transientLogFileReadTicket: Exported log file ticket.
    :var bomline: Input BOMLine.
    """
    transientZipFileReadTicket: str = ''
    transientLogFileReadTicket: str = ''
    bomline: BOMLine = None


@dataclass
class ExportConfiguredNXAssemblyResponse(TcBaseObj):
    """
    Consists of the output and the 'serviceData'
    The output will be returned as a list of 'ExportConfiguredNXAssemblyOutput' objects each of which contains
    zipfileticket, logfileticket, and a list of 'ExportConfiguredNXAssemblyInfo' structures.  The
    'ExportConfiguredNXAssemblyInfo' structure contains the input BOMLine object and the naming format.
    
    
    :var output: A list of type 'ExportConfiguredNXAssemblyOutput'
    :var serviceData: The input BOMLine and the error message.
    """
    output: List[ExportConfiguredNXAssemblyOutput] = ()
    serviceData: ServiceData = None
