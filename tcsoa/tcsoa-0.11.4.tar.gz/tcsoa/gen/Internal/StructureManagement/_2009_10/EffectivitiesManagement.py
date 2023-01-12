from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow, Item, ItemRevision, Effectivity
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetEffectivityGrpListResponse(TcBaseObj):
    """
    Response contains two elements namely 'effGrpRevList' and 'serviceData'. List of Fnd0EffectvtyGrpRevision objects
    applied on the BOMWindow can be retrieved from 'effGrpRevList'. If the BOMWindow does not have any
    Fnd0EffectvtyGrpRevision objects set on it, then the list is empty.
    
    :var serviceData: structure containing error codes and messages
    :var effGrpRevList: Contains list of Fnd0EffectvtyGrpRevision objects applied to the input BOMWindow
    """
    serviceData: ServiceData = None
    effGrpRevList: List[ItemRevision] = ()


@dataclass
class EffectivitiesInputInfo(TcBaseObj):
    """
    Input structure containing details to create, update or delete an Effectivity object for the input
    Fnd0EffectvtyGrpRevision object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var effectivityComponent: Effectivity object to be updated or deleted from the Fnd0EffectvtyGrpRevision. If the
    'effectivityComponent' is NULL, new Effectivity object is created for given 'unitRangeText' and 'endItemComponent'.
    :var endItemComponent: Valid Item object representing a product, system or module with respect to which user can
    configure the structure by Effectivity.
    :var unitRangeText: Valid range of unit numbers. Unit range can be discrete or non continuous.
    :var decision: Flag to decide if Effectivity object  is to be updated or deleted. 
    decision = 1 ( Update Effectivity component )
    decision =2 ( Delete Effectivity component )
    There is no flag required for create. If effectivityComponent is given as NULL, new Effectivity object is created.
    """
    clientId: str = ''
    effectivityComponent: Effectivity = None
    endItemComponent: Item = None
    unitRangeText: str = ''
    decision: int = 0


@dataclass
class EffectivityGroupInputInfo(TcBaseObj):
    """
    Input structure containing details of BOMWindow and Fnd0EffectvtyGrpRevision objects to be applied.
    
    :var bomWindow: BOMWindow containing a structure with occurrence effectivity
    :var effGrpRevisions: List of Fnd0EffectvtyGrpRevision objects to be applied to the BOMWindow
    :var clientId: Identifier that helps the client to track the object(s) created
    """
    bomWindow: BOMWindow = None
    effGrpRevisions: List[ItemRevision] = ()
    clientId: str = ''
