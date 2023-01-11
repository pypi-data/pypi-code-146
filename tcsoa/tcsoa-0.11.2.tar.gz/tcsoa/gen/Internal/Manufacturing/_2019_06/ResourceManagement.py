from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetICOMappingTargetsResponse(TcBaseObj):
    """
    -
    
    :var serviceData: The service data containing partial errors if any.
    :var mappingInfoVector: A list of "MappingInfo" structure.
    """
    serviceData: ServiceData = None
    mappingInfoVector: List[MappingInfo] = ()


@dataclass
class MappingInfo(TcBaseObj):
    """
    Structure containing data for  GTC mapping.
    
    :var sourceIcoID: ICO ID for the source class.
    :var sourceIcoUID: ICO UID for the source class.
    :var sourceClassID:  ID for the source class.
    :var sourceClassName: Name of the source class.
    :var targetMachine: Value of machine side connection code used for finding match based on connection codes.
    :var targetWorkpiece: Value of workpiece side connection code used for finding match based on connection codes.
    :var targetGTCBase:  GTC Base value for target class used for finding match based on connection codes.
    :var targetClasses: A list of "TargetClass" structure.
    """
    sourceIcoID: str = ''
    sourceIcoUID: str = ''
    sourceClassID: str = ''
    sourceClassName: str = ''
    targetMachine: str = ''
    targetWorkpiece: str = ''
    targetGTCBase: str = ''
    targetClasses: List[TargetClass] = ()


@dataclass
class TargetClass(TcBaseObj):
    """
    -
    
    :var targetID: ID of target class.
    :var targetName: Name of target class.
    """
    targetID: str = ''
    targetName: str = ''
