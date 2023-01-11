from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AttributeDetailsStruct(TcBaseObj):
    """
    The structure specifyies the attributes and its value.
    
    :var attributeName: The string representing the name of the valid attribute which needs to be edited.
    :var attributeValueDetails: The structure specifying details of the attribute value.
    """
    attributeName: str = ''
    attributeValueDetails: Data = None


@dataclass
class ObjectAttributesInput(TcBaseObj):
    """
    The input structure contains object(s) to be edited and the details of the attributes or relations which need to be
    edited.
    
    :var object: The business object representing the BOM line. Attributes of the objects attached to this BOM line
    will be edited. 
    :var attachedObject: The business object attached to the BOM line. Attributes of this object are edited.
    :var attributeDetails: List of the structure attributeDetailsStruct specifying the attributes and their value.
    """
    object: BusinessObject = None
    attachedObject: BusinessObject = None
    attributeDetails: List[AttributeDetailsStruct] = ()


@dataclass
class SyncStudyInput(TcBaseObj):
    """
    The Mfg0BvrStudy objects to synchronize and the direction to synchronize (to/from the study).
    
    :var study: The Mfg0BvrStudy objects to synchronize
    :var direction: The direction to synhronize (true = from BOP, false = to BOP)
    """
    study: BusinessObject = None
    direction: bool = False


@dataclass
class SyncStudyResponse(TcBaseObj):
    """
    The FMS file ticket to the log file for the study synchronization.
    
    :var logFileTicket: The fmd ticket to the log file
    :var serviceData: Standard Service Data
    """
    logFileTicket: str = ''
    serviceData: ServiceData = None


@dataclass
class Data(TcBaseObj):
    """
    The structure specifies details of the attribute value.
    
    :var dataType: Type of the data. Valid types are "Boolean", "Character", "Integer", "Double", "String", "Tag" and
    "Date". Corresponding list in this structure need to be populated based on the data type string.
    :var boolAttributes: The list of Boolean values.
    :var charAttributes: The string representing the list of characters. Each character in the string is a value of the
    attribute.
    :var integerAttributes: The list of integer values.
    :var doubleAttributes: The list of double values.
    :var stringAttributes: The list of string values.
    :var tagAttributes: The list of business objects.
    :var dateAttributes: The list of dates.
    """
    dataType: str = ''
    boolAttributes: List[bool] = ()
    charAttributes: str = ''
    integerAttributes: List[int] = ()
    doubleAttributes: List[float] = ()
    stringAttributes: List[str] = ()
    tagAttributes: List[BusinessObject] = ()
    dateAttributes: List[datetime] = ()
