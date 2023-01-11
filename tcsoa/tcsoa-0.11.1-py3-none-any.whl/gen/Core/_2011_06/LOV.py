from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ListOfValues
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LOVAttachment(TcBaseObj):
    """
    Structure to hold property and its LOV attachment.
    
    :var propName: Name of the property to  which LOV attachment return.
    :var lov: Attached LOV object.
    """
    propName: str = ''
    lov: ListOfValues = None


@dataclass
class LOVAttachmentsInput(TcBaseObj):
    """
    A structure holding objects and common properties for which LOV attachments are to be returned.
    
    :var objects: Instances of any business object for which LOV attachments are being evaluated.
    :var properties: Names of common properties for which LOV attachments to be returned for each instance in 'objects'
    """
    objects: List[BusinessObject] = ()
    properties: List[str] = ()


@dataclass
class LOVAttachmentsResponse(TcBaseObj):
    """
    LOV attachments for the given object properties.
    
    :var lovAttachments: A list of objects and its properties and associated LOV attachments.
    :var serviceData: The Service Data.
    """
    lovAttachments: InpoutObjectToLOVAttachmentsMap = None
    serviceData: ServiceData = None


"""
A map of input objects to list of LOVattachments structure.
"""
InpoutObjectToLOVAttachmentsMap = Dict[BusinessObject, List[LOVAttachment]]
