from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AMImpactedObjectsResponse(TcBaseObj):
    """
    Data structure that holds the UIDs of Teamcenter business objects whose READ access is impacted by the Access
    Manager rule tree changes, a Boolean flag that indicates if full reindex is needed or not and the service data with
    any partial errors that might happen while finding the impacted objects
    
    :var serviceData: serviceData
    :var isImpactGlobal: isImpactGlobal
    :var impactedUids: impactedUids
    """
    serviceData: ServiceData = None
    isImpactGlobal: bool = False
    impactedUids: List[str] = ()


@dataclass
class GetSessionValuesResponse(TcBaseObj):
    """
    Structure that holds the SessionValuesMap which contains session keys and corresponding session values. Each
    session key in the SessionValuesMap corresponds to a session attribute like groups, roles and project teams.
    
    :var sessionValues: A map of key-value pairs that holds the session keys and the matching session values from Read
    Expression string.
    """
    sessionValues: SessionValuesMap = None


"""
List of session names which maps session name to value(s). All values are expressed in their string equivalent.
"""
SessionValuesMap = Dict[str, List[str]]
