from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RemoteCheckinFailure(TcBaseObj):
    """
    Object specific detailed failure information.
    
    :var failureObjects: A list of objects that have failed to check-in.
    :var failureCodes: A list of failure codes for this operation.
    :var failureStrings: A list of error strings corresponding to each error in failureCodes.
    """
    failureObjects: List[BusinessObject] = ()
    failureCodes: List[int] = ()
    failureStrings: List[str] = ()


@dataclass
class RemoteCheckinResponse(TcBaseObj):
    """
    The RemoteCheckinResponse returns detailed partial failure information in RemoteCheckinFailure structures along
    with a ServiceData.
    
    :var failureInfo: A list of RemoteCheckinFailure structures. Each structure contains failure information for a
    specific business object that was supplied.
    :var serviceData: The standard ServiceData return.
    """
    failureInfo: List[RemoteCheckinFailure] = ()
    serviceData: ServiceData = None


@dataclass
class RemoteCheckoutFailure(TcBaseObj):
    """
    Failure information  for specific objects that failed to remote check out.
    
    :var failureObjects: A list of objects that have failed to check out.
    :var failureCodes: A list of failure codes for the failureObjects.
    :var failureStrings: A list of error strings corresponding to each error in failureCodes.
    """
    failureObjects: List[BusinessObject] = ()
    failureCodes: List[int] = ()
    failureStrings: List[str] = ()


@dataclass
class RemoteCheckoutResponse(TcBaseObj):
    """
    The RemoteCheckoutResponse returns detailed partial failure information in RemoteCheckoutFailure structures along
    with a ServiceData.
    
    :var serviceData: The standard ServiceData return.
    :var failureInfos: A list of RemoteCheckoutFailure structures. Each structure contains failure information for a
    specific business object that was supplied.
    """
    serviceData: ServiceData = None
    failureInfos: List[RemoteCheckoutFailure] = ()


"""
Map of string array property names to values (string, vector).
"""
StringVectorMap = Dict[str, List[str]]
