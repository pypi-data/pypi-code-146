from __future__ import annotations

from tcsoa.gen.Common import ObjectPropertyPolicy
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RegisterIndex(TcBaseObj):
    """
    Contains the index to be used for unregistering.
    
    :var registryIndex: Index to be used for unregistering.
    """
    registryIndex: int = 0


@dataclass
class SetPolicyResponse(TcBaseObj):
    """
    The policy ID and full definition of the object property policy.
    
    :var policyId: Unique ID for this object property policy.
    :var policy: The full definition of the object property policy.
    """
    policyId: str = ''
    policy: ObjectPropertyPolicy = None
