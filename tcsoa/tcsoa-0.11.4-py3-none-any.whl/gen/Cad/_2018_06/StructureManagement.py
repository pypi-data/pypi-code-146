from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AssemblyConfigurationResponse(TcBaseObj):
    """
    This structure is used by SOA Teamcenter::Soa::Cad::_2018_06::
    StructureManagement::writeAssemblyConfigurationDetails for returning XML output file name in
    readFileTicketForStructureData and status of operation is written to serviceData.
    
    :var readFileTicketForStructureData: This is the FMS read file ticket for the TC XML data file written to the
    transient volume. The TC XML file can be downloaded using this ticket.
    :var serviceData: This service data contains any partial errors which may have been encountered during processing.
    The partial error client Ids match the client Id for the input which failed.
    """
    readFileTicketForStructureData: str = ''
    serviceData: ServiceData = None
