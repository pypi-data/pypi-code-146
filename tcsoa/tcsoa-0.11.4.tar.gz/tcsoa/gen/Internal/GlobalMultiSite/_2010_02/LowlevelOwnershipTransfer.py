from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ObjectsForOwnershipTransferResponse(TcBaseObj):
    """
    It holds FMS ticket of report file which lists candidates for ownership transfer and errors if any.
    
    :var fileFmsTickets: Output file (report) ticket
    :var serviceData: The service data
    """
    fileFmsTickets: str = ''
    serviceData: ServiceData = None


@dataclass
class TransferOwnershipResponse(TcBaseObj):
    """
    It holds the FMS ticket of report file which has information about the status of transfer ownership operation.
    
    :var fileFmsTickets: Output file (report) ticket
    :var serviceData: The service data
    """
    fileFmsTickets: str = ''
    serviceData: ServiceData = None


@dataclass
class UpdateOwnershipTransferResponse(TcBaseObj):
    """
    It holds the FMS ticket of report which has information about the status of update ownership operation and errors
    if any.
    
    :var fileFmsTickets: Output file (report) ticket
    :var serviceData: The service data
    """
    fileFmsTickets: str = ''
    serviceData: ServiceData = None
