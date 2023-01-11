from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ResolveDataInfo(TcBaseObj):
    """
    Input structure specifying the Operation or Process. the Tool Requirement that is to be resolved. the Tool with
    which Tool requirement resolve against and the tool source from where tool is to be picked.
    
    :var parent: Specifies the Operation of type Mfg0BvrOperation or Process of type Mfg0BvrProcess under which Tool
    requirement is assigned.
    :var trObject: Specifies the Tool Requirement of type Mfg0BVRToolRequirement that is to be resolved.
    :var toolObject: Tool of type Mfg0BvrResource that matches the search criteria of the Tool Requirement and against
    which it is going to be resolved.
    :var toolSource: Specifies the source from where the tool is to be fetched.
    The possible values are LIBRARY & WORKAREA and ALL which specify that the tool is to be fetched respectively from
    only library only workarea or workarea and library. Note that in the case of ALL the preference is given to the
    workarea over the library.
    """
    parent: BusinessObject = None
    trObject: BusinessObject = None
    toolObject: BusinessObject = None
    toolSource: str = ''


@dataclass
class Tool(TcBaseObj):
    """
    Specifies the candidate tools with members as the Tool Requirement and the tools that match the search criteria of
    Tool Requirement.
    
    :var trObject: Specifies the Tool Requirement of type Mfg0BVRToolRequirement.
    :var toolObjects: Specifies the candidate tools of type Mfg0BvrResource matching the search criteria of the Tool
    Requirement.
    """
    trObject: BusinessObject = None
    toolObjects: List[BusinessObject] = ()


@dataclass
class ToolRequirementInput(TcBaseObj):
    """
    Input structure specifying the Operation or Process. the Tool Requirement for which candidate tools are to be
    fetched and the tool source from where tools are to be fetched.
    
    :var parent: Specifies the Operation of type Mfg0BvrOperation or Process of type Mfg0BvrProcess under which Tool
    requirement is assigned.
    :var trObject: Specifies the Tool Requirement of type Mfg0BVRToolRequirement for which candidate tools are to be
    fetched.
    :var toolSource: Specifies the source from where the tools are to be fetched. 
    The possible values are Library & WorkArea and All. Which specify that the tools are to be fetched respectively
    from library and workarea. Only library and only workarea.
    """
    parent: BusinessObject = None
    trObject: BusinessObject = None
    toolSource: str = ''


@dataclass
class ToolRequirementResponse(TcBaseObj):
    """
    Specifies the Tool Requirements that are assigned to an Operation or Process.
    
    :var toolRequirements: Specifies the Tool Requirements.
    :var serviceData: Service data will hold warnings and errors. if any.
    """
    toolRequirements: List[ToolRequirementResult] = ()
    serviceData: ServiceData = None


@dataclass
class ToolRequirementResult(TcBaseObj):
    """
    Specifies the Tool Requirements that are assigned to an Operation or Process.
    
    :var parentObject: Specifies the Operation of type Mfg0BvrOperation or Process of type Mfg0BvrProcess to which Tool
    requirement is assigned.
    :var toolRequirements: Specifies the Tool Requirement of type Mfg0BVRToolRequirement that are assigned to the
    Operation or Process.
    """
    parentObject: BusinessObject = None
    toolRequirements: List[BusinessObject] = ()


@dataclass
class CandidateTool(TcBaseObj):
    """
    Specifies the candidate tools for the Operation or Process where Tool Requirement is assigned.
    
    :var parentObject: Specifies the Operation of type Mfg0BvrOperation or Process of type Mfg0BvrProcess where Tool
    Requirement is assigned.
    :var tools: Specifies the candidate tools matching the search criteria of the Tool Requirement.
    """
    parentObject: BusinessObject = None
    tools: List[Tool] = ()


@dataclass
class CandidateToolsForToolRequirement(TcBaseObj):
    """
    Specifies the candidate tools for the Tool Requirement
    
    :var candidateTools: Structure with member as Operation or Process and the candidate tools.
    :var serviceData: Service data will hold warnings and errors. if any.
    """
    candidateTools: List[CandidateTool] = ()
    serviceData: ServiceData = None
