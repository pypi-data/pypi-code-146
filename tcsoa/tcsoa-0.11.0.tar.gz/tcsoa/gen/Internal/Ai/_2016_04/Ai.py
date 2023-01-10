from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InvokeResponse(TcBaseObj):
    """
    This represents the response returned by the Invoke service.
    
    :var xmlOut: The formatted Xml String that the Ai invoke service returns. The structure of xml is an unpublished
    handshake between Teamcenter server and NX client.
    :var data: Service data for this operation. Plain objects are added to this data. All the model objects that are
    contained in the xml output are added here for tracking purpose.
    """
    xmlOut: str = ''
    data: ServiceData = None
