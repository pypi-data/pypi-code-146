from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportSearchResultsResponse(TcBaseObj):
    """
    This structure contains the file ticket of exported file. . 
    
    The following partial errors may be returned: 
    141401    Unable to export object "<Object name>" with UID "<UID>". 
    141402    selectedObjectUIDs list cannot be empty when exporting selected objects.
    141403    The column configuration must be specified to export search results.
    141404    An internal error has occurred which caused the object export operation to fail.
    141405    The search input criteria cannot contain empty properties when exporting all objects.
    141406    The supported application format is MSExcelX.
    
    :var serviceData: The ServiceData. If an error occurs then ServiceData will contain partial error such as error
    generating transient file read ticket due to a configuration issue at the server.
    :var transientFileReadTickets: A list of transient file read tickets for the exported file.
    """
    serviceData: ServiceData = None
    transientFileReadTickets: List[str] = ()
