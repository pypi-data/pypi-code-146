from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2020_12.DataManagement import ObjectLocalizedPropertiesInfo, GetLocalizedPropertiesInput, GetLocalizedPropertiesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def setLocalizedProperties(cls, input: List[ObjectLocalizedPropertiesInfo]) -> ServiceData:
        """
        This operation sets the values for multiple properties on multiple objects in different locales. With the
        display values capability, each localized string property can have different language translations.
        
        Use cases:
        When running Active workspace, user wants to set or modify the localized single or multiple property value
        which displayed in localization panel. This operation can be used to fulfill this requirement. By providing the
        desired business object, internal name of the properties, and specific locale name(s), local value associated
        to the locale and the localization status, this operation can be used to set multiple properties localization
        value(s) with alternative status.
        
        It should be noted that this operation is only used to set the secondary (not the master) values of the
        localized properties. User cannot package the master in the ObjectLocalizedPropertiesInfo structure.
        """
        return cls.execute_soa_method(
            method_name='setLocalizedProperties',
            library='Internal-AWS2',
            service_date='2020_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getLocalizedProperties(cls, input: GetLocalizedPropertiesInput) -> GetLocalizedPropertiesResponse:
        """
        This operation returns desired property values for any of the supported locales of the Teamcenter server.
        String and string array type properties are supported and may be localized with values for each supported
        locale, this operation will return the translated values for the input locales. If no locales are input, it
        will return translations for all supported locales.
        And it will also return the full set of translation statuses: their enumeration, localized display name and
        description for the locale in client session.
        
        Use cases:
        Retrieve the localized values for localizable properties
        
        When running Active workspace, a user may want to see the localized property value to be displayed in
        localization panel. This operation can be used to fulfill this requirement. By providing the desired business
        object, internal name of the properties, and specific locale name(s), this operation will return the localized
        properties value(s) in that particular locale(s) and the status corresponding to localized value(s) in that
        locale(s).
        
        This operation can return the fullTranslationStatuses for all the supported translation statuses for the locale
        in client session.
        """
        return cls.execute_soa_method(
            method_name='getLocalizedProperties',
            library='Internal-AWS2',
            service_date='2020_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetLocalizedPropertiesResponse,
        )
