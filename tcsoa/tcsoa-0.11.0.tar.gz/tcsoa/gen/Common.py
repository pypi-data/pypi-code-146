from __future__ import annotations

from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ObjectPropertyPolicy(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    modifiers: List[Modifiers] = ()
    types: List[PolicyType] = ()
    useRefCount: bool = False


@dataclass
class PolicyProperty(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    name: str = ''
    modifiers: List[Modifiers] = ()


@dataclass
class PolicyType(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    name: str = ''
    modifiers: List[Modifiers] = ()
    properties: List[PolicyProperty] = ()


@dataclass
class Modifiers(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    name: str = ''
    value: str = ''
