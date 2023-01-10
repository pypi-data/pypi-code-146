from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass
from typing import Dict


@dataclass
class MarkupResponse(TcBaseObj):
    """
    This MarkupResponse structure is for the response of all processMarkups operations.
    
    :var baseObject: The resulting base object after process markups.
    :var version: The version of the markups set by the server, opaque to the client.
    :var properties: A map (string/string) of properties.    Values can be:
    - Key: "message".  Value: "author","reviewer" or "editor"
    
    
    :var markups: The user supplied JSON markup data that was updated or loaded.
    :var serviceData: The Service Data that may contain partial errors.
    """
    baseObject: WorkspaceObject = None
    version: str = ''
    properties: MarkupProperties = None
    markups: str = ''
    serviceData: ServiceData = None


"""
Contains the key/value pairs for client/server communication.
"""
MarkupProperties = Dict[str, str]
