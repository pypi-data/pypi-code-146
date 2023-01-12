from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ParentChildPair(TcBaseObj):
    """
    Structure of a pair of parent and child objects for occurrence condition validation.
    
    :var parent: The parent ItemRevision object where to add the child
    :var child: The child ItemRevision or GeneralDesignElement object to be added
    """
    parent: BusinessObject = None
    child: BusinessObject = None


@dataclass
class AddInformation(TcBaseObj):
    """
    Contains information of the object to be added as a new line. When used by Add operation, only one of the
    item/itemRev, element and line will be used.
    
    :var item: The item to be added. It can be null.
    :var itemRev: The item revision to be added. It can be null.
    :var bomView: The BOMView object to be added. It can be null.
    :var element: The General Design Element object to be added. It can be null.
    :var line: The BOMLine object to be pasted as new line. It can be ImanItemLine or GDELine. It can be null.
    :var initialValues: A map to hold initial values of BOMLine properties. Occurrence type can be specified here but
    will be handled specially if used by Add operation.
    """
    item: BusinessObject = None
    itemRev: BusinessObject = None
    bomView: BusinessObject = None
    element: BusinessObject = None
    line: BOMLine = None
    initialValues: BOMLineProperties = None


@dataclass
class AddParam(TcBaseObj):
    """
    The input for adding lines.
    
    :var parent: The parent where the objects are added.
    :var toBeAdded: The information about the objects to be added.
    :var flags: A  bit map of the flags. The lowest bit is reserved for as substitute. If the bit is 1, it means the
    operation will add the object as substitute, otherwise it as normal line. The second lowest bit is for propagating
    transform matrix, when specified as 1, transform matrix will be propagated from source line to the new line. The
    third lowest bit is used for pending cut lines. If set, the line will be removed after being copied.  Other bits
    are not used.
    """
    parent: BOMLine = None
    toBeAdded: List[AddInformation] = ()
    flags: int = 0


@dataclass
class AddResponse(TcBaseObj):
    """
    The response for add operation
    
    :var addedLines: The added lines.
    :var serviceData: The serviceData object that contains partial errors.
    """
    addedLines: List[BOMLine] = ()
    serviceData: ServiceData = None


"""
BOMLine properties and values.
"""
BOMLineProperties = Dict[str, str]
