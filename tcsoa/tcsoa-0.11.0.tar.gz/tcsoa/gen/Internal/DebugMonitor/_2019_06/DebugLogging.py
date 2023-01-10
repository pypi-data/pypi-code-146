from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class DebugLoggingResponse(TcBaseObj):
    """
    The DebugLoggingResponse data type provides a response to the client of the debug logging flags that were set and
    the service data information.
    
    :var prevDebugLoggingFlags: Previous debug logging flags.
    :var serviceData: Service data information.
    """
    prevDebugLoggingFlags: Logflags = None
    serviceData: ServiceData = None


"""
A map (string, string) of logflags that enables debug logs.
"""
Logflags = Dict[str, str]
