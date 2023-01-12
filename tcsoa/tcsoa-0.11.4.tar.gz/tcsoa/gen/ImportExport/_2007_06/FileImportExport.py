from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportToApplicationInputData(TcBaseObj):
    """
    The ExportToApplicationInputData structure represents all of the data necessary to export selected objects to
    Word/Excel.
    
    :var objectsToExport: The list of Teamcenter business objects to export.
    :var attributesToExport: The list of attributes to export.
    :var applicationFormat: The application format such as "'MSWordXML'", "'MSExcel'" and "'MSExcelLive'".
    
    Supported application format for this operation
    
    - MSWordXML     This format is used for exporting WorkspaceObject to static MSWord application.
    - MSExcel    This format is used for exporting Teamcenter objects to static MSExcel  application.
    - MSExcelLive    This format is used for exporting Teamcenter objects to Live MSExcel  application.
    
    
    :var templateId: The name of the Word/Excel template.
    """
    objectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateId: str = ''


@dataclass
class ExportToApplicationResponse(TcBaseObj):
    """
    ExportToApplicationResponse structure represents the output of export to application operation.
    It has information about file ticket for the exported file generated at the server.
    
    :var transientFileReadTickets: The transient file read tickets for the exported file.
    :var serviceData: The Service Data
    """
    transientFileReadTickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class ImportFromApplicationInputData(TcBaseObj):
    """
    This holds the data necessary to import an MSWord document into Teamcenter.
    
    :var transientFileWriteTicket: The file ticket of the. docx file to be imported into Teamcenter.
    :var applicationFormat: The supported application format is MSWordXML
    
    Supported application format for this operation
    
    - MSWordXML     This format is used for exporting WorkspaceObjects business objects to static MSWord application.
    
    
    :var createSpecElementType: The subtype of SpecElement to be created.
    """
    transientFileWriteTicket: str = ''
    applicationFormat: str = ''
    createSpecElementType: str = ''


@dataclass
class ImportFromApplicationResponse(TcBaseObj):
    """
    ImportFromApplicationResponse structure represents the output of import from application operation. It contains the
    UID of the BOMWindow after the document is imported to Teamcenter.
    
    :var resultObjects: The resultant objects which contains the UID of the BOMWindow created after the document is
    imported.  In case of importing templates, it contains the tag of the template.
    :var serviceData: The Service Data
    """
    resultObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None
