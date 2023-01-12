from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportManufaturingFeaturesInput(TcBaseObj):
    """
    input for import manufaturing features
    
    :var context: A BOMLine in the product structure. The connected parts of the imported manufatruing features are
    searched under this line
    :var content: A list of detailed input
    """
    context: BusinessObject = None
    content: List[ImportManufaturingFeaturesScope] = ()


@dataclass
class ImportManufaturingFeaturesScope(TcBaseObj):
    """
    Detailed input for importing manufacturing features
    
    :var xmlFileTicket: The FMS file ticket for the input XML file to be imported
    :var scope: The BOMLine under which the manufaturing features are being searched. Based on the result of the
    search, the import decides whether to create a new manufacturing feature or to update an existing one
    :var container: The BOMLine under which the manufaturing features are going to be imported
    :var importMode: Indicates whether the existing manufacturing features under the container shall be deleted or not.
    The possible values of the import mode are:  keepExistingFeatures The existing discrete manufacturing features
    under the container should not be deleted. refreshWholeContainer   The existing discrete manufacturing features
    under the container may be deleted.
    :var nameRefFileTickets: A list of FMS tickets for the dataset named reference files
    """
    xmlFileTicket: str = ''
    scope: BusinessObject = None
    container: BusinessObject = None
    importMode: str = ''
    nameRefFileTickets: List[str] = ()


@dataclass
class MfgExportToBriefcaseResponse(TcBaseObj):
    """
    This operation returns export log and datasets associated with exported objects.
    
    :var briefcaseFileFMSTicket: FMS ticket of the briefcase file, which can be used to download the briefcase file
    from server to client.
    :var fileTickets: To represent a file ticket and its original file name.
    :var messageIds: List of message IDs.
    :var briefcaseDataSet: A business object of Dataset which includes the out briefcase file in its namedReference.
    After export, a new Dataset will be created. The exported briefcase file will be added to the new Dataset.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors in case
    of failure conditions.
    """
    briefcaseFileFMSTicket: str = ''
    fileTickets: List[str] = ()
    messageIds: List[str] = ()
    briefcaseDataSet: BusinessObject = None
    serviceData: ServiceData = None


"""
A map of strings. Contains names and values.
"""
NamesAndValuesMap = Dict[str, str]
