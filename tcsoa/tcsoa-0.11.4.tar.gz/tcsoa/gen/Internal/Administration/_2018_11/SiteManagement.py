from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import POM_imc
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SiteInfo(TcBaseObj):
    """
    This object represents a POM_imc business object along with all the information that belongs to that object.
    
    :var siteID: The unique numeric identification number for the site, cannot be 0 but can be negative.
    :var siteName: The name of the site, accepts all ASCII characters but cannot be an empty string.
    :var additionalPropMap: A map (string, string) for the additional properties to create or modify on the POM_imc
    business object. The map has the following Key/Value pairs representing the property name and property's value
    respectively.
    """
    siteID: int = 0
    siteName: str = ''
    additionalPropMap: AdditionalProperty = None


@dataclass
class CreateOrUpdateSitesResponse(TcBaseObj):
    """
    Response structure of createOrUpdateSite operation.
    
    :var outputs: The information that is given back upon a successful creation or update of a POM_imc business object.
    Information includes the object's name, object's ID, and any additional properties the object has.
    :var serviceData: The service data with partial errors if any.
    """
    outputs: List[CreateSitesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateSitesOutput(TcBaseObj):
    """
    The output from creating or updating a POM_imc business object, including the object itself.
    
    :var siteInfo: Information about the POM_imc business object that was updated or created.
    :var pomIMC: The business object POM_imc retrieved from the database.
    """
    siteInfo: SiteInfo = None
    pomIMC: POM_imc = None


"""
A key / value pair for additional properties of the site.

NOTE: This is used for bool types and string types. For bool types we are assuming that the valid values are:

true: "true" (any form of capitalization)
false: "false" (any form of capitalization)
"""
AdditionalProperty = Dict[str, str]
