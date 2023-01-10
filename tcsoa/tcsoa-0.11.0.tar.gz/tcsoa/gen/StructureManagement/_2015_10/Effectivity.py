from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ReleaseStatus, Effectivity
from tcsoa.gen.StructureManagement._2014_12.Effectivity import EffectivityInfoInput
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RemoveOccEffectivitiesInput(TcBaseObj):
    """
    The information required to remove effectivity objects from specified BOMLine objects.
    
    :var bomLine: The BOMLine whose effectivities are removed
    :var effectivityComponents: The effectivity objects to be removed
    """
    bomLine: BOMLine = None
    effectivityComponents: List[Effectivity] = ()


@dataclass
class RemoveRelStatusEffectivityInput(TcBaseObj):
    """
    The information required to remove Effectivity from a released status
    
    :var releaseStatus: The released status whose Effectivity is removed
    :var effectivityComponent: The effectivity object to be removed
    """
    releaseStatus: ReleaseStatus = None
    effectivityComponent: Effectivity = None


@dataclass
class EditOccEffectivityInput(TcBaseObj):
    """
    The information required to update occurrence effectivity for the  BOMLine
    
    :var bomLine: The BOMLine whose effectivity is updated
    :var effectivityComponent: The effectivity object to be updated
    :var effectivityInfoInput: A structure to hold effectivity info
    """
    bomLine: BOMLine = None
    effectivityComponent: Effectivity = None
    effectivityInfoInput: EffectivityInfoInput = None


@dataclass
class EditRelStatusEffectivityInput(TcBaseObj):
    """
    The information required to update effectivity on a released status
    
    :var releaseStatus: The released status whose effectivity is updated
    :var effectivityComponent: The effectivity object to be updated
    :var effectivityInfoInput: A structure to hold effectivity info
    """
    releaseStatus: ReleaseStatus = None
    effectivityComponent: Effectivity = None
    effectivityInfoInput: EffectivityInfoInput = None
