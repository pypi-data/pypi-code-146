from __future__ import annotations

from tcsoa.gen.Internal.Administration._2007_06.Authorization import AuthorizationInfo, AccessorInfo, AccessorAccessibleNamesList
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Internal.Administration._2007_06.PreferenceManagement import PreferencesDeleteInput, PreferenceResponse, PreferencesImportInput, PreferenceExportResponse, PreferencesExportInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class PreferenceManagementService(TcService):

    @classmethod
    def importPreferences(cls, importPrefs: PreferencesImportInput) -> ServiceData:
        """
        Imports preferences from the specified input file, at the specified location (as seen from the end-user), for
        the specified categories and following the specified import action.
        """
        return cls.execute_soa_method(
            method_name='importPreferences',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={'importPrefs': importPrefs},
            response_cls=ServiceData,
        )

    @classmethod
    def createPreferenceCategories(cls, categoryNames: List[str]) -> ServiceData:
        """
        Creates a new preference category for each provided category name. 
        Only Site administrators can create a new category. 
        A category helps to sort preferences by categories. For example, all security related preferences are
        categorized under a category called "Security". 
        Teamcenter provides most of the category out-of-the-box. Customers can add new categories as required. 
        If no category is provided while creating a preference, it is stored under the "General" category.
        
        Use cases:
        Create a new preference category:
        Site administrator can create a new category of type "MyReservation" using the createPreferenceCategories
        operation by providing a unique name (e.g. "MyReservation") as the category name. Multiple names can be
        provided to create more than one category.
        """
        return cls.execute_soa_method(
            method_name='createPreferenceCategories',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={'categoryNames': categoryNames},
            response_cls=ServiceData,
        )

    @classmethod
    def deletePreferences(cls, deletePrefs: List[PreferencesDeleteInput]) -> ServiceData:
        """
        This operation is deprecated starting Tc10.0.0. Please use the 'deletePreferencesAtLocations' operation
        instead. 
        
        It enables the deletion of preference instances at any location, provided the logged-in user has the needed
        privileges: users can delete their own preference instances; administrators have the additional possibility to
        delete at other locations (site level, group level, role level, and other users) by specifying a target object
        in the 'PreferencesDeleteInput' structure.
        
        Use cases:
        1. Users to delete a preference instance:
        - Either provide a preference name and preference location as "USER" as part of 'PreferenceDeleteInput'
        structure,
        - Or provide a preference name and user object UID as part of 'PreferenceDeleteInput' structure. 
        
        
        
        2. Group or site administrators to delete a preference instance for location other than their user: 
        Provide a preference name and an object UID for the user, role or group from which the preference instance
        needs to be removed. The administrator must have the needed privilege on the targeted location.
        """
        return cls.execute_soa_method(
            method_name='deletePreferences',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={'deletePrefs': deletePrefs},
            response_cls=ServiceData,
        )

    @classmethod
    def exportPreferences(cls, exportPrefs: PreferencesExportInput) -> PreferenceExportResponse:
        """
        Exports preferences of the logged-in user for the specified location (as seen from the logged-in user) and
        categories.
        """
        return cls.execute_soa_method(
            method_name='exportPreferences',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={'exportPrefs': exportPrefs},
            response_cls=PreferenceExportResponse,
        )

    @classmethod
    def getModifiedSitePreferences(cls) -> PreferenceResponse:
        """
        Retrieves the modified site preferences. 
        When values of existing out-of-the-box (OOTB) preferences are changed, or when new preference definitions are
        created, they qualify as modified site preferences.
        """
        return cls.execute_soa_method(
            method_name='getModifiedSitePreferences',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={},
            response_cls=PreferenceResponse,
        )

    @classmethod
    def getNonSessionPreferences(cls, preferenceScope: str, object: BusinessObject) -> PreferenceResponse:
        """
        Get non session preferences given a preference scope and target object. This method can be used by a DBA to ask
        preferences of another user, role or group specifying the scope.
        """
        return cls.execute_soa_method(
            method_name='getNonSessionPreferences',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='PreferenceManagement',
            params={'preferenceScope': preferenceScope, 'object': object},
            response_cls=PreferenceResponse,
        )


class AuthorizationService(TcService):

    @classmethod
    def setAuthorization(cls, inputAuthorization: List[AuthorizationInfo]) -> ServiceData:
        """
        This operation can be used to set authorization rules for the given accessors.  Authorization rules tells what
        administration applications or the administration utilities the given accessor can access in authoring mode.
        The accessor can be either a Group or Role in the Group. Rule domain specifies if the list is either list of
        utilities or list of applications. Valid values for the domain are utility and application.  If some other
        string is specified as rule domain this operation will return error code 290006.  However authorization setting
        for correct domain names will continue. Following are the valid application names and utility names for this
        operation. For more information on authorization rules please refer to Authorization guide in Teamcenter
        documentation.
        
        List of application IDs:
        Organization
        Business_Modeler_IDE
        Access_Manager
        Archive_Restore
        Setup_Wizard
        Workflow_Designer
        PLMXML_Import_Export
        Project
        Subscription_Monitor
        Classification_Admin
        Report_Designer
        Application_Configuration
        EIntegrator_Admin
        Audit_Manager
        Authorization
        Schema_Editor
        Appearance_Configuration
        ADA License
        
        List of utility IDs:
        data_share
        export_recovery
        database_verify
        update_project_data
        data_sync
        dsa_util
        import_export_business_rules
        purge_invalid_subscriptions
        create_change_types
        fsc_admin
        ada_util
        attribute_export
        
        Use cases:
        To set the authorization rules for an accessor through Authorization application.
        """
        return cls.execute_soa_method(
            method_name='setAuthorization',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='Authorization',
            params={'inputAuthorization': inputAuthorization},
            response_cls=ServiceData,
        )

    @classmethod
    def getAuthorization(cls, inputAccessors: List[AccessorInfo]) -> AccessorAccessibleNamesList:
        """
        This operation can be used to get authorization rules for the given accessors.  Authorization rules tells what
        administration applications or the administration utilities the given accessor can access in authoring mode.
        The accessor can be either a Group or Role in the Group. Rule domain specifies if the list is either list of
        utilities or list of applications. Valid values for the domain are "utility" and "application".  If some other
        string is specified as rule domain this operation will return error code 290006.  Following are the valid
        application names and utility names for this operation. For more information on authorization rules please
        refer to Authorization guide in Teamcenter documentation.
        
        Use cases:
        To display authorization rules in authorization application.
        """
        return cls.execute_soa_method(
            method_name='getAuthorization',
            library='Internal-Administration',
            service_date='2007_06',
            service_name='Authorization',
            params={'inputAccessors': inputAccessors},
            response_cls=AccessorAccessibleNamesList,
        )
