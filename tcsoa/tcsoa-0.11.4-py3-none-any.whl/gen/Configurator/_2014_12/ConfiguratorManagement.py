from __future__ import annotations

from tcsoa.gen.BusinessObjects import Cfg0AbsAdmissibility, POM_object, Cfg0ConfiguratorPerspective
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AdmissibilityData(TcBaseObj):
    """
    The output structure containing the admissibility data corresponding to the context object.
    
    :var admissibilityList: List of the admissibility objects associated with the context POM_Objects.
    :var contextObject: The context object for which the admissibility information is being returned.
    """
    admissibilityList: List[Cfg0AbsAdmissibility] = ()
    contextObject: POM_object = None


@dataclass
class AdmissibilityOutput(TcBaseObj):
    """
    The output structure containing the admissibility data corresponding to one input entry.
    
    :var admissibilityDataList: The list of admissibility data associated with the context Business Object.
    :var index: The index for corresponding input structure.
    """
    admissibilityDataList: List[AdmissibilityData] = ()
    index: int = 0


@dataclass
class GetAdmissibilityInputStruct(TcBaseObj):
    """
    The input structure for the getAdmissibility operation containing the contexts and perspective instance with
    RevisionRule.
    
    :var configPerspective: The Cfg0ConfiguratorPerspective instance to specify the context and revision rule. This
    parameter can be NULL if the operation parameter for the perspective is not NULL.
    :var contextObjects: The list of context business objects having configurator context as defined by
    configPrespective.
    """
    configPerspective: Cfg0ConfiguratorPerspective = None
    contextObjects: List[POM_object] = ()


@dataclass
class GetAdmissibilityResponse(TcBaseObj):
    """
    Response structure for getAdmissibility operation.
    
    :var admissibilityOutputList: The list of admissibility information output structures for each input.
    :var serviceData: Service data to return partial errors.
    """
    admissibilityOutputList: List[AdmissibilityOutput] = ()
    serviceData: ServiceData = None
