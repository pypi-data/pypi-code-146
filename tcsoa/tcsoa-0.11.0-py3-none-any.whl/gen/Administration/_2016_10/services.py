from __future__ import annotations

from tcsoa.gen.Administration._2016_10.UserManagement import GetCurrentCountryPageInfoResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def saveAndValidateCurrentCountry(cls, selectedcountry: str) -> ServiceData:
        """
        This operation saves the selected country value for the session user and then validates that this user
        hasn&rsquo;t violated the global license contract. If the validation of the global contract fails, the
        user&rsquo;s current country  will still be set to the selected country. Note, the selectedCountry attribute is
        not validated against the ISO 3166-1 alpha-2 standard.
        """
        return cls.execute_soa_method(
            method_name='saveAndValidateCurrentCountry',
            library='Administration',
            service_date='2016_10',
            service_name='UserManagement',
            params={'selectedcountry': selectedcountry},
            response_cls=ServiceData,
        )

    @classmethod
    def getCurrentCountryPageInfo(cls) -> GetCurrentCountryPageInfoResponse:
        """
        This operation retrieves current configuration of country selection. The configuration is a list of selectable
        countries, the initial country to be displayed, and a customer configurable confidentiality statement.
        
        Use cases:
        This will be used for both RAC and AW to populate their current country selection pages.
        """
        return cls.execute_soa_method(
            method_name='getCurrentCountryPageInfo',
            library='Administration',
            service_date='2016_10',
            service_name='UserManagement',
            params={},
            response_cls=GetCurrentCountryPageInfoResponse,
        )
