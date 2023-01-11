from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, StructureContext, WorkspaceObject
from dataclasses import dataclass


@dataclass
class GetStructureContextLinesResponse(TcBaseObj):
    """
    Get toplines from the BomWindow setup by StructureContext and any selected bomlines.
    
    :var topLines: Map of StructureContext to its toplines.
    For example, Product Structure and Process Structure top lines.
    :var selectedLines: Map of StructureContext to any selected child lines.
    Note: If the topline is selected this map will be empty.
    :var serviceData: Structure to capture any partial errors.
    """
    topLines: StructureContextToLinesMap2 = None
    selectedLines: StructureContextToLinesMap2 = None
    serviceData: ServiceData = None


@dataclass
class PasteDuplicateStructureResponse(TcBaseObj):
    """
    response structure of operation that clones the src objects before pasting.
    
    :var createdICRevs: any newly created Incremental Change Revisions.
    :var createdFutureICRevs: any newly created future IC revs
    :var serviceData: service data returns the populated targetLines along with any partial errors.
    :var newChildLines: the map of targetline and the newly created lines under it.
    """
    createdICRevs: List[WorkspaceObject] = ()
    createdFutureICRevs: List[WorkspaceObject] = ()
    serviceData: ServiceData = None
    newChildLines: LineToLinesMap = None


@dataclass
class CopyEBOPStructureResponse(TcBaseObj):
    """
    response structure for the service method copyEBOPStructure.
    
    :var createdICRevs: any newly created incremental change revisions
    :var createdFutureICRevs: any newly created future Incremental Change Revisions.
    :var serviceData: the updated item(root) and any partial errors returned here.
    :var updatedObject: The updatedObject which is the itemrevision of the passed in item.
    """
    createdICRevs: List[WorkspaceObject] = ()
    createdFutureICRevs: List[WorkspaceObject] = ()
    serviceData: ServiceData = None
    updatedObject: WorkspaceObject = None


"""
Map of a line to it's new pasted child lines
"""
LineToLinesMap = Dict[BusinessObject, List[BusinessObject]]


"""
map of StructureContexts to its associated BomLines
"""
StructureContextToLinesMap2 = Dict[StructureContext, List[BOMLine]]
