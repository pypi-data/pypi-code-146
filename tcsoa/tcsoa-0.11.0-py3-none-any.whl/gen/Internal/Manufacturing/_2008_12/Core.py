from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CheckinInput(TcBaseObj):
    """
    Input for the checkin service.
    
    :var ciProcess: true if "process" opition is selected.
    :var isRecursive: true if "isRecursive" opition is selected.
    """
    ciProcess: bool = False
    isRecursive: bool = False


@dataclass
class CheckoutInput(TcBaseObj):
    """
    Input for the checkout service.
    
    :var coProcess: true if "process" opition was selected.
    :var isRecursive: true if "isRecursive" opition was selected.
    :var coTools: true if "coTools" opition was selected.
    :var coPlant: true if "coPlant" opition was selected.
    :var coAssembly: true if "coAssembly" opition was selected.
    :var changeId: The user Id.
    :var reason: The reason for the checkout.
    """
    coProcess: bool = False
    isRecursive: bool = False
    coTools: bool = False
    coPlant: bool = False
    coAssembly: bool = False
    changeId: str = ''
    reason: str = ''
