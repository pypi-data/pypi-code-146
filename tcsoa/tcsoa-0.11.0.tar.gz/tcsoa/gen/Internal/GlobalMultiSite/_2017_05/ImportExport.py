from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class TransformDataResponse(TcBaseObj):
    """
    The TransformDataResponse holds the FMS tickets of the output file, the log file and also contains the partial
    errors that are used to report any partial failures.
    
    :var outputFileTicket: The FMS ticket is used to get the transformed output file.
    :var logFileTicket: The FMS ticket is sued to get the generated transform log file. All the warning and error
    messages in the transform process are recorded in the log file.
    :var serviceData: Service data contains user facing partial errors which are returned to the client. For the
    complete list of errors and warnings during the transform process, users need to check the log file.
    """
    outputFileTicket: str = ''
    logFileTicket: str = ''
    serviceData: ServiceData = None
