from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AllocationContextInput2(TcBaseObj):
    """
    The AllocationContextInput2 structure represents all the data necessary for creating an Allocation Context. The
    basic attributes that are required by ITK are passed as named elements in the structure. It will be used by the
    revised SOA createAllocationContext2() which also handles extended attributes.
    
    :var id: The ID of the AllocationMap object to be created. If empty, will be generated.
    :var name: The name of the AllocationMap object to be created. Optional input.
    :var type: The type of the AllocationMap object to be created. If type is not provided, the AllocationMap created
    will be of type AllocationMap.
    :var revision: The revision id for the AllocationRevisionMap object to be created.
    :var openedBOMWindows: List of BOMWindow business objects to be associated to the AllocationMap business object,
    where the created AllocationMap will be the context for the Allocations created between the BOMLines of these
    BOMWindows.
    :var attrValueMap: The map of  Attribute names and  value pairs to be used for AllocationMap business object
    creation of type string/string. The client calling this operation is responsible for converting the different
    property types (int , float, date etc) to string  using the appropriate to XXXString functions. Multi valued
    properties are represented with a comma separated string.
    """
    id: str = ''
    name: str = ''
    type: str = ''
    revision: str = ''
    openedBOMWindows: List[BOMWindow] = ()
    attrValueMap: AttrValueMap = None


"""
The AttrValueMap map represents Attribute Value pair map for the Allocation Map attributes.
"""
AttrValueMap = Dict[str, str]
