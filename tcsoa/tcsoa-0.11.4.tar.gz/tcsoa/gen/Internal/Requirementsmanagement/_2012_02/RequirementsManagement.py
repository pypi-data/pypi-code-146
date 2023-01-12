from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanRelation
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TraceabilityMatrixInfo(TcBaseObj):
    """
    'TraceabilityMatrixInfo' structure represents the parameters required to create the traceability matrix between
    source and target BOM structure.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var sourceLine: The source BOMLine object, required to create a traceability matrix.
    :var targetLine: The target BOMLine object, required to create a traceability matrix.
    """
    clientId: str = ''
    sourceLine: BOMLine = None
    targetLine: BOMLine = None


@dataclass
class TraceabilityMatrixOutput(TcBaseObj):
    """
    'TraceabilityMatrixOutput' structure represents the output parameters as a result of creating the traceability
    matrix between source and target structure. This structure contains a map object that will contain source object
    for link creation as a key of the map and list of all object as a values.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var traceabilityMap: The TraceabilityMatrixMap object, that contains the source BOMLine object as a key and list
    of TraceabilityMatrixStructure as value in the map. This map will be parsed on the client to show proper link count
    for specific source and target object in the traceability matrix.
    """
    clientId: str = ''
    traceabilityMap: TraceabilityMatrixMap = None


@dataclass
class TraceabilityMatrixResponse(TcBaseObj):
    """
    'TraceabilityMatrixResponse' structure represents list of TraceabilityMatrixOutput structure containing the
    TraceabilityMatrixMap map object along with the ServiceData.
    
    :var serviceData: The Service Data.
    :var output: A list of TraceabilityMatrixOutput structure that hold the information to generate traceability matrix
    selected source and target objects. This information will be parsed on the client to show the proper data in the
    matrix.
    """
    serviceData: ServiceData = None
    output: List[TraceabilityMatrixOutput] = ()


@dataclass
class TraceabilityMatrixStructure(TcBaseObj):
    """
    'TraceabilityMatrixStructure' structure represents the output parameters to specify that for specified source
    BOMLine and specified target BOMLine object these TraceLink relation objects are created. This structure contains
    the list of all TraceLink relation between specified source BOMLine and each target BOMLine object.
    
    :var bomLine: A target BOMLine object with respect to each source BOMLine from the source structure.
    :var relations: A list of TraceLink relation object that defined that specified each source and target BOMLine
    object.
    """
    bomLine: BOMLine = None
    relations: List[ImanRelation] = ()


"""
This is a map that will contain the source BOMLine object as a key and 'TraceabilityMatrixStructure' structure vector as values.
"""
TraceabilityMatrixMap = Dict[BOMLine, List[TraceabilityMatrixStructure]]
