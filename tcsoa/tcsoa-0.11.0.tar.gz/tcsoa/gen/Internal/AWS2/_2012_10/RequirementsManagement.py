from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SetContentInput(TcBaseObj):
    """
    DEPRECATED: SetContentInput structure represents the parameters required to set the contents to the FullText object.
    
    :var objectToProcess: SpecElement Revision or FullText object.
    :var bodyText: Value of the new body text on the FullText object.
    :var contentType: Value of the content type on the FullText object.
    """
    objectToProcess: WorkspaceObject = None
    bodyText: str = ''
    contentType: ContentTypes = None


@dataclass
class ExportToApplicationInputData(TcBaseObj):
    """
    Export to application input data
    
    :var objectsToExport: Objects to Export.
    :var attributesToExport: Attributes to export.
    :var applicationFormat: Application Format
    :var templateId: Template ID
    """
    objectsToExport: List[BusinessObject] = ()
    attributesToExport: List[str] = ()
    applicationFormat: str = ''
    templateId: str = ''


@dataclass
class ExportToApplicationResponse(TcBaseObj):
    """
    ExportToApplicationResponse
    
    :var transientFileReadTickets: transientFileReadTickets
    :var outlineMap: outline map
    :var serviceData: service data
    """
    transientFileReadTickets: List[str] = ()
    outlineMap: OutlineMap = None
    serviceData: ServiceData = None


class ContentTypes(Enum):
    """
    DEPRECATED: ContentTypes enumeration represents the valid content types of the FullText object.
    """
    HTML = 'HTML'
    PLAINTEXT = 'PLAINTEXT'


"""
Outline Map
"""
OutlineMap = Dict[str, BusinessObject]
