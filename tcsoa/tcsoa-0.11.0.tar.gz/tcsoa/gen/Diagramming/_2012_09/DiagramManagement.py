from __future__ import annotations

from tcsoa.gen.BusinessObjects import TransferMode, Fnd0DiagramTmplRevision
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateOrUpdateTemplateInputInfo1(TcBaseObj):
    """
    CreateOrUpdateTemplateInputInfo1 structure represents the parameters required to create a diagram template.
    
    :var available: If true, the Diagram Template is available for use.
    :var tmplStencilFileTickets: A list of FMS tickets to the Diagram tool specific stencils or Template files.
    :var tmplMappingFileTicket: FMS ticket to the Property Map xml file.
    :var membershipRule: The Transfer mode, which will be used for traversing the structure for the diagram root object.
    :var relationRule: The Relation Rule which is the list of relations between the objects shown on the diagram.
    :var diagramTmplRev: The updated template object.
    :var propNamevsPropValueMap: A map of property names and values (string/string). Valid keys are Description, Name,
    templateName and ID.
    :var hidePorts: If true, the interface shapes will not be shown on the created diagram.
    """
    available: bool = False
    tmplStencilFileTickets: List[str] = ()
    tmplMappingFileTicket: str = ''
    membershipRule: TransferMode = None
    relationRule: List[str] = ()
    diagramTmplRev: Fnd0DiagramTmplRevision = None
    propNamevsPropValueMap: DiagramTemplatePropNamevsPropValueMap = None
    hidePorts: bool = False


"""
This  map contains the property name and its value for a Diagram Template
"""
DiagramTemplatePropNamevsPropValueMap = Dict[str, str]
