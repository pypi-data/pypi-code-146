from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Item, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetEffectivityResponse(TcBaseObj):
    """
    The 'GetEffectivityResponse' structure represents the effectivity data returned by 'getEffectivity' operation.
    
    :var effectivityData: A list of BusinessObjects with effectivity data.
    :var serviceData: The service data contains partial errors, if there are any errors during the operation.
    """
    effectivityData: List[EffectivityInfo] = ()
    serviceData: ServiceData = None


@dataclass
class Effectivity(TcBaseObj):
    """
    The 'Effectivity' represents a validity range. The following constants have special meaning:
    - January 2, 1900 12:00 AM UTC: Open Start Date.
    - December 30, 9999 12:00 AM UTC: Open End Date.
    - December 26, 9999 12:00 AM UTC: Stock Out.
    - 1: Open Start Unit.
    - 2147483647: Open End Unit.
    - 2147483646: Stock Out.
    
    
    Effect in as well as effect out points may have NULL values, which indicate no value assigned:
    - -1: no unit value assigned.
    - NULL date: no date value assigned.
    
    
    
    :var unitIn: The unit at which validity range starts.
    :var unitOut: The unit at which validity range ends.
    :var dateIn: The date at which validity range starts.
    :var dateOut: The date at which validity range ends.
    :var endItem: The effectivity end Item. This is mandatory if unit range is specified.
    :var effectivityOptions: A list of 'EffectivityOption' for which the effectivity range is valid (optional). The
    valid effectivity options are available on the effectivity context associated with with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit.  The effectivity options can be specified as: 
    - 'familyNamespace'=EFFCTX001, 'familyName'=Maturity Intent, 'optionValue'=Design, 'opCode'=5
    - 'familyNamespace'=EFFCTX001, 'familyName'=Module Intent, 'optionValue'=Kit, 'opCode'=5
    
    """
    unitIn: int = 0
    unitOut: int = 0
    dateIn: datetime = None
    dateOut: datetime = None
    endItem: Item = None
    effectivityOptions: List[EffectivityOption] = ()


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    The 'EffectivityInfo' structure represents effectivity for a BusinessObject.
    
    :var clientId: A unique string to identify returned BusinessObject and partial errors associated with input.
    :var inputObject: The BusinessObject to which effectivity information to be associated. Supported types are:
    ItemRevision and Awb0Element.
    :var effectivity: A list of 'Effectivity' for an 'inputObject'.
    :var effectivityFormula: The effectivity formula for an 'inputObject'. Either 'effectivity' or 'effectivityFormula'
    can be specified while setting the effectivity. If both are specified, 'effectivity' is ignored.
    For example, for unit range 1 to 10 the corresponding formula is ([Teamcenter::]Unit >= 1 &amp; [Teamcenter::]Unit
    < 11 ) &amp; [Teamcenter::]EndItem = "HDD-Top"
    """
    clientId: str = ''
    inputObject: BusinessObject = None
    effectivity: List[Effectivity] = ()
    effectivityFormula: str = ''


@dataclass
class EffectivityInfoInput(TcBaseObj):
    """
    The 'EffectivityInfoInput' structure represents BusinessObject and its effectivity to be set.
    
    :var effectivityContext: The effectivity context to be associated with the 'inputObject' in 'effectivityData'
    (optional). If 'effectivityContext' is specified, a new Fnd0ProductEffConfigCxtRel relation is created between
    'inputObject' and 'effectivityContext'. Supported context types are: Item and ItemRevision. The context is
    considered only when 'inputObject' is of type ItemRevision and is ignored if 'inputObject' is of type Awb0Element.
    If 'NULL', effectivity context is not associated with 'inputObject'.
    :var effectivityData: A list of BusinessObjects with effectivity data.
    """
    effectivityContext: WorkspaceObject = None
    effectivityData: List[EffectivityInfo] = ()


@dataclass
class EffectivityOption(TcBaseObj):
    """
    The 'EffectivityOption' structure represents an additional effectivity validity along with date and unit
    effectivity ranges.
    
    :var familyNamespace: The namespace by which the effectivity option family is uniquely identified. The
    'familyNamespace' is the item id of effectivity context associated with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The 'familyNamespace' can be EFFCTX001.
    :var familyName: The name of the effectivity option family. The valid option family names are available on the
    effectivity context associated with with product Item with relation Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The 'familyNamespace' is set as EFFCTX001. The 'familyName' can be either
    Maturity Intent or Module Intent.
    :var opCode: The operator to be used for the 'optionValue'. 
    The valid values are:
    - 5 &ndash; Equals
    - 6 &ndash; Not Equals
    
    
    :var optionValue: The value for the effectivity option. The valid option values for given 'familyNamespace'  and
    'familyName' are available on the effectivity context associated with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The 'familyNamespace' is set as EFFCTX001. The 'familyName' is set Maturity
    Intent. The 'optionValue' can be either Design or Production.
    """
    familyNamespace: str = ''
    familyName: str = ''
    opCode: int = 0
    optionValue: str = ''
