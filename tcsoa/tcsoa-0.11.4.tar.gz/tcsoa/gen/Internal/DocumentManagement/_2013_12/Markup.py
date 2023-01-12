from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MarkupResponse(TcBaseObj):
    """
    This common MarkupResponse structure is for the response of both loadMarkups and saveMarkups operations.
    
    :var version: The version of the markups set by the server, opaque to the client.
    :var message: The message for client/server communication about the markups, excluding error messages.
    :var markups: The loaded or updated markups.
    :var serviceData: The Service Data that may contain partial errors.
    """
    version: str = ''
    message: str = ''
    markups: str = ''
    serviceData: ServiceData = None
