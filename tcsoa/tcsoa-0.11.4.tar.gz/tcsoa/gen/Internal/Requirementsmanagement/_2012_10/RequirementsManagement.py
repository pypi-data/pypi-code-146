from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MatchLineInputData(TcBaseObj):
    """
    The MatchLineInputData structure represents all of the data necessary to search any ItemRevision object from all
    open BOMWindow instances.
    
    :var revObject: The business revision object for which matching BOMLine needs to be searched.
    :var scopeTopLines: The list of top BOMLine of all open BOMWindow instance(s) in which revision objects needs to be
    searched.
    """
    revObject: BusinessObject = None
    scopeTopLines: List[BusinessObject] = ()


@dataclass
class MatchedLineData(TcBaseObj):
    """
    This structure contains information about matching BOMLine or GDELine, and top line within the scope of BOMWindow.
    
    :var matchedLine: First matched BOMLine or GDELine object. If no matching object found then returns null.
    :var topLine: Top line of BOMWindow in which the matching BOMLine found.
    """
    matchedLine: BusinessObject = None
    topLine: BusinessObject = None


@dataclass
class MatchedLineOutput(TcBaseObj):
    """
    This structure represents the output details for each matching BOMLine or GDELine. It has information about
    underlying revision object, list of matching BOMLine instances, and its corresponding top BOMLine.
    
    :var revObject: The revision object which searched in all given BOMWindow instance(s).
    :var matchedLineData: This is the list of found matching BOMLine and their corresponding BOMWindow top line for
    given revision.
    """
    revObject: BusinessObject = None
    matchedLineData: List[MatchedLineData] = ()


@dataclass
class MatchedLineResponse(TcBaseObj):
    """
    This structure represents the output of getMatchingLines operation.  It has information about matched BOMLine
    objects and its corresponding revision object.
    
    :var matchedOutput: A list of MatchedLineOutput structure containing information of each matching found details.
    :var serviceData: The Service Data
    """
    matchedOutput: List[MatchedLineOutput] = ()
    serviceData: ServiceData = None


@dataclass
class TraceabilityMatrixInfo1(TcBaseObj):
    """
    This structure holds information to create the traceability matrix between source and target BOM structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var sourceLine: The source BOMLine object, required to create a traceability matrix.
    :var targetLine: The target BOMLine object, required to create a traceability matrix.
    :var filterFormat: Name of filtering format for traceability matrix. On this format name will be decided whether to
    filter or not and also need to include subtypes of trace link for selected trace link types. This filterFormat
    strings will be:
    NO_FILTER : Filter will not be applied for getting trace link relations. It will get all trace link relations.
    DO_FILTER : Filter will be applied for getting only selected trace link types mentioned in parameter filterTypes
    list.
    DO_FILTER_SUBTYPE : Filter will be applied for getting only selected trace link type objects mentioned in list
    filterTypes, including their subtypes.
    :var filterTypes: Vector of trace link types to be filtered and displayed in traceability matrix.
    """
    clientId: str = ''
    sourceLine: BOMLine = None
    targetLine: BOMLine = None
    filterFormat: str = ''
    filterTypes: List[str] = ()
