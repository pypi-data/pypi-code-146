from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class HasActiveMarkupAssociatedOut(TcBaseObj):
    """
    Output of the hasActiveMarkupAssociated operation.
    
    :var hasActiveMarkup: A Boolean variable which contains:
    -  true: if there are active markups.
    -  false: if there are no active markups.
    
    
    :var serviceData: An object of ServiceData which contains any errors that may have occurred during operation.
    """
    hasActiveMarkup: bool = False
    serviceData: ServiceData = None


@dataclass
class MassUpdateChange(TcBaseObj):
    """
    Holds the name and new value of the property to be modified.
    
    :var propName: Name of the property which is to be modified.
    :var propValue: New value for the property specified in propName.
    """
    propName: str = ''
    propValue: str = ''


@dataclass
class SaveImpactedAssembliesIn(TcBaseObj):
    """
    Input structure for the saveImpactedAssemblies operation.
    
    :var impactedObject: Fnd0MUImpactedParents Object to specify modified impacted assembly.
    :var massUpdateChanges: List of MassUpdateChange objects.
    """
    impactedObject: RuntimeBusinessObject = None
    massUpdateChanges: List[MassUpdateChange] = ()
