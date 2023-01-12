from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanFile, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOccKinematicsInfoInput(TcBaseObj):
    """
    Input containing context and scope for which the occurrence kinematics information of resource occurrence
    Mfg0MEResourceRevision or ItemRevision is required
    
    :var context: Root BOMLine in Bill of Equipment structure representing Mfg0BvrWorkarea. The operation processes
    scope within the context.
    :var scope: BOMLine representing Mfg0BvrWorkarea object under context. The operation processes resource occurrence
    under the scope to get occurrence kinematics information. The scope can be empty, in this case context is treated
    as scope.
    """
    context: BOMLine = None
    scope: BOMLine = None


@dataclass
class GetOccurrenceKinematicsInfoResponse(TcBaseObj):
    """
    Response for getOccurrenceKinematicsInformation operation.
    
    :var occurrenceKinematicInfo: A list containing information about BOMLine representing occurrence of
    Mfg0MEResourceRevision or ItemRevision and ImanFile having occurrence kinematics information
    :var serviceData: The Teamcenter Services structure used to return status of the operation.
    """
    occurrenceKinematicInfo: List[OccurrenceKinematicsInfo] = ()
    serviceData: ServiceData = None


@dataclass
class OccurrenceKinematicsInfo(TcBaseObj):
    """
    Response containing information about context BOMLine representing Mfg0BvrWorkarea, scope BOMLine representing
    Mfg0BvrWorkarea , a map with key as BOMLine representing occurrence of Mfg0MEResourceRevision or ItemRevision and
    the value as ImanFile having occurrence kinematics information.
    
    :var context: Root BOMLine in Bill of Equipment structure representing Mfg0BvrWorkarea
    :var scope: BOMLine representing Mfg0BvrWorkarea object under context. The operation processes resource occurrence
    under the scope to get occurrence kinematics information
    :var resourceLineInformation: A map (BOMLine, ImanFile) containing information about BOMLine representing the
    occurrence of MFg0MEResourceRevision or ItemRevision as key and corresponding ImanFile as value which contains the
    kinematics information
    """
    context: BOMLine = None
    scope: BOMLine = None
    resourceLineInformation: ResourceLineInfoMap = None


"""
The map (BOMLine, Dataset) containing BOMLine representing occurrence of Mfg0MEResourceRevision or ItemRevision as key and Mfg0OccKinematicsInfo dataset as value.
"""
OccKinematicsInfoMap = Dict[BOMLine, Dataset]


"""
A map (BOMLine, ImanFile) containing information about the BOMLine representing occurrence of MFg0MEResourceRevision or ItemRevision as key and corresponding ImanFile as value which contains the kinematics information.
"""
ResourceLineInfoMap = Dict[BOMLine, ImanFile]
