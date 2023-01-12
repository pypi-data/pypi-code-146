from __future__ import annotations

from tcsoa.gen.Core._2008_06.DataManagement import BOWithExclusionIn
from tcsoa.gen.Core._2007_06.DataManagement import BaseClassInput
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2010_04.DataManagement import DatasetInfo, DisplayableSubBusinessObjectsResponse, GetAvailableBusinessObjectTypesResponse, CreateDatasetsResponse, LocalizedPropertyValuesInfo, LocalizableStatusResponse, LocalizableStatusInput, LocalizedPropertyValuesList, GetDatasetCreationRelatedInfoResponse2, PropertyInfo
from tcsoa.gen.Core._2010_04.Session import LHNShortcutInputs, MultiPreferenceResponse2, GetShortcutsResponse
from tcsoa.gen.Core._2010_04.LanguageInformation import TranslationStatusResponse, LanguageResponse
from typing import List
from tcsoa.gen.Core._2007_01.Session import ScopedPreferenceNames
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def getShortcuts(cls, shortcutInputs: LHNShortcutInputs) -> GetShortcutsResponse:
        """
        This operation gets the sections and corresponding content in Left Hand Navigation task pane given the section
        name and the corresponding preference name for the current session user. The preference name is the key to look
        up section content stored in preference.    In the rich client, the LHN sections are Quick Links, Open Items,
        History, Favorites and I Want To. The user can organize Teamcenter data in these sections during runtime, which
        is persisted in the preference. The Quick Links section provides a quick access point to the user`s home
        folder, work list, favorite Web links, projects, saved searches, and View Markup. The Open Items section lists
        Teamcenter components currently opened in the active perspective. The History section lists Teamcenter
        components opened before, but currently closed. The Favorites section contains the Favorites container and
        Teamcenter components the user added there for quick access. The I Want To section contains commands configured
        by default or configured by the user.
        
        Use cases:
        The user logs in to the rich client and retrieves Quick Links, Open Items, History, Favorites and I Want To
        task pane section for Left Hand Navigation.
        
        Exceptions:
        >Service Exception    Thrown if there is an empty or invalid section name.
        """
        return cls.execute_soa_method(
            method_name='getShortcuts',
            library='Core',
            service_date='2010_04',
            service_name='Session',
            params={'shortcutInputs': shortcutInputs},
            response_cls=GetShortcutsResponse,
        )

    @classmethod
    def getPreferences2(cls, preferenceNames: List[ScopedPreferenceNames]) -> MultiPreferenceResponse2:
        """
        This operation takes an input structure which contains a scope value and vector of preference names. The return
        type of this operation is the MultiPreferencesResponse2 structure whose elements are the ServiceData and the
        vector of ReturnedPreferences2 structure.
        """
        return cls.execute_soa_method(
            method_name='getPreferences2',
            library='Core',
            service_date='2010_04',
            service_name='Session',
            params={'preferenceNames': preferenceNames},
            response_cls=MultiPreferenceResponse2,
        )


class DataManagementService(TcService):

    @classmethod
    def isPropertyLocalizable(cls, inputInfo: List[LocalizableStatusInput]) -> LocalizableStatusResponse:
        """
        The operation is used to determine if string-type property is localizable or not and can retrieve the
        localizable status for ONE or MORE properties.
        
        Use cases:
        Determine whether a string property is marked as localizable property 
        
        User needs to use this service operation to determine a string property is localizable first before he can add
        the translations to the value of this property.
        """
        return cls.execute_soa_method(
            method_name='isPropertyLocalizable',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'inputInfo': inputInfo},
            response_cls=LocalizableStatusResponse,
        )

    @classmethod
    def setLocalizedProperties(cls, info: LocalizedPropertyValuesInfo) -> ServiceData:
        """
        This operation allows user to set or modify the display values for a localized property on a single object.
        This sets the property values for a single property on an object in different locales. With the display values
        capability, each localized string property could have different language translations associated with that.
        
        Please be aware of the following: 
        - This operation is only used to set the secondary (not the master) values of the localized property. User can
        still package the master value (with localization status marked as "M") in the 'LocalizedPropertyValuesInfo'
        structure, however, the operation will ignore and skip the master value during the process.
        - This operation is only used to set the localization values for one property. If you want to set the localized
        values for multiple properties, please use operation 'setLocalizedPropertyValues'().
        
        """
        return cls.execute_soa_method(
            method_name='setLocalizedProperties',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ServiceData,
        )

    @classmethod
    def setLocalizedPropertyValues(cls, info: List[LocalizedPropertyValuesInfo]) -> ServiceData:
        """
        Sets the property values for multiple properties on a single object in different locales. With the display
        values capability, each localized string property could have different language translations associated with
        that. This operation allows user to set or modify the display values for the localized properties on a single
        object.
        
        It should be noted that this operation is only used to set the secondary (not the master) values of the
        localized properties. User can still package the master value (with localization status marked as "M") in the
        'LocalizedPropertyValuesInfo' structure, however, the operation will ignore and skip these master values during
        the process.
        """
        return cls.execute_soa_method(
            method_name='setLocalizedPropertyValues',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ServiceData,
        )

    @classmethod
    def createDatasets(cls, input: List[DatasetInfo]) -> CreateDatasetsResponse:
        """
        This operation creates a list of Dataset objects, sets the requested attribute data, adds named references,
        fetches write tickets for files that will be uploaded as named references and creates the specified relation
        type between created Dataset and input container object. The caller needs to convert the structure members from
        the output Core::_2010_04::Datamanagement::CommitDatasetFileInfo to the input
        Core::_2006_03::Filemanagement::CommitDatasetFileInfo if the caller wants to use the 2010_04  version of
        createDatasets in combination with commitDatasetFiles.
        """
        return cls.execute_soa_method(
            method_name='createDatasets',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateDatasetsResponse,
        )

    @classmethod
    def findDisplayableSubBusinessObjectsWithDisplayNames(cls, input: List[BOWithExclusionIn]) -> DisplayableSubBusinessObjectsResponse:
        """
        This operation returns sub Business Object names that are displayable to the login user in the object creation
        dialog and their display names for each Primary Business Object given as the input.  Returned Business Object
        lists have exclusions of Business Objects and their secondary Business Objects as specified in the input. This
        returns the hierarchy of displayable objects for each Business Object it returns.
        """
        return cls.execute_soa_method(
            method_name='findDisplayableSubBusinessObjectsWithDisplayNames',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'input': input},
            response_cls=DisplayableSubBusinessObjectsResponse,
        )

    @classmethod
    def getAvailableTypesWithDisplayNames(cls, classes: List[BaseClassInput]) -> GetAvailableBusinessObjectTypesResponse:
        """
        This operation returns Business Object names and their display names for each primary Business Object given as
        the input.  Returned Business Object lists have exclusions of Business Objects and their secondary Business
        Objects as specified in the input. If any of the returned Business Objects is also a primary Business Object
        then this operation may not return its secondary Business Objects by default. In order to return its secondary
        Business Objects also, it is required to add this Business Object name to following preference
        TYPE_DISPLAY_RULES_list_types_of_subclasses.
        Please see the Preferences and Environment Variables Reference documentation for preference
        TYPE_DISPLAY_RULES_list_types_of_subclasses for more information.
         This is a lightweight way of getting all displayable Business Objects by name rather than model object.
        """
        return cls.execute_soa_method(
            method_name='getAvailableTypesWithDisplayNames',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'classes': classes},
            response_cls=GetAvailableBusinessObjectTypesResponse,
        )

    @classmethod
    def getDatasetCreationRelatedInfo2(cls, typeName: str, parentObject: BusinessObject) -> GetDatasetCreationRelatedInfoResponse2:
        """
        This operation pre-populates Dataset creation information, default new Dataset name and Tool names, for a
        specified Dataset type.  This operation is used to get all the information associates with the specified
        Dataset prior to the creation operation. The returned default new Dataset name may be determined by the parent
        container object.
        """
        return cls.execute_soa_method(
            method_name='getDatasetCreationRelatedInfo2',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'typeName': typeName, 'parentObject': parentObject},
            response_cls=GetDatasetCreationRelatedInfoResponse2,
        )

    @classmethod
    def getLocalizedProperties(cls, info: List[PropertyInfo]) -> LocalizedPropertyValuesList:
        """
        Typically business object property values are returned in the locale of the current session, this operation
        returns desired property values in any of the supported locales of the Teamcenter server.  String type
        properties may be localized with values for each supported locale, this operation will return the translated
        values for one or more desired locales.
        
        Use cases:
        Retrieve the localized values for localizable property
        
        When running Teamcenter in language environment other than the English, user wants to see the localized
        property value to be displayed in corresponding language in the UI.   This operation can be used to fulfill
        this requirement. By providing the desired business object, internal name of the properties, and specific
        locale name(s), this operation will return the localized property value(s) in that particular locale(s).
        """
        return cls.execute_soa_method(
            method_name='getLocalizedProperties',
            library='Core',
            service_date='2010_04',
            service_name='DataManagement',
            params={'info': info},
            response_cls=LocalizedPropertyValuesList,
        )


class LanguageInformationService(TcService):

    @classmethod
    def getAllTranslationStatuses(cls) -> TranslationStatusResponse:
        """
        Retrieves the full set of translation statuses: their enumeration, localized name and description. 
        Currently, the translation statuses in the Teamcenter system includes: "Master", "Approved", "Pending",
        "In-Review", and "Invalid"
        """
        return cls.execute_soa_method(
            method_name='getAllTranslationStatuses',
            library='Core',
            service_date='2010_04',
            service_name='LanguageInformation',
            params={},
            response_cls=TranslationStatusResponse,
        )

    @classmethod
    def getLanguagesList(cls, scenario: str) -> LanguageResponse:
        """
        Retrieves a list of languages according to different scenarios as specified in the input parameter. 
        All the returned language names are in the Java-standard format.
        """
        return cls.execute_soa_method(
            method_name='getLanguagesList',
            library='Core',
            service_date='2010_04',
            service_name='LanguageInformation',
            params={'scenario': scenario},
            response_cls=LanguageResponse,
        )
