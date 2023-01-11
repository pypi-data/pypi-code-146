from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class UserConsentStatement(TcBaseObj):
    """
    Output strucutre of getUserConsentStatement operation.
    
    :var consentStatement: User consent statement for the locale the user is logged in.
    :var serviceData: Service data with the partial error information.
    """
    consentStatement: str = ''
    serviceData: ServiceData = None
