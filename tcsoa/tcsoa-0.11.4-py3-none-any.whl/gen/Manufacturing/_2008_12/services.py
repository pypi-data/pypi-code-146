from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2008_12.IPAManagement import IPAManagementGenerateSearchScopeResponse, IPAManagementGetFilteredIPAResponse, IPAManagementSaveSearchResultResponse, IPAManagementSaveSearchResultInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IPAManagementService(TcService):

    @classmethod
    def saveSearchResult(cls, input: List[IPAManagementSaveSearchResultInput]) -> IPAManagementSaveSearchResultResponse:
        """
        Saves the search result in a new/updated structure.
        """
        return cls.execute_soa_method(
            method_name='saveSearchResult',
            library='Manufacturing',
            service_date='2008_12',
            service_name='IPAManagement',
            params={'input': input},
            response_cls=IPAManagementSaveSearchResultResponse,
        )

    @classmethod
    def deletefilteredIPA(cls, processes: List[BusinessObject]) -> ServiceData:
        """
        Deletes the filteredIPA structure from the process.
        """
        return cls.execute_soa_method(
            method_name='deletefilteredIPA',
            library='Manufacturing',
            service_date='2008_12',
            service_name='IPAManagement',
            params={'processes': processes},
            response_cls=ServiceData,
        )

    @classmethod
    def generateSearchScope(cls, processes: List[BusinessObject]) -> IPAManagementGenerateSearchScopeResponse:
        """
        find the IPA under the given process (for each process) and retrives the bomlines from under it.
        """
        return cls.execute_soa_method(
            method_name='generateSearchScope',
            library='Manufacturing',
            service_date='2008_12',
            service_name='IPAManagement',
            params={'processes': processes},
            response_cls=IPAManagementGenerateSearchScopeResponse,
        )

    @classmethod
    def getFilteredIPA(cls, processes: List[BusinessObject]) -> IPAManagementGetFilteredIPAResponse:
        """
        Return the filteredIPA structure from the process.
        """
        return cls.execute_soa_method(
            method_name='getFilteredIPA',
            library='Manufacturing',
            service_date='2008_12',
            service_name='IPAManagement',
            params={'processes': processes},
            response_cls=IPAManagementGetFilteredIPAResponse,
        )
