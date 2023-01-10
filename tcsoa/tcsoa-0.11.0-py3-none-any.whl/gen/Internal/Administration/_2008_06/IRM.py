from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ACLNameInfo(TcBaseObj):
    """
    This structure holds the Named ACL object of requested type and its name.
    
    :var aclObject: Named ACL object.
    :var aclName: The name of the named ACL object.
    """
    aclObject: BusinessObject = None
    aclName: str = ''


@dataclass
class ACLInfoResponse(TcBaseObj):
    """
    This object contains a list of ACL objects of given type and their names.
    
    :var aclNameInfos: A list of  ACLNameInfo objects one for each  named ACL found for the given type.
    :var serviceData: Object that holds the partial errors that occur while getting the named  ACLs of given type.
    """
    aclNameInfos: List[ACLNameInfo] = ()
    serviceData: ServiceData = None
