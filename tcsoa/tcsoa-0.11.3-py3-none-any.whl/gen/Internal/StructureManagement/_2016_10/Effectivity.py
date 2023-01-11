from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_object, PSBOMViewRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class NetEffectivityOutput(TcBaseObj):
    """
    Holds unit net effectivity data for each BOMLine object.
    
    :var occEffectivity: The occurrence effectivity of the BOMLine
    :var netEffectivity: The calculated unit net effectivity of the BOMLine
    :var netEOC: Indicates whether the BOMLine would configure based on its calculated unit net effectivity
    """
    occEffectivity: str = ''
    netEffectivity: str = ''
    netEOC: bool = False


@dataclass
class NetEffectivityResponse(TcBaseObj):
    """
    Holds the NetEffectivity output response for the input BOMLine objects.
    
    :var netEffectivityOutputVector: Holds unit net effectivity data for input BOMLine objects.
    :var serviceData: The Service Data.
    """
    netEffectivityOutputVector: List[NetEffectivityOutput] = ()
    serviceData: ServiceData = None


@dataclass
class OccCutbackValueInfo(TcBaseObj):
    """
    Contains  effectivity value proposals for a specified occurrence
    
    :var occ: occurrence whose effectivity is being modified, may not be null
    :var effProposals: list of proposed effectivity values, may be empty
    """
    occ: BusinessObject = None
    effProposals: List[ProposalInfo] = ()


@dataclass
class OccEffCutbackInfo(TcBaseObj):
    """
    Contains unit occurrence effectivity cutback information for the specified PSBOMViewRevision
    
    :var cutbackParent: PSBOMViewRevision object for which to manage cutback data
    :var cutbacks: list of cutback objects, may be empty
    """
    cutbackParent: PSBOMViewRevision = None
    cutbacks: List[CutbackInfo] = ()


@dataclass
class ProposalInfo(TcBaseObj):
    """
    Contains the Teamcenter:: Fnd0OccEffValue proposal being modified and the proposed effectivity value, in format
    unit range(enditem). The proposal may not be null, an empty effectivity value  allows re-generation of a proposal
    value.
    
    :var proposal: Teamcenter:: Fnd0OccEffValue proposal being modified, may not be null
    :var effectivity: proposed effectivity value, in format: unit range(enditem), if empty then allows re-generation of
    proposal value
    """
    proposal: POM_object = None
    effectivity: str = ''


@dataclass
class CutbackInfo(TcBaseObj):
    """
    Contains data to govern the cuback action. The solution BOMLine objects take on the cutback effectivity, and the
    impacted BOMLine objects may not be effective for that cutback effectivity.
    
    :var cutback: Teamcenter::Fnd0OccEffCutback cutback being modified, if null then create a new cutback object
    :var name: name of cutback, may not be null
    :var description: description of cutback, may be null
    :var sequence: sequence order during application of active cutbacks
    :var effectivity: list of effectivity values to drive cutback action, each element in format: unit range(enditem)
    :var solutions: list of OccCutbackValueInfo objects for the cutback effectivity, may be empty
    :var impacted: list of OccCutbackValueInfo objects to be impacted by solution effectivity, may not be empty
    :var allowGaps: indicates whether proposals can leave gaps in overall effectivity
    :var actionForCutback: The action to take on the cutback object: 1=create, 2=modify, 3=delete
    """
    cutback: POM_object = None
    name: str = ''
    description: str = ''
    sequence: int = 0
    effectivity: List[str] = ()
    solutions: List[OccCutbackValueInfo] = ()
    impacted: List[OccCutbackValueInfo] = ()
    allowGaps: bool = False
    actionForCutback: int = 0


@dataclass
class CutbackUnitEffectivityResponse(TcBaseObj):
    """
    Unit occurrence effectivity cutback data for input BOMLine objects.
    
    :var cutbacks: Holds unit occurrence effectivity cutback data for input PSBOMViewRevision objects
    :var serviceData: The Service Data
    """
    cutbacks: List[OccEffCutbackInfo] = ()
    serviceData: ServiceData = None
