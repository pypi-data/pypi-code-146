from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.GlobalMultiSite._2007_12.ImportExport import OwningSiteAndObjs, CallToRemoteSiteResponse, NamesAndValues
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def getRemoteSites(cls, siteType: str) -> ServiceData:
        """
        This operation returns a list of sites registered for the requested type of transfer.
        """
        return cls.execute_soa_method(
            method_name='getRemoteSites',
            library='GlobalMultiSite',
            service_date='2007_12',
            service_name='ImportExport',
            params={'siteType': siteType},
            response_cls=ServiceData,
        )

    @classmethod
    def requestExportToRemoteSites(cls, reason: str, sites: List[BusinessObject], objects: List[BusinessObject], optionSet: BusinessObject, optionNameAndValues: List[NamesAndValues], sessionOptionNamesAndValues: List[NamesAndValues]) -> CallToRemoteSiteResponse:
        """
        This operation exports objects to specified sites using Global Multisite.
        
        Use cases:
        This operation gets invoked from RAC when user does following actions from Navigator or structure manager
        1>    Tools->Export->To Remote Site Via Global Services.
        2>    Tools->Export->To PDX
        3>    Tools->Export->To Briefcase
        """
        return cls.execute_soa_method(
            method_name='requestExportToRemoteSites',
            library='GlobalMultiSite',
            service_date='2007_12',
            service_name='ImportExport',
            params={'reason': reason, 'sites': sites, 'objects': objects, 'optionSet': optionSet, 'optionNameAndValues': optionNameAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=CallToRemoteSiteResponse,
        )

    @classmethod
    def requestImportFromRemoteSites(cls, reason: str, owningSitesAndObjs: List[OwningSiteAndObjs], optionSet: BusinessObject, optionNamesAndValues: List[NamesAndValues], sessionOptionNamesAndValues: List[NamesAndValues]) -> CallToRemoteSiteResponse:
        """
        This operation imports objects to specified sites using Global Multisite.
        
        Use cases:
        This operation is not in use.
        """
        return cls.execute_soa_method(
            method_name='requestImportFromRemoteSites',
            library='GlobalMultiSite',
            service_date='2007_12',
            service_name='ImportExport',
            params={'reason': reason, 'owningSitesAndObjs': owningSitesAndObjs, 'optionSet': optionSet, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=CallToRemoteSiteResponse,
        )
