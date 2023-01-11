from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Variant
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetVariabilityInfoResponse(TcBaseObj):
    """
    The 'GetVariabilityObjsResponse' structure represents a list of 'compAndParentVarInfo' objects and the
    'ServiceData' object.
    
    :var compAndParentVarInfo: The list of  'CompAndParentVariabilityInfo' objects containing  variability information
    of the component and its parent.
    :var serviceData: The 'ServiceData' object containing error codes and error messages along with the indices for
    which the getVariabilityInfo operation fails.
    """
    compAndParentVarInfo: List[CompAndParentVariabilityInfo] = ()
    serviceData: ServiceData = None


@dataclass
class VariabilityInfo(TcBaseObj):
    """
    The variability information about each component is provided by way of the 'VariabilityInfo' data structure.
    
    :var variabilityObj: An object pointing to the Variability Expression (VariantExpression with operator code = 2).
    :var variantObj: A Variant object used in the Variability Expression.
    :var comment: An integer value passed through as string which points to the index of the variant value. It is the
    index of variant value from the list of variant values available in the Variant object, which applies to this
    particular Variability Expression.
    """
    variabilityObj: BusinessObject = None
    variantObj: Variant = None
    comment: str = ''


@dataclass
class CompAndParentVariabilityInfo(TcBaseObj):
    """
    The variability information about each component and its parent is provided by way of the
    'CompAndParentVariabilityInfo' data structure.
    
    :var compVarInfo: The list of 'VariabilityInfo' objects containing variability information of component.
    :var parentVarInfo: The list of 'VariabilityInfo' objects containing variability information of the parent of
    component supplied as input.
    """
    compVarInfo: List[VariabilityInfo] = ()
    parentVarInfo: List[VariabilityInfo] = ()
