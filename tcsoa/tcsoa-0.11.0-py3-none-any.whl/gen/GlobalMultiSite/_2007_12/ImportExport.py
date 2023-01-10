from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NamesAndValues(TcBaseObj):
    """
    The NamesAndValues structure represents a generic name-value pair.
    
    :var name: The name of the session option.
    :var value: The value of the session option.
    """
    name: str = ''
    value: str = ''


@dataclass
class OwningSiteAndObjs(TcBaseObj):
    """
    Vector of object and it's owning site.
    These objects need to be remote imported
    
    :var owningSiteId: owningSiteId
    :var objs: objs
    """
    owningSiteId: int = 0
    objs: List[BusinessObject] = ()


@dataclass
class CallToRemoteSiteResponse(TcBaseObj):
    """
    CallToRemoteSiteResponse
    
    :var msgIDs: msgIDs
    :var serviceData: serviceData
    """
    msgIDs: List[str] = ()
    serviceData: ServiceData = None
