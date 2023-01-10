from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List


@dataclass
class ContextObjectResponse(TcBaseObj):
    """
    This structure contains the list of all the objects related to the current object within context and the
    serviceData object.
    
    :var objectMap: A map of input business object to a list of related Item, Processes and ChangeRequestRevision 
    (business object/ vector). The DesignContext application then adds these objects to the respective lists i.e.
    Workparts list, ChangeRequestRevision list or the Processes list based on the type of object. If no related object
    is found empty map is returned.
    :var serviceData: The ServiceData objects containing error codes and error messages in case of failure.
    """
    objectMap: RelatedObjectsInfo = None
    serviceData: ServiceData = None


"""
This map contains a list of related objects for each input object.
Key: The input object is the key.
Values: A list of objects that related to the input object are the values.
"""
RelatedObjectsInfo = Dict[BusinessObject, List[BusinessObject]]
