from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PackageBriefcaseContentsInfo(TcBaseObj):
    """
    The input for packageBriefcaseContents operation.
    
    :var sourceSiteId: The Id of the source site.
    :var targetSiteIds: The Ids of the target sites.
    :var requestingUserName: The user name who is creating the briefcase.
    :var tcplmxmlFmsTickets: FMS tickets of the source TC XML files.
    :var exportLogFmsTickets: FMS tickets of the export log files.
    :var datasetName: This string is in the format of datasetName~~transactionId. The first part will be used as the
    name of the dataset. The second part is the transaction ID which will be used to confirm the TC XML export
    opertion. This transaction ID should be the same with the one used in ImportExport::exportObjects operation.
    """
    sourceSiteId: int = 0
    targetSiteIds: List[int] = ()
    requestingUserName: str = ''
    tcplmxmlFmsTickets: List[str] = ()
    exportLogFmsTickets: List[str] = ()
    datasetName: str = ''


@dataclass
class PackageBriefcaseContentsResponse(TcBaseObj):
    """
    The response from packageBriefcaseContents operation.
    
    :var briefcaseDataSet: The briefcase Dataset with briefcase file as named reference.
    :var briefcaseDataSetUrl: The URL of the briefcase Dataset. This is constructed from the Dataset.
    :var serviceData: Contains the partial error, the briefcase datasets are added to the createdObject list.
    """
    briefcaseDataSet: Dataset = None
    briefcaseDataSetUrl: str = ''
    serviceData: ServiceData = None


@dataclass
class UnpackBriefcaseContentsResponse(TcBaseObj):
    """
    The response from unpackBriefcaseContents operation.
    
    :var sourceSiteId: The Id of the source site.
    :var tcplmxmlFmsTickets: FMS tickets of the output TCXML files which are ready for import.
    :var serviceData: The Service Data. The input briefcase TC file will be deleted and added to deletedObject list.
    """
    sourceSiteId: int = 0
    tcplmxmlFmsTickets: List[str] = ()
    serviceData: ServiceData = None
