from __future__ import annotations

from tcsoa.base import TcService


class PreferenceManagementService(TcService):

    @classmethod
    def refreshPreferences(cls) -> bool:
        """
        Refreshes the preference values stored in the server cache, so that they are synchronized with the latest
        values. 
        
        This situation might happen when the preferences for a given user are being changed in 2 different sessions, or
        when an administrator is making changes to the Site / Role or Group preferences. 
        <Calling the refreshPreferences operation will retrieve the updated values.
        
        Exceptions:
        >If the operation has failed.
        """
        return cls.execute_soa_method(
            method_name='refreshPreferences',
            library='Administration',
            service_date='2011_05',
            service_name='PreferenceManagement',
            params={},
            response_cls=bool,
        )
