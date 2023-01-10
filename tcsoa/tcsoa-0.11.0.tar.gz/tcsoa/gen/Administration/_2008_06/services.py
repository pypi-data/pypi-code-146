from __future__ import annotations

from tcsoa.base import TcService


class PreferenceManagementService(TcService):

    @classmethod
    def lockSitePreferences(cls) -> bool:
        """
        Locks the Site preferences stored in the database. 
        
        This can be used by system administrators only. It is not mandatory to lock Site preferences to make changes,
        but it ensures exclusive write accesses when necessary.
        
        Exceptions:
        >The exception will not contain any error code.
        """
        return cls.execute_soa_method(
            method_name='lockSitePreferences',
            library='Administration',
            service_date='2008_06',
            service_name='PreferenceManagement',
            params={},
            response_cls=bool,
        )

    @classmethod
    def unlockSitePreferences(cls) -> bool:
        """
        Releases the lock set on the site preferences stored in the database. The locking comes from the call to
        lockSitePreferences operation. Only the user who locked the site preferences is allowed to unlock them. As of
        Teamcenter 11.6, due to the re-architecture of preferences from XML storage to database objects, this operation
        is no longer required. So it is deprecated.
        
        Exceptions:
        >The exception will not contain any error code:
        """
        return cls.execute_soa_method(
            method_name='unlockSitePreferences',
            library='Administration',
            service_date='2008_06',
            service_name='PreferenceManagement',
            params={},
            response_cls=bool,
        )
