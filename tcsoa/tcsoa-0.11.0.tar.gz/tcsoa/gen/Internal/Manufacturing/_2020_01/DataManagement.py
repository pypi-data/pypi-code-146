from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssociateOrRemoveScopeInput(TcBaseObj):
    """
    The structure contains a process line object for which the scopes are added or removed. A list of BOMLine object or
    Mfg0BvrWorkarea  object which are assoiated as scope to the input process line object. A list of already defined
    scope object which is disassociated from the process line object. A generic map to provide additional information
    if required.
    
    :var processLine: A Bill Of Process line (BOPLine) object be associated with the scope. The ItemRevision of this
    BOPLine represents the primary of the relation Fnd0ProcessScopeRel.
    :var addScopeLines: A list of either BOMLine object or Mfg0BvrWorkarea object which are associated with the input
    BOPLine object. The AbsOccurrence of BOMLine  object or the Mfg0BvrWorkarea object represents secondary of
    Fnd0ProcessScopeRel.
    :var removeScopeLines: A list of BOMLine object or Mfg0BvrWorkarea object for which the association with process
    line object is removed. For these objects the Fnd0ProcessScopeRel relation is removed.
    :var additionalInfo: 1. Add scope on multiple process lines. The key is "ScopeProcessLine" and the value is a list
    of process line from BOP structure.
    2. Add scope on child lines of input process line. The key is "ScopeChidLines" and the value is string representing
    "Closure Rule".
    """
    processLine: BusinessObject = None
    addScopeLines: List[BusinessObject] = ()
    removeScopeLines: List[BusinessObject] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    A structure containing generic maps to capture the additional information for future use.
    
    :var strToDateMap: A map (string , list of date) to capture additional information.
    :var strToDoubleMap: A map (string, list of double) to capture additional information.
    :var strToStrMap: A map (string, list of string) used to specify if the BOMLine scope is added to the child BOP
    lines of the input process line scope. The key is "ScopeChildLines" and the value is "ClosureRule". The closure
    conatins the BOP object types on which the scope from BOMLine is added.
    :var strToIntMap: A map (string, list of interger) to capture additional information.
    :var strToObjVectorMap: A map (string, list of business object) to capture additional information.
    """
    strToDateMap: StringToDateMap = None
    strToDoubleMap: StringToDoubleMap = None
    strToStrMap: StringToStringMap = None
    strToIntMap: StringToIntegerMap = None
    strToObjVectorMap: StringToObjectMap = None


"""
A map (string , list of date) to capture additional information.
"""
StringToDateMap = Dict[str, List[datetime]]


"""
A map (string, list of double) to capture additional information.
"""
StringToDoubleMap = Dict[str, List[float]]


"""
A map (string, list of interger) to capture additional information.
"""
StringToIntegerMap = Dict[str, List[int]]


"""
A map (string, list of business object) to capture additional information.
"""
StringToObjectMap = Dict[str, List[BusinessObject]]


"""
A map (string, list of string) to capture additional information.
"""
StringToStringMap = Dict[str, List[str]]
