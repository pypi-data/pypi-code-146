from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import RuntimeBusinessObject
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class HasActiveMarkupAssociatedOut(TcBaseObj):
    """
    Output of the hasActiveMarkupAssociated.
    
    :var hasActiveMarkup: A Boolean variable which contains:
        true: if there are active markups.
        false: if there are no active markups.
    :var serviceData: An object of ServiceData which contains any errors that may have occurred  during operation.
    """
    hasActiveMarkup: bool = False
    serviceData: ServiceData = None


@dataclass
class MassUpdateChange(TcBaseObj):
    """
    Structure to hold Property and its value to be modified.
    
    :var propName: Name of the Property which is to be modified.
    :var propValue: New value for the provided property name in propName.
    """
    propName: str = ''
    propValue: str = ''


@dataclass
class SaveImpactedAssembliesIn(TcBaseObj):
    """
    Input Structure to Save Impacted Assemblies.
    
    :var impactedObject: Fnd0MUImpactedParents Object to specify modified impacted assembly.
    :var massUpdateChanges: List of Mass Update changes.
    """
    impactedObject: RuntimeBusinessObject = None
    massUpdateChanges: List[MassUpdateChange] = ()
