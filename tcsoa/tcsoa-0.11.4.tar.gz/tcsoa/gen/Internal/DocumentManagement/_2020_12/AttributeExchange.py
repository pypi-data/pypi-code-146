from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProcessAttrExchangeConfigInput(TcBaseObj):
    """
    This common structure is for the create, update or delete operations on the Attribute Exchange Configuration
    (Fnd0AttrExchangeConfig) object(s)
    
    
    
    This operation adds and/or update or delete a list of attribute exchange configurations that is referenced by
    Logical Object Type.  The attribute exchange configurations will have the attribute exchange directions (e.g
    Teamcenter to File or File to Teamcenter) corresponding to each of Logical Object Type&rsquo;s presented properties.
    
    :var logicalObjectType: An object of logical object type (Fnd0LogicalObject) to which attribute exchange
    configuration are to be added or updated, then relate to.
    :var propertyData: sdgfsdfg sdg sdgfsdfgsdf
    """
    logicalObjectType: BusinessObject = None
    propertyData: List[PropertyData] = ()


@dataclass
class PropertyData(TcBaseObj):
    """
    This property data structure of presented property and corresponding actions of create, update or delete to perform
    on the Fnd0AttrExchangeConfig object.
    
    :var presentedPropertyName: The Fnd0LogicalObjectType&rsquo;s presented property name.
    :var action: The action to perform on the Fnd0AttrExchangeConfig object.  Valid actions are 'add', 'update' or
    'delete'.
    """
    presentedPropertyName: str = ''
    action: str = ''
