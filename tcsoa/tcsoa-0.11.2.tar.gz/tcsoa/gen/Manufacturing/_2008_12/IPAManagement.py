from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class IPAManagementGenerateSearchScopeResponse(TcBaseObj):
    """
    Return structure for IPAManagementGenerateSearchScope operation
    
    :var bomlines: A vectoer of all the bomlines that are the search scope.
    :var serviceData: This is a common data strucuture used to return sets of Teamcenter
     Data Model object from a service request. This also holds services exceptions.
    """
    bomlines: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class IPAManagementGetFilteredIPAResponse(TcBaseObj):
    """
    Return structure for IPAManagementGetFilteredIPA operation
    
    :var filteredIPAs: A vectoer of all the filteredIPAs found.
    :var serviceData: This is a common data strucuture used to return sets of Teamcenter
     Data Model object from a service request. This also holds services exceptions.
    """
    filteredIPAs: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class IPAManagementSaveSearchResultInput(TcBaseObj):
    """
    Input structure for IPAManagementSaveSearchResult operation
    
    :var process: The process from which we want to filter the IPA.
    :var searchResultList: The bomlines result from the search.
    :var name: The name of the new filtered structure.
    """
    process: BusinessObject = None
    searchResultList: List[BusinessObject] = ()
    name: str = ''


@dataclass
class IPAManagementSaveSearchResultResponse(TcBaseObj):
    """
    Return structure for IPAManagementSaveSearchResult operation
    
    :var filteredIPA: This is the new filteredIPA structure.
    :var filteredIPARoot: The flat list of all filteredIPA structures.
    :var rejectedList: A list of all the bomlines that were not found in the IPA structure.
    :var serviceData: This is a common data strucuture used to return sets of Teamcenter
     Data Model object from a service request. This also holds services exceptions.
    """
    filteredIPA: BusinessObject = None
    filteredIPARoot: BusinessObject = None
    rejectedList: List[BusinessObject] = ()
    serviceData: ServiceData = None
