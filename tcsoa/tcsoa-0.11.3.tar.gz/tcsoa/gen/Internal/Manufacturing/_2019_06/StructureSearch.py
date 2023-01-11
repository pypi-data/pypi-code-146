from __future__ import annotations

from tcsoa.gen.Manufacturing._2014_12.StructureSearch import AdditionalInfo
from tcsoa.gen.BusinessObjects import BOMLine
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PartsInProximityOutput(TcBaseObj):
    """
    This structure contains the following information:
    - proximityDistance - The proximity distance (in mm) for which the operation was carried out.
    - featureToPartsInProximity - A map (BOMLine, list of BOMLine) containing key as the BOMLine object of type
    Mfg0BvrManufacturingFeature and value as its corresponding list of BOMLine objects that represent parts which are
    in proximity of given proximity distance.
    - additionalInfoOut - Any additional output information. Reserved for future use.
    
    
    
    :var proximityDistance: The proximity distance (in mm) for which the operation was carried out.
    :var featureToPartsInProximity: A map (BOMLine, list of BOMLine) containing key as the BOMLine object of type
    Mfg0BvrManufacturingFeature and value as its corresponding list of BOMLine objects that represent parts which are
    in proximity of given proximity distance.
    :var additionalInfoOut: Any additional output information. Reserved for future use.
    """
    proximityDistance: float = 0.0
    featureToPartsInProximity: MFGFeatureToPartsMap = None
    additionalInfoOut: AdditionalInfo = None


@dataclass
class PartsInProximityResponse(TcBaseObj):
    """
    The response of the service operation contains the following:
    - partsInProximityOut - A list containing returned information after processing of the operation. This will contain
    the proximity distance, a map of BOMLine objects of type Mfg0BvrManufacturingFeature and their corresponding list
    of BOMLine objects representing parts within the proximity distance criteria provided.
    - serviceData - Partial errors as part of the serviceData.
    
    
    
    :var partsInProximityOut: A list containing returned information after processing of the operation. This will
    contain the proximity distance, a map of BOMLine objects of type Mfg0BvrManufacturingFeature and their
    corresponding list of BOMLine objects representing parts within the proximity distance criteria provided.
    :var serviceData: Partial errors as part of the serviceData.
    """
    partsInProximityOut: List[PartsInProximityOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ProximityCriteriaInput(TcBaseObj):
    """
    This structure contains the following information:
    - proximityDistance - The distance in "mm", which represent the proximity distance from BOMLine of type
    Mfg0BvrManufacturingFeature to search for closest BOMLine objects representing parts.
    - mfgFeatureLines - A list of BOMLine objects of type Mfg0BvrManufacturingFeature for which to find the parts in
    proximity.
    - additionalInfoIn - Any additional input information. Reserved for future use.
    
    
    
    :var proximityDistance: The distance in "mm", which represent the proximity distance from BOMLine of type
    Mfg0BvrManufacturingFeature to search for closest BOMLine objects representing parts.
    :var mfgFeatureLines: A list of BOMLine objects of type Mfg0BvrManufacturingFeature for which to find the parts in
    proximity.
    :var additionalInfoIn: Any additional input information. Reserved for future use.
    """
    proximityDistance: float = 0.0
    mfgFeatureLines: List[BOMLine] = ()
    additionalInfoIn: AdditionalInfo = None


"""
A Map (BOMLine,  list of BOMLine) containing key as the BOMLine object of type Mfg0BvrManufacturingFeature and value as its corresponding list of BOMLine objects that represent parts which are in proximity of given proximity distance.
"""
MFGFeatureToPartsMap = Dict[BOMLine, List[BOMLine]]
