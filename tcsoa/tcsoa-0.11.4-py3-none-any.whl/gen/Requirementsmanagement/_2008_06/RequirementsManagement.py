from __future__ import annotations

from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class GetContentInput1(TcBaseObj):
    """
    'GetContentInput1' structure represents the parameters required to open requirement in MSWord.
    
    :var objectToProcess: Fulltext object that user want to view.
    :var applicationFormat: For viewing and editing content without template this parameter should be MSWordXML.
    For viewing and editing object by applying template this parameter should be MSWordXMLLive.
    
    
    :var templateId: This parameter is not used currently.
    :var applyTemplates: For viewing and editing content without template this parameter should be false.
    For viewing and editing object by applying template this parameter should be true.
    """
    objectToProcess: WorkspaceObject = None
    applicationFormat: str = ''
    templateId: str = ''
    applyTemplates: bool = False
