from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportToApplicationInputData2(TcBaseObj):
    """
    The ExportToApplicationInput2 represents the data required to export selected objects to MSWord or MSExcel.
    
    :var objectsToExport: The list of Teamcenter business objects to be exported to MSWord or MSExcel.
    :var targetObjectsToExport: The list of Teamcenter business objects to be exported which acts as target objects
    used for comparing the contents. This is an optional parameter and can be empty.
    :var attributesToExport: The list of attributes to export. This is an optional parameter which can be empty.
    :var applicationFormat: The application formats supported are :
    "MSExcel","MSWordXMLLive","MExcelLive","MSExcelReimport","MSWordCompare","HTML"
    :var templateName: The name of the MSWord or MSExcel template.
    """
    objectsToExport: List[BusinessObject] = ()
    targetObjectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateName: str = ''


@dataclass
class ExportToApplicationResponse2(TcBaseObj):
    """
    This structure contains the html contents of the input SpecElement objects or a file ticket of .docm or .xlsm file.
    
    :var transientFileReadTickets: The transient file read tickets for the exported file.
    :var contents: The HTML contents associated to the objects sent as input to the service operation. This is an
    optional parameter in the response . The parameter targetObjectsToExport in ExportToApplicationInput2 is not used
    to output the HTML contents.
    :var serviceData: The ServiceData. If an error occurs then ServiceData will contain partial error such as error
    generating transient file read ticket due to a configuration issue at the server.
    """
    transientFileReadTickets: List[str] = ()
    contents: List[str] = ()
    serviceData: ServiceData = None
