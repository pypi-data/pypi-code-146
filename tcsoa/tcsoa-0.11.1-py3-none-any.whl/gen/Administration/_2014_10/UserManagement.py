from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MakeUserResponse(TcBaseObj):
    """
    The return data for the makeUser service operation.
    
    :var commandStatus: The make_user command completion status (0 - Success, 1 - Failure). See the make_user utility
    documentation for details.
    :var standardOutputFmsTicket: FMS ticket for the make_user standard output. This element is empty if the
    enableStandardOutput parameter for the operation is false.
    :var standardErrorFmsTicket: FMS ticket for the make_user standard error. This element is empty if the
    enableStandardError parameter for the operation is false.
    :var serviceData: Any errors that occur transferring files to or from FMS or in launcing the make_user utility are
    included in the list of partial errors.
    """
    commandStatus: int = 0
    standardOutputFmsTicket: str = ''
    standardErrorFmsTicket: str = ''
    serviceData: ServiceData = None
