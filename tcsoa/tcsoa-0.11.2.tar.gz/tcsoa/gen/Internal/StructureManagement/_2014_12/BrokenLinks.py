from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RevisionRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReplacementCandidate(TcBaseObj):
    """
    Structure containing the list of replacement candidates and the coresponding properties list for which the match is
    found.
    
    :var candidate: Candidate found on the basis of given search criteria
    :var matchedProps: The list of property on candidate matching the search criteria
    """
    candidate: BusinessObject = None
    matchedProps: List[str] = ()


@dataclass
class ReplacementCandidateSearchCriteria(TcBaseObj):
    """
    It represents property clause of criteria for searching candidates for broken links.
    
    :var operatorName: The type of search to perform "Mandatory" or "Optional".
    :var propertyName: The name of BOMLine property.
    :var propertyValue: The value of property
    """
    operatorName: str = ''
    propertyName: str = ''
    propertyValue: str = ''


@dataclass
class ReplacementCandidateSearchInput(TcBaseObj):
    """
    Represents the scope and search criteria to find the replacement candidates for broken links.
    
    :var searchScopes: The scope is a BOMLine to search  for the replacements candidates for the given broken link.
    :var replacementCandidateSearchCriteria: The list of search criteria to find the replacement candidate within the
    scope.
    :var revisionRule: The configuration of the structure to retrieve the original value of the abs occ properties of
    the broken link.
    """
    searchScopes: List[BusinessObject] = ()
    replacementCandidateSearchCriteria: List[ReplacementCandidateSearchCriteria] = ()
    revisionRule: RevisionRule = None


@dataclass
class BrokenLinkReplacementResponse(TcBaseObj):
    """
    The response contains service data and list of broken links, and the replacement candidates as per the given search
    criteria  
    
    :var brokenLinkWithReplacementCandidates: The list of broken links and replacement candidates.
    :var serviceData: The service data containing partial errors if any.
    """
    brokenLinkWithReplacementCandidates: List[BrokenLinkWithReplacementCandidate] = ()
    serviceData: ServiceData = None


@dataclass
class BrokenLinkSearchInput(TcBaseObj):
    """
    Input to the service is a structure containing the scope from BOP to find the broken links, scope from product
    structure to find the candidates and the search criteria .
    
    :var searchScope: The scope is a BOMLine to  search  for the broken links.
    :var replacementCandidateSearchInput: List of search criterion to find the replacement candidates for the given
    broken links.
    :var autoRepair: If true the broken link is automatically resolved if the single replacement candidate is found.
    :var fullStructure: If true the search is to be performed in full structure or only in visible structure.
    """
    searchScope: List[BusinessObject] = ()
    replacementCandidateSearchInput: ReplacementCandidateSearchInput = None
    autoRepair: bool = False
    fullStructure: bool = False


@dataclass
class BrokenLinkWithReplacementCandidate(TcBaseObj):
    """
    It represents the list of broken link and its replacement candidates
    
    :var brokenLink: The BOMLine found as a broken link 
    :var replacementCandidates: The list replacement candidates that are found as per the criteria
    """
    brokenLink: BusinessObject = None
    replacementCandidates: List[ReplacementCandidate] = ()
