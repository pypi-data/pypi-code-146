from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class Arg(TcBaseObj):
    """
    Arg
    
    :var val: Argument value
    :var structure: Structure if argument is structure
    :var array: Array if argument is array
    """
    val: str = ''
    structure: List[Structure] = ()
    array: List[Array] = ()


@dataclass
class Array(TcBaseObj):
    """
    Array
    
    :var entries: Array entries
    """
    entries: List[Entry] = ()


@dataclass
class InvokeICTMethodResponse(TcBaseObj):
    """
    Response of invokeICTMethod method
    
    :var output: Output arguments
    :var serviceData: service data
    """
    output: List[Arg] = ()
    serviceData: ServiceData = None


@dataclass
class Structure(TcBaseObj):
    """
    structure
    
    :var args: List of arguments
    """
    args: List[Arg] = ()


@dataclass
class Entry(TcBaseObj):
    """
    Array entry
    
    :var val: Entry value
    :var structure: Structure if entry is a structure
    :var array: Array if entry is an array
    """
    val: str = ''
    structure: List[Structure] = ()
    array: List[Array] = ()
