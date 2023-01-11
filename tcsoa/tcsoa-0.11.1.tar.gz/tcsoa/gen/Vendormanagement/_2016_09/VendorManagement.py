from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class VendorPartProperties2(TcBaseObj):
    """
    The information about each ManufacturerPart to be processed is provided by way of the VendorPartProperties2 data
    structure.
    
    :var partId: Id of ManufacturerPart to be created, if not specified or blank then operation will generate the
    partId.
    :var partName: Part Name of the ManufacturerPart to be created.
    :var partType: Object type to be created. Only "ManufacturerPart" is valid type.
    :var revId: Revision Id specified for create. Generated if the string is empty.
    :var vendorObj: Vendor object to be associated with ManufacturerPart.
    :var companyLocationObj: CompanyLocation object to be associated with ManufacturerPart. If null, then no location
    will be associated with ManufacturerPart object.
    :var clientId: A unique string supplied by the caller. This ID is used to identify the Partial Errors associated
    with input.
    """
    partId: str = ''
    partName: str = ''
    partType: str = ''
    revId: str = ''
    vendorObj: BusinessObject = None
    companyLocationObj: BusinessObject = None
    clientId: str = ''
