from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FileTicket(TcBaseObj):
    """
    The FileTicket struct.
    
    :var fileName: The file name.
    :var ticket: The FMS download ticket.
    """
    fileName: str = ''
    ticket: str = ''


@dataclass
class GetTemplateInput(TcBaseObj):
    """
    This structure defines the list of search criteria used to find the appropriate DMTemplates for the calling
    application.
    
    :var application: The name of the calling application.
    :var version: The version of the application. Optional.
    :var templateType: An application defined type value for different templates.
    :var templateUnits: The measurement units that the application uses.
    :var createItemType: The item Type to be created using the template files.
    :var nameReferenceName: The named reference name for the thumbnail file.
    :var relation: The relation to the thumbnail dataset.
    """
    application: str = ''
    version: str = ''
    templateType: str = ''
    templateUnits: str = ''
    createItemType: str = ''
    nameReferenceName: str = ''
    relation: str = ''


@dataclass
class GetTemplateOutput(TcBaseObj):
    """
    The GetTemplateOutput struct.
    
    :var templateRev: The document template revision.
    :var templateName: The document template name.
    :var dataset: The thumbnail dataset associated with the template.
    :var fileTicket: The file ticket for the FMS download of the thumbnail file.
    """
    templateRev: BusinessObject = None
    templateName: str = ''
    dataset: Dataset = None
    fileTicket: FileTicket = None


@dataclass
class GetTemplatesResponse(TcBaseObj):
    """
    The GetTemplateOutput struct.
    
    :var output: The list of references to struct GetTemplateOutput.
    :var serviceData: The Service Data. Partial errors and failures are updated and returned through this object.
    """
    output: List[GetTemplateOutput] = ()
    serviceData: ServiceData = None
