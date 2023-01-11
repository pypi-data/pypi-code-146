from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ServiceData(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    plain: List[str] = ()
    updated: List[str] = ()
    deleted: List[str] = ()
    created: List[str] = ()
    partialErrors: List[ErrorStack] = ()
    modelObjects: TagMap = None


@dataclass
class ErrorStack(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    clientId: str = ''
    clientIndex: str = ''
    associatedObject: BusinessObject = None
    errorValues: List[ErrorValue] = ()


@dataclass
class ErrorValue(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    message: str = ''
    code: int = 0
    level: int = 0


@dataclass
class PartialErrors(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    pass


@dataclass
class Preferences(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    pass


@dataclass
class TypeSchema(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    pass


@dataclass
class ModelSchema(TcBaseObj):
    """
    System class - needs reverse engineering!
    """
    pass


TagMap = Dict[str, BusinessObject]
