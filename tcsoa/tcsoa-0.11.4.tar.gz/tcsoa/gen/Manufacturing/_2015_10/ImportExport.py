from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportManufaturingFeaturesInput(TcBaseObj):
    """
    input for import manufaturing features.
    
    :var context: A BOMLine in the product structure. The connected parts of the imported manufatruing features are
    searched under this line.
    :var content: A list of detailed input.
    """
    context: BusinessObject = None
    content: List[ImportManufaturingFeaturesScope] = ()


@dataclass
class ImportManufaturingFeaturesResponse(TcBaseObj):
    """
    The output of import manufacturing features.
    
    :var logFileName: The name of the generated log file.
    :var logFileTicket: The FMS ticket of the log file.
    :var serviceData: The service data.
    """
    logFileName: str = ''
    logFileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class ImportManufaturingFeaturesScope(TcBaseObj):
    """
    Detailed input for importing manufacturing features
    
    :var xmlFileTicket: The FMS file ticket for the input XML file to be imported.
    :var container: The BOMLine under which the manufaturing features are going to be imported.
    :var importMode: Indicates whether the existing manufaturing features under the container maybe deleted or not. The
    possible values of the import mode are: keepExistingFeatures - The existing discrete manufacturing features under
    the container should not be deleted. refreshWholeContainer - The existing discrete manufacturing features under the
    container may be deleted.
    :var nameRefFileTickets: The FMS tickets for dataset named reference files.
    """
    xmlFileTicket: str = ''
    container: BusinessObject = None
    importMode: str = ''
    nameRefFileTickets: List[str] = ()
