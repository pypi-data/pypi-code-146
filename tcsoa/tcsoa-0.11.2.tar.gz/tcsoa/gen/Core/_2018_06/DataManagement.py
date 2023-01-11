from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2015_07.DataManagement import CreateInput2
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateIn3(TcBaseObj):
    """
    This is an input structure for create operation of a single object including unique client identifier.
    
    :var clientId: Unique client identifier.
    :var createData: Input data for create operation.
    :var targetObject: Target to which the created object will be related.
    :var pasteProp: Property to be used to relate the created object to the targetObject. This can be something similar
    to the illustrations below:
    (1)      A reference property on the targetObject Type. For example, "contents" on targetObject of Type Folder.
    (2)      A relation property on the targetObject Type. For example, "IMAN_reference" on targetObject of Type Item
    or "IMAN_specification" on targetObject of Type ItemRevision.
    """
    clientId: str = ''
    createData: CreateInput2 = None
    targetObject: BusinessObject = None
    pasteProp: str = ''
