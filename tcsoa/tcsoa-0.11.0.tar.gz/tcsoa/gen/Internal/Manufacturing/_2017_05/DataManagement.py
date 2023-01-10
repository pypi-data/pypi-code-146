from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2015_10.StructureManagement import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetFutureRevisionsIn(TcBaseObj):
    """
    Structure to provide input BOMLine.
    
    :var inputLine: The BOMLine of type Mfg0BvrProcess or MfgBvrOperation that future revisions will be searched for.
    :var additionalInfo: For future use.
    """
    inputLine: BusinessObject = None
    additionalInfo: AdditionalInfo = None


@dataclass
class GetFutureRevisionsInfo(TcBaseObj):
    """
    Collection of revision information.
    
    :var line: BOMLine associated with future revision information.
    :var revInfoList: List of future revision information.
    :var additionalInfo: For future use.
    """
    line: BusinessObject = None
    revInfoList: List[RevisionInfo] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class GetFutureRevisionsResponse(TcBaseObj):
    """
    Structure to return future revision information for a line.
    
    :var lineFutureRevisionInfoMap: A map (BOMLine/std::vector< GetFutureRevisionsInfo >) of input line to associated
    future revisions information.
    :var serviceData: Partial errors and future use.
    :var additionalInfo: Reserved for future use.   For example ,  key = "Transitions" and values = "10 July","20 Aug".
    """
    lineFutureRevisionInfoMap: LineFutureRevisionInfoMap = None
    serviceData: ServiceData = None
    additionalInfo: AdditionalInfo = None


@dataclass
class RevisionInfo(TcBaseObj):
    """
    Collection of revision information.
    
    :var futureRevision: The future revision Item Revision.
    :var futureRevStatusInfo: The list of associated status and effectivity information for futureRevision.
    :var additionalInfo: For future use.
    """
    futureRevision: BusinessObject = None
    futureRevStatusInfo: List[StatusInfo] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class StatusInfo(TcBaseObj):
    """
    Collection of Status information.
    
    :var status: The status object.
    :var futureRevEffectivityInfo: The list of associated effectivity information for status.
    """
    status: BusinessObject = None
    futureRevEffectivityInfo: List[EffectivityInfo] = ()


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    A collection of effectivity information.
    
    :var effectivity: The effectivity object.
    :var ranges: A list of effectivity ranges.
    :var effectivityTransitionsMap: A map(std::string/std::vector<std::string>) correlating an effectivity range to a
    corresponding list of effectivity transitions within that range.
    """
    effectivity: BusinessObject = None
    ranges: List[str] = ()
    effectivityTransitionsMap: RangeTransitionsEffectivityMap = None


"""
Map of input BOMLine to associated future revisions information
"""
LineFutureRevisionInfoMap = Dict[BusinessObject, List[GetFutureRevisionsInfo]]


"""
A map correlating an effectivity range to a corresponding list of effectivity transitions within that range.
"""
RangeTransitionsEffectivityMap = Dict[str, List[str]]
