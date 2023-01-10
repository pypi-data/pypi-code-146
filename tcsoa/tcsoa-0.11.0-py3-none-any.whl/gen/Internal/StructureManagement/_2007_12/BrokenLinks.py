from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, RevisionRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FindAndFixInput(TcBaseObj):
    """
    This structure provides a set of input values for searching candidates for broken links.
    
    :var brokenLinkBOMLines: The broken links or the scope of the broken links.
    :var quickSearch: Do quick search for broken links and candidates?
    :var criteria: The criteria used to search candidates.
    :var autofixAllowed: Automatically fix the broken links if one-to-one match is found?
    """
    brokenLinkBOMLines: List[BOMLine] = ()
    quickSearch: bool = False
    criteria: SearchCandidatesCriteria = None
    autofixAllowed: bool = False


@dataclass
class FindCandidatesResponse(TcBaseObj):
    """
    This structure provides the return of the operation.
    
    :var foundCandidates: The candidates found.
    :var serviceData: The service data to be returned.
    """
    foundCandidates: List[CandidatesList] = ()
    serviceData: ServiceData = None


@dataclass
class RepairBrokenLinksParam(TcBaseObj):
    """
    This structure provides a set of broken link and candidate pair.
    
    :var brokenLink: The broken link to fix.
    :var candidate: The candidate for the broken link.
    """
    brokenLink: BOMLine = None
    candidate: BOMLine = None


@dataclass
class SearchCandidatesCriteria(TcBaseObj):
    """
    This structure provides a set of criteria for searching candidates for broken links including
    candidate scope and previous configuration.
    
    :var candidateScopeBOMLines: the selected BOM lines from where to search the candidates
    :var criteria: the criteria to match BOM lines and the broken link
    :var previousConfiguration: the configuration of the structure to retrieve the original
    value of the abs occ properties of the broken link
    """
    candidateScopeBOMLines: List[BOMLine] = ()
    criteria: List[CriteriaStruct] = ()
    previousConfiguration: RevisionRule = None


@dataclass
class CandidatesList(TcBaseObj):
    """
    This structure provides a set of candidates for a broken link.
    
    :var brokenLink: the BOM line of the broken link
    :var candidates: the candidates of the broken link. When empty means no candidate or
    no search for candidates performed
    """
    brokenLink: BOMLine = None
    candidates: List[BOMLine] = ()


@dataclass
class CriteriaStruct(TcBaseObj):
    """
    This structure provides a property clause of criteria for searching candidates for broken links.
    
    :var propertyName: propertyName
    :var operatorName: operatorName
    """
    propertyName: str = ''
    operatorName: str = ''
