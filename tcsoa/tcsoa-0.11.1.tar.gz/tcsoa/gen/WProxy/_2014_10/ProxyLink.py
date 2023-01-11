from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class CreateProxyLinkInputInfo(TcBaseObj):
    """
    A structure containing uid,owning site of the object for which the ProxyLink object is created, primary object to
    which the proxy link object is related, relation name used to relate the primary object and the proxylink and the
    attributes to be populated on the proxy link object.
    
    :var objectUID: The uid of the object for which the ProxyLink is created.
    :var owningSite: The owning site of the object for which the ProxyLink is created.
    :var proxyLinkType: The name of the ProxyLink type.
    :var attributes: A map (string/string) of  property names and initial  value pairs to be populated on the ProxyLink
    object. 
    :var primaryObject: The BusinessObject to attach the ProxyLink object. 
    :var relationName: The name of the relation to use while attaching the ProxyLink object to the primaryObject .
    """
    objectUID: str = ''
    owningSite: str = ''
    proxyLinkType: str = ''
    attributes: NameValuePairs = None
    primaryObject: BusinessObject = None
    relationName: str = ''


"""
A map (string/string) of  property names and initial  value pairs to be populated on the ProxyLink object.
"""
NameValuePairs = Dict[str, str]
