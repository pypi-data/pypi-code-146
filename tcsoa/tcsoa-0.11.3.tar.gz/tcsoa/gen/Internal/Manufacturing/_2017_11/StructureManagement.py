from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_10.StructureManagement import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AlternativeScopeForProductInputInfo(TcBaseObj):
    """
    Data required to create Fnd0MfgAlternativeScope for each product.
    
    :var productNode: A root BOMLine object  to create the Fnd0MfgAlternativeScope from.
    :var newAlternativeScpName: The name of Fnd0MfgAlternativeScope to be created.
    :var newAlternativeScpDesc: The description of the Fnd0MfgAlternativeScope to be created.
    :var containerInfo: A map (string,  list of BOMLine objects) containing the container name as key and list of
    BOMLine nodes which will be part of the container as value. Valid container names are "In-process Assembly
    Container", "Manufacturing Features Container" and "Connected To Container".
    """
    productNode: BusinessObject = None
    newAlternativeScpName: str = ''
    newAlternativeScpDesc: str = ''
    containerInfo: AlternativeScopeContainerInfo = None


@dataclass
class AlternativeScopeForProductResponse(TcBaseObj):
    """
    The response contains map where the key is input root BOMLine and the value is newly created
    Fnd0MfgAlternativeScope object.The following partial error may be returned :
    - 251076  : Alternative Scope creation failed for the given product structure.
    
    
    
    :var productNodeAlternativeScp: The map(BOMLine, BOMLine)  containing the input BOMLine node as key and the newly
    created Fnd0MfgAlternativeScope as value.
    :var serviceData: standard service data containing partial errors.
    """
    productNodeAlternativeScp: ProductNodeAndAlternativeScpMap = None
    serviceData: ServiceData = None


@dataclass
class PasteByRuleInfo(TcBaseObj):
    """
    Structure representing a source BOMLine and target BOMline pair.
    
    :var sourceLine: The source BOMline of type Mfg0BVROperation or type Mfg0BvrProcess to be pasted.
    :var targetLine: The target BOMline of type Mfg0BvrProcessStation from a PlantBOP to paste source BOMline to.
    :var additionalInfo: Currently not used.
    """
    sourceLine: BusinessObject = None
    targetLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class PasteByRuleInfoInput(TcBaseObj):
    """
    Contains a  list of PasteByRuleInfo elements each representing a source and target line pair.
    
    :var sourceTargetLineInfo: List of structures of type representing source and target BOMline pairs.
    :var targetLine: Represents the target BOMLine in the PlantBOP. Can be provided when target is same for all source
    BOMLine objects.
    :var additionalInfo: Currently not used.
    """
    sourceTargetLineInfo: List[PasteByRuleInfo] = ()
    targetLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class PasteByRuleResponse(TcBaseObj):
    """
    Structure representing created BOMLine objects and partial errors.
    
    :var createdLines: A list of  BOMLine objects created during the paste operation.  Can be NULL for some BOMLine
    objects if there is an error during creation of the new BOMLine. The index of createdLines matches the index of the
    sourceTargetLineInfo list.
    :var serviceData: The service data containing partial errors.
    :var additionalInfo: Currently not used.
    """
    createdLines: List[BusinessObject] = ()
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


"""
A map contains the input product root node as key and the newly created Fnd0MfgAlternativeScope object as value.
"""
ProductNodeAndAlternativeScpMap = Dict[BusinessObject, BusinessObject]


"""
A map contains the container information. The key of the map is container name and the value is list of BOMLine objects.
"""
AlternativeScopeContainerInfo = Dict[str, List[BusinessObject]]
