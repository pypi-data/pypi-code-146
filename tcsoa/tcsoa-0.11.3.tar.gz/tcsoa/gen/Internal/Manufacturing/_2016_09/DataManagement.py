from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanRelation
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LinkBOPtoBOEObjectInfo(TcBaseObj):
    """
    A list of LinkBOPtoBOEObjectInfo structures is the input to the SOA linkPlantBOPtoBOE. This structure has
    1. sourceLine
    2. targetLine
    3. clientId
    
    :var sourceLine: BOP line as  primary object.
    :var targetLine: BOE line as secondary object.
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this LinkBOPtoBOEObjectInfo structure.
    """
    sourceLine: BOMLine = None
    targetLine: BOMLine = None
    clientID: str = ''


@dataclass
class LinkPlantBOPtoBOEResponse(TcBaseObj):
    """
    This structure represents the response from the SOA linkPlantBOPtoBOE for a list of input LinkBOPtoBOEObjectInfo
    structures.
     It has
    1. relationObjects
    2. serviceData
    
    :var relationObjects: A list of created relations.
    :var serviceData: Partial errors as part of the serviceData.
    """
    relationObjects: List[LinkedRelationObject] = ()
    serviceData: ServiceData = None


@dataclass
class LinkedRelationObject(TcBaseObj):
    """
    This structure represents the output from the SOA linkPlantBOPtoBOE  for a single input LinkBOPtoBOEObjectInfo
    structure.
    It has
    1. clientId
    2. relation
    
    :var clientId: The unmodified value from the LinkBOPtoBOEObjectInfo.clientId. This can be used by the caller to
    identify this data structure with the source input data.
    :var relation: The newly created relation of type Mfg0MELinkedBOERel.
    """
    clientId: str = ''
    relation: ImanRelation = None


@dataclass
class SynchronizeBOPAndBOEInputInfo(TcBaseObj):
    """
    A list of SynchronizeBOPAndBOEInputInfo structures is the input to the SOA synchronizePlantBOPAndBOE. This
    structure has
    1. sourceLine
    2. targetLine
    3. removeObsoleteTwin
    4. clientId
    
    :var sourceLine: The source line can either be a plant BOP line or a BOE line. This is the primary structure in the
    synchronization,  based on which the target structure will be modified and its attributes will be mapped.
    :var targetLine: The target line can either be a BOE line or a plant BOP line. The target structure will be
    modified in order to have the similar structure as that of source.
    :var removeObsoleteTwin: A boolean variable to specify if an obsolete object in target structure are to be removed.
    If true, each line in the target structure which do not have any connected line with Mfg0MELinkedBOERel relation
    will be removed. If false, such obolete lines will be unchanged.
    :var clientID: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this SynchronizeBOPAndBOEInputInfo structure.
    """
    sourceLine: BOMLine = None
    targetLine: BOMLine = None
    removeObsoleteTwin: bool = False
    clientID: str = ''


@dataclass
class SynchronizePlantBOPAndBOEOutput(TcBaseObj):
    """
    This structure represents the output from the SOA synchronizePlantBOPAndBOE for a single input
    SynchronizeBOPAndBOEInputInfo structure.
    It has
    1. clientId
    2. relations
    
    :var clientId: The unmodified value from the         SynchronizeBOPAndBOEInputInfo.clientId. This can be used by
    the caller to identify this data structure with the source input data.
    :var relations: A list of newly created relations of type Mfg0MELinkedBOERel.
    """
    clientId: str = ''
    relations: List[ImanRelation] = ()


@dataclass
class SynchronizePlantBOPAndBOEResponse(TcBaseObj):
    """
    This structure represents the response from the SOA synchronizePlantBOPAndBOE for a list of input
    SynchronizeBOPAndBOEInputInfo structures.
    It has
    1.synchronizePlantBOPAndBOEOutput: The list of new relations created
    2. serviceData: Partial errors as part of the serviceData.
    
    :var synchronizePlantBOPAndBOEOutput: The list of new relations created.
    :var serviceData: Partial errors as part of the serviceData.
    """
    synchronizePlantBOPAndBOEOutput: List[SynchronizePlantBOPAndBOEOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateBOEfromPlantBOPResponse(TcBaseObj):
    """
    Response from SOA createBOEfromPlantBOP.
    1. boeStructureTopLines
        Top lines of new created BOE structures.
    2. serviceData:
        Partial errors as part of the serviceData.
    
    :var boeStructureTopLines: Top lines of new created BOE structures.
    :var serviceData: Partial errors as part of the serviceData.
    """
    boeStructureTopLines: List[BOMLine] = ()
    serviceData: ServiceData = None
