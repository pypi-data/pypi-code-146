from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanRelation
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class InvalidAssociation(TcBaseObj):
    """
    Invalid Association data
    
    :var associationType: Association Type
    :var primary: primary BOMLine
    :var secondary: secondary BOMLine.
    :var relation: Invalid relation object
    :var reason: Reason why relation is invalid
    """
    associationType: str = ''
    primary: BOMLine = None
    secondary: BOMLine = None
    relation: ImanRelation = None
    reason: str = ''


@dataclass
class ValidateInStructureAssociationsResponse(TcBaseObj):
    """
    Contains the Service data and array of invalid associations data
    
    :var serviceData: This is a common data structure used to return sets of Teamcenter Data Model object from a
    service request. This also holds services exceptions.
    :var failedAssociations: Vector of invalid associations
    """
    serviceData: ServiceData = None
    failedAssociations: List[InvalidAssociation] = ()
