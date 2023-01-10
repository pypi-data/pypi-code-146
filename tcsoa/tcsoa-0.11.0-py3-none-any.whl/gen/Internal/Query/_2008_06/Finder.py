from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindObjectsAttrAndValues(TcBaseObj):
    """
    A structure for FindObjectsByClassAndAttributes operation.  This structure contains the  attributes and values used
    to filter the search.
    
    :var attrName: Attribute name
    :var values: List of attribute values
    """
    attrName: str = ''
    values: List[str] = ()


@dataclass
class FindObjectsInput(TcBaseObj):
    """
    Input stucture for FindObjectsByClassAndAttributes.
    
    :var className: An attribute name on the class to query on.
    :var clientId: The client ID
    :var outputAttributeNames: List of attributes whos values will be returned.  Can be empty if requesting the objects.
    :var attrAndValues: A list of FindSingleAttributeAttrAndValues.
    """
    className: str = ''
    clientId: str = ''
    outputAttributeNames: List[str] = ()
    attrAndValues: List[FindObjectsAttrAndValues] = ()


@dataclass
class FindObjectsResponse(TcBaseObj):
    """
    Return structure for FindObjectsByClassAndAttributes operation.
    
    :var serviceData: The ServiceData
    :var result: A list of the objects found.  This will be empty if attribute values are requested.
    :var attrAndValues: A list of FindSingleAttributeAttrAndValues.
    """
    serviceData: ServiceData = None
    result: List[BusinessObject] = ()
    attrAndValues: List[FindObjectsAttrAndValues] = ()
