from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import ItemRevision


@dataclass
class FileStatus(TcBaseObj):
    """
    Data structure to be used in the response for Simulation Data Monitor Soa services. It contains the information
    about the files found for the traversal path defined in the simulation data monitor config XML
    
    :var heading: Heading to be displayed in the summary section of simulation data monitor.
    :var dstype: Dataset type.
    :var foundCount: Number of valid attached files found
    :var totalCount: Number of components loaded in the simulation Data monitor
    """
    heading: str = ''
    dstype: str = ''
    foundCount: int = 0
    totalCount: int = 0


@dataclass
class MonitorResponse(TcBaseObj):
    """
    Response to be used by the SOA services defined for simulation data monitor.
    
    :var columnHeadings: List of Column headings of monitored columns.
    :var progressHeadings: Data structure containing status for the attached files.
    :var monitoredComponentMap: Monitored component map which contains the list of monitored column.
    :var serviceData: Service Data to be sent with response.
    """
    columnHeadings: List[str] = ()
    progressHeadings: List[FileStatus] = ()
    monitoredComponentMap: MonitoredComponentMap = None
    serviceData: ServiceData = None


@dataclass
class MonitoredColumn(TcBaseObj):
    """
    Data structure to be used in the response of simulation data monitor soa services. It contains the information
    about the attributes.
    
    :var columnHeading: Column Heading under which the attributes of selected components and also the attached files
    will be monitored.
    :var isImage: Boolean to indicate the image
    :var value: Value of the attribute
    """
    columnHeading: str = ''
    isImage: bool = False
    value: str = ''


"""
Map containing list of monitored columns for each component where key is the item revision.
"""
MonitoredComponentMap = Dict[ItemRevision, List[MonitoredColumn]]
