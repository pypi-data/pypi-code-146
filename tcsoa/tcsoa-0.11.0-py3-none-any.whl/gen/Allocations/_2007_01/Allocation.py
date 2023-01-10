from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, PSBOMView, AllocationMapRevision, AllocationMap, RevisionRule, AllocationWindow, AllocationLine, BOMWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AllocationContextInput(TcBaseObj):
    """
    The AllocationContextInput structure represents all the data necessary for creating an Allocation Context. The
    basic attributes that are required by ITK are passed as named elements in the structure.
    
    :var id: The ID of the AllocationMap object to be created. If empty, will be generated.
    :var name: The name of the AllocationMap object to be created. Optional input.
    :var type: The type of the AllocationMap object to be created. If type is not provided, the AllocationMap created
    will be of type AllocationMap.
    :var revision: The revision id for the AllocationRevisionMap object to be created.
    :var openedBOMWindows: List of BOMWindow business objects to be associated to the AllocationMap business object,
    where the created AllocationMap will be the context for the Allocations created between the BOMLine objects of
    these BOMWindow objects.
    """
    id: str = ''
    name: str = ''
    type: str = ''
    revision: str = ''
    openedBOMWindows: List[BOMWindow] = ()


@dataclass
class AllocationLineInfo(TcBaseObj):
    """
    The AllocationLineInfo structure represents all of the data necessary to construct the AllocationLine object. The
    basic attributes that are required by ITK are passed as named elements in the structure.
    
    :var name: The AllocationLine name for creation, optional if empty, generated on server.
    :var type: The AllocationLine type, if empty then the default type Allocation is used.
    :var reason: The AllocationLine reason, optional.
    :var fromBOMLines: AllocateFrom BOMLine objects, required.
    :var toBOMLines: AllocateTo BOMLine objects, required.
    """
    name: str = ''
    type: str = ''
    reason: str = ''
    fromBOMLines: List[BOMLine] = ()
    toBOMLines: List[BOMLine] = ()


@dataclass
class AllocationLineInput(TcBaseObj):
    """
    The AllocationLineInput structure contains all the elements necessary for the identifying an AllocationLine object,
    including AllocationLineInfo structure as well as an object reference to the AllocationLine itelf.
    
    :var allocationLine: AllocationLine object which needs to be modified.
    :var allocationLineInfo: AllocationLineInfo element containing all information necessary for modification of the
    AllocationLine object.
    """
    allocationLine: AllocationLine = None
    allocationLineInfo: AllocationLineInfo = None


@dataclass
class AllocationWindowInfo(TcBaseObj):
    """
    The AllocationWindowInfo structure represents all of the data necessary for opening an AllocationWindow. The basic
    attributes that are required by ITK are passed as named elements in the structure.
    
    :var allocationContext: AllocationContext Object, can be AllocationMap or AllocationMapRevision businessobject.
    :var allocationRule: Allocation Rule.
    :var openedBOMWindows: Keep track of opened BOM Window
    """
    allocationContext: AllocationMapRevision = None
    allocationRule: RevisionRule = None
    openedBOMWindows: List[BOMWindow] = ()


@dataclass
class GetAllocatedBOMViewInfo(TcBaseObj):
    """
    The GetAllocatedBOMViewInfo structure is used as a mapping between the AllocationMap
    object and its corresponding allocated BOMView Objects.
    
    :var allocationMap: AllocationMap business object.
    :var allocatedBOMViewObjects: A list of PSBOMView business objects associated to the AllocationMap object.
    """
    allocationMap: AllocationMap = None
    allocatedBOMViewObjects: List[PSBOMView] = ()


@dataclass
class GetAllocatedBOMViewResponse(TcBaseObj):
    """
    The GetAllocatedBOMViewResponse structure contains a list of the structure GetAllocatedBOMViewInfo and Service
    Data. Any errors are reported in ServiceData.
    
    :var allocatedBOMViewInfo: Structure which contains the AllocationMap business object and a list of associated
    PSBOMView objects.
    :var serviceData: The ServiceData.
    """
    allocatedBOMViewInfo: List[GetAllocatedBOMViewInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GetAllocationWindowResponse(TcBaseObj):
    """
    The GetAllocationWindowResponse structure represents the current state of the BOMWindow as well as the list of
    AllocationLine objects contained in said BOMWindow.
    
    :var allocationWindow: The Business Object corresponding to the AllocationWindow.
    :var allocationLines: AllocationLine objects for the modified AllocationWindow.
    :var serviceData: ServiceData contains the created AllocationMap, AllocationMapRevision, and AllocationWindow 
    created in the created objects of list of the ServiceData Element. Any errors occurred during the operation will be
    returned in the Partial errors of the ServiceData element.
    """
    allocationWindow: AllocationWindow = None
    allocationLines: List[AllocationLine] = ()
    serviceData: ServiceData = None
