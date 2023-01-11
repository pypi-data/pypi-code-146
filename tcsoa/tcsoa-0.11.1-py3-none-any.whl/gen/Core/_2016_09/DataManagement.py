from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2010_04.DataManagement import DatasetOutput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateAttachOut(TcBaseObj):
    """
    This is output structure for create operation including unique client identifier.
    
    :var clientId: Unique client identifier
    :var objects: List of objects that were created.
    :var datasets: List of output structure for created Dataset objects. Each element in the list contains a client id,
    the related Dataset object created, and the information needed to upload the Dataset object's named reference
    """
    clientId: str = ''
    objects: List[BusinessObject] = ()
    datasets: List[DatasetOutput] = ()


@dataclass
class CreateAttachResponse(TcBaseObj):
    """
    This is response object structure for the createAttachAndSubmitObjects operation
    
    :var output: List of output objects representing objects that were created
    :var serviceData: Service data including partial errors that are mapped to the client id
    """
    output: List[CreateAttachOut] = ()
    serviceData: ServiceData = None
