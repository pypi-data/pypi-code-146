from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, WorkspaceObject, StructureContext, CfgActivityLine, CfgAttachmentLine
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GetAttachmentLineChildrenResponse(TcBaseObj):
    """
    response of getAttachmentLineChildren method - a map of input line to it's children
    
    :var lines: map of parent attachmentline to child lines.
    :var serviceData: any partial errors to be returned.
    """
    lines: AttachmentLineToChildLinesMap = None
    serviceData: ServiceData = None


@dataclass
class GetBOMLineActivitiesResponse(TcBaseObj):
    """
    Response of getBOMLineActivities method. lines represent the activities for supplied bomline. servicesData to
    capture partialErrors.
    
    :var lines: vector of bomline to activities map
    :var serviceData: serviceData object to capture partial errors.
    """
    lines: BOMLineToActivitiesMap = None
    serviceData: ServiceData = None


@dataclass
class GetBOMLineAttachmentsResponse(TcBaseObj):
    """
    Response of getBOMLineAttachments method. lines represent the attachmentlines for supplied bomline. servicesData to
    capture partialErrors.
    
    :var lines: bomline to attachmentlines map
    :var serviceData: serviceData to capture partial errors.
    """
    lines: BOMLineToAttachmentLinesMap = None
    serviceData: ServiceData = None


@dataclass
class GetStructureContextActivityLinesResponse(TcBaseObj):
    """
    return structure of getStructureContextActivityLinesResponse. lines has the map of sc to activitylines, and
    serviceData has partial errors.
    
    :var lines: map of sc to activity lines
    :var serviceData: for reporting partial errors.
    """
    lines: StructureContextActivityLinesMap = None
    serviceData: ServiceData = None


@dataclass
class GetStructureContextTopLinesResponse(TcBaseObj):
    """
    response of getStructureContextTopLines methods. lines member has the map of StructureContext to it's toplines, and
    serviceData member has any partial errors.
    
    :var lines: map of SC to it's lines
    :var serviceData: serviceData to hold partial errors
    """
    lines: StructureContextToLinesMap = None
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateAttachmentsData(TcBaseObj):
    """
    Structure to specify input data for createOrUpdateAttachments
    
    :var bomLine: bomline - the top line of the attachment window. Optional if attLine is going to be specified.
    :var attLine: Parent attachment line-under which the new one will be created or updated. Overrides bomLine member
    if specified.
    :var objects: relation string to the workspaceobject secondaries map
    """
    bomLine: BOMLine = None
    attLine: CfgAttachmentLine = None
    objects: ContextToSecondaryObjectsMap = None


"""
map of attachmentline to it's child attachmentlines
"""
AttachmentLineToChildLinesMap = Dict[CfgAttachmentLine, List[CfgAttachmentLine]]


"""
map of bomline to it's mfg activity lines
"""
BOMLineToActivitiesMap = Dict[BOMLine, List[CfgActivityLine]]


"""
map of bomline to it's attachment lines
"""
BOMLineToAttachmentLinesMap = Dict[BOMLine, List[CfgAttachmentLine]]


"""
map of StructureContext to Activities,
"""
StructureContextActivityLinesMap = Dict[StructureContext, List[CfgActivityLine]]


"""
map of StructureContext Object to it's toplines
"""
StructureContextToLinesMap = Dict[StructureContext, List[BOMLine]]


"""
the map if relation string to the secondary workspace objects that defines the attachment(s)
"""
ContextToSecondaryObjectsMap = Dict[str, List[WorkspaceObject]]
