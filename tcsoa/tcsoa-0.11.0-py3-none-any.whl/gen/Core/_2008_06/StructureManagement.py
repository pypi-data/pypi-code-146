from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetPrimariesOfInStructureAssociationInfo(TcBaseObj):
    """
    Input structure for GetPrimariesOfInStructureAssociationInfo operation
    
    :var secondary: secondary object/BOMLine business object
    :var contextBOMLine: Context object of association. This is generally the parent line of the primary object and is
    an optional parameter.
    :var associationType: the created association type e.g. ConnectTo, ImplementedBy, RealizedBy, DeviceToConnector,
    RoutedBy, SignalToSource, SignalToTarget, SignalToTransmitter, ProcessVariable, RedundantSignal.
    """
    secondary: BusinessObject = None
    contextBOMLine: BOMLine = None
    associationType: str = ''


@dataclass
class GetPrimariesOfInStructureAssociationResponse(TcBaseObj):
    """
    Return structure for GetPrimariesOfInStructureAssociationResponse  operation
    
    :var serviceData: The ServiceData structure is used to return the primary BOMLine business objects and partial
    errors if any occurring in the operation.
    :var primariesInfo: Context object of association. This is generally the parent line of the primary object.
    """
    serviceData: ServiceData = None
    primariesInfo: List[PrimariesOfInStructureAssociation] = ()


@dataclass
class GetSecondariesOfInStructureAssociationInfo(TcBaseObj):
    """
    Input structure for GetSecondariesOfInStructureAssociationInfo operation
    
    :var primaryBOMLine: primary BOMLine
    :var contextBOMLine: Context BOMLine business object of association (optional)
    :var associationType: Association type between the primary and secondary BOMLine business objects.
    """
    primaryBOMLine: BOMLine = None
    contextBOMLine: BOMLine = None
    associationType: str = ''


@dataclass
class GetSecondariesOfInStructureAssociationResponse(TcBaseObj):
    """
    Return structure for GetSecondariesOfInStructureAssociationResponse  operation
    
    :var serviceData: Secondary BOMLine business objects and Partial errors if any
    :var secondariesInfo: primary BOMLine and association type.
    """
    serviceData: ServiceData = None
    secondariesInfo: List[SecondariesOfInStructureAssociation] = ()


@dataclass
class InStructureAssociationInfo(TcBaseObj):
    """
    Input structure for InstructureAssociationInfo operation
    
    :var primaryBOMLine: The primary object of association
    :var contextBOMLine: The context in which the association of the specified type between primaryBOMLine and
    secondaries is valid.
    :var secondaries: secondary objects of association.
    :var associationType: association type to be created
    """
    primaryBOMLine: BOMLine = None
    contextBOMLine: BOMLine = None
    secondaries: List[BusinessObject] = ()
    associationType: str = ''


@dataclass
class PrimariesOfInStructureAssociation(TcBaseObj):
    """
    Output structure for GetPrimariesOfInStructureAssociationInfo operation
    
    :var secondary: secondary object for which the primaries has been returned
    :var associationType: association type to be created
    :var primaryBOMLine: Primary object associated with the secondary
    """
    secondary: BusinessObject = None
    associationType: str = ''
    primaryBOMLine: BOMLine = None


@dataclass
class RemoveInStructureAssociationsInfo(TcBaseObj):
    """
    Input structure for removeInStructureAssociations operation
    
    :var primaryBOMLine: primary BOMLine object reference of association
    :var contextBOMLine: Context BOMLine of association (optional)
    :var secondaries: Secondary BOMLines to be disassociated from the primary BOMLine.
    :var associationType: Association type between primary and secondary BOMLines.
    """
    primaryBOMLine: BOMLine = None
    contextBOMLine: BOMLine = None
    secondaries: List[BusinessObject] = ()
    associationType: str = ''


@dataclass
class RemoveInStructureAssociationsResponse(TcBaseObj):
    """
    Return structure for GetSecondariesOfInStructureAssociationResponse  operation
    
    :var serviceData: The updated objects and partial errors if any.
    """
    serviceData: ServiceData = None


@dataclass
class SecondariesOfInStructureAssociation(TcBaseObj):
    """
    Output structure for GetSecondariesOfInStructureAssociationInfo operation
    
    :var primaryBOMLine: Primary BOMLine associated with the secondary.
    :var associationType: association type to be created
    :var secondaries: Secondary BOMLines associated with the primaries
    """
    primaryBOMLine: BOMLine = None
    associationType: str = ''
    secondaries: List[BusinessObject] = ()


@dataclass
class CreateInStructureAssociationResponse(TcBaseObj):
    """
    Return structure for createInStructureAssociations  operation
    
    :var serviceData: The ServiceData structure is used to return the updated objects and contains partial errors, if
    any, occurring in the operation.
    """
    serviceData: ServiceData = None
