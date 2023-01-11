from __future__ import annotations

from tcsoa.gen.Administration._2012_09.PreferenceManagement import PreferenceResponseWithFileTicket, ImportPreferencesAtLocationsIn, ImportPreferencesAtLocationDryRunResponse, GetPreferencesResponse, SetPreferences2In, PreferencesAtLocationIn, ImportPreferencesAtLocationDryRunIn, PreferenceLocation, SetPreferencesDefinitionIn, SetPreferencesAtLocationsIn, GetPreferencesAtLocationsResponse
from tcsoa.gen.Administration._2012_09.UserManagement import GroupMemberInput, GetUserGroupMembersInputData, GetUserGroupMembersResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class UserManagementService(TcService):

    @classmethod
    def getUserGroupMembers(cls, inputObjects: List[GetUserGroupMembersInputData]) -> GetUserGroupMembersResponse:
        """
        This operation retrieves information of all group members for a list of users specified in the list of
        GetUserGroupMembersInputData inputs. The information includes Group object, Role object, User object, status,
        group admin privilege, and default role flag of the user group members. The returned results could contain
        information only for the active group members of the user or both active and inactive group members of the user
        depending on option includeInactive setting in GetUserGroupMembersInputData.
        
        Exceptions:
        >If system errors occur.
        """
        return cls.execute_soa_method(
            method_name='getUserGroupMembers',
            library='Administration',
            service_date='2012_09',
            service_name='UserManagement',
            params={'inputObjects': inputObjects},
            response_cls=GetUserGroupMembersResponse,
        )

    @classmethod
    def setGroupMemberProperties(cls, inputObjects: List[GroupMemberInput]) -> ServiceData:
        """
        This operation updates the properties on one or more GroupMembers.The following properties may be updated:
        membership_data_source, ga,default_role, status.
        """
        return cls.execute_soa_method(
            method_name='setGroupMemberProperties',
            library='Administration',
            service_date='2012_09',
            service_name='UserManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )


class PreferenceManagementService(TcService):

    @classmethod
    def importPreferencesAtLocationDryRun(cls, importPreferences: ImportPreferencesAtLocationDryRunIn) -> ImportPreferencesAtLocationDryRunResponse:
        """
        Pretends to import the preferences from the input file into the specified location.
        On the contrary to the import operation, the dry run operates on one location at a time.
        The objective is to gather information on what would be the final result for proceeding with the real import
        operation.
        
        This operation takes a vector of structure representing the preferences and the location where to import.
        The valid values for the location parameter in the PreferenceLocation structure are: Site, Group, Role, User.
        The Site value means that the preference will be imported for the entire organization.
        Group or Role means that the value will be imported for the Group or Role of the current logged-in user.
        It is also possible to import for the non-current user.
        """
        return cls.execute_soa_method(
            method_name='importPreferencesAtLocationDryRun',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'importPreferences': importPreferences},
            response_cls=ImportPreferencesAtLocationDryRunResponse,
        )

    @classmethod
    def importPreferencesAtLocations(cls, importPreferenceIn: ImportPreferencesAtLocationsIn) -> PreferenceResponseWithFileTicket:
        """
        Imports the preferences from the input file into the specified locations.
        
        This operation takes a vector of structure representing the preferences and the location where to import.
        The valid values for the location parameter in the PreferenceLocation structure are: Site, Group, Role, User.
        The Site value means that the preference will be imported for the entire organization.
        Group or Role means that the value will be imported for the Group or Role of the current logged-in user.
        It is also possible to import for the non-current user.
        """
        return cls.execute_soa_method(
            method_name='importPreferencesAtLocations',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'importPreferenceIn': importPreferenceIn},
            response_cls=PreferenceResponseWithFileTicket,
        )

    @classmethod
    def removeStalePreferenceInstancesAtLocations(cls, locations: List[PreferenceLocation]) -> ServiceData:
        """
        Since the preference manager utility has a cleanup mode that does the same thing as
        removeStalePreferenceInstancesAtLocations-_2012_09-PreferenceManagementService. There is no need of a SOA
        operation to achieve this.
        """
        return cls.execute_soa_method(
            method_name='removeStalePreferenceInstancesAtLocations',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'locations': locations},
            response_cls=ServiceData,
        )

    @classmethod
    def setPreferences2(cls, preferenceInput: List[SetPreferences2In]) -> ServiceData:
        """
        Allows the logged-in user to set the values for the given preferences for the logged-in user.
        Values can only be given to preferences already defined in the system and for which the protection scope allows
        the user to give a value. Otherwise, the operation will return an error for this preference.
        Preference name and values are specified in input structure 'SetPreferences2In'. 
        """
        return cls.execute_soa_method(
            method_name='setPreferences2',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'preferenceInput': preferenceInput},
            response_cls=ServiceData,
        )

    @classmethod
    def setPreferencesAtLocations(cls, setPreferenceIn: List[SetPreferencesAtLocationsIn]) -> ServiceData:
        """
        Sets the values for the specified preferences and locations. <br/><br/>The input 'PreferenceLocation' structure
        (within the 'SetPreferencesAtLocationsIn' structure) contains 2 mutually exclusive parameters: <ol><li>The
        location parameter, for which values can be for this specific operation: <ul type="circle"><li>"Site": The
        preference will be set for the entire organization.
        <li>"Group": the preference will be set for the group of the logged-in user. 
        <li>"Role": The preference will be set for the role of the logged-in user. 
        <li>"User": The preference will be set for the logged-in user.
        </ul>
        <li> The object parameter, which represents the User, Role or Group where to set the values. This is to be used
        when the target is for the non-logged-in user. Note that the caller must have permission to set the preference
        values for the specified object. 
        </ol>
        """
        return cls.execute_soa_method(
            method_name='setPreferencesAtLocations',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'setPreferenceIn': setPreferenceIn},
            response_cls=ServiceData,
        )

    @classmethod
    def setPreferencesDefinition(cls, preferenceInput: List[SetPreferencesDefinitionIn]) -> ServiceData:
        """
        Allows system administrators to create the definitions for new preferences, or to modify existing preference
        definitions. If the preferences do not exist, it sets the definitions and values for the specified preferences.
        If the preferences already exist (i.e. they have been defined already), it modifies them. 
        
        This is a system administrator level operation. The intent is that only the system administrator should create
        a preference. However, this could be needed from non-directly-related user interactions. Therefore, the
        decision to make a call to this operation is delegated to its caller. This operation takes a list of
        'SetPreferencesDefinitionIn' structures, which contains a 'PreferenceDefinition' structure. This structure can
        be simplified in case of preference modifications. 
        
        Its parameters are: 
        
        - category: The category where the preference is stored. If the input string is empty, the parameter will not
        be taken into account. However, in case the preference has not been created yet, it will be assumed that the
        preference will go under the "General" category. If the string is not empty, and if the category does not
        exists in the system already, new category would be created and the preference would go under this category.  
        
        
        
        - description: The textual explanation of what the preference does. If the input string is empty, the parameter
        will not be taken into account. 
        
        
        
        - type: The preference type. Valid values are:
        
        
                                0: String preference. 
                                1: Logical preference. 
                                2: Integer preference. 
                                3: Double preference. 
                                4: Date preference. 
                        If the preference does not exist, this piece of information will be needed. If the preference
        exists and if the value is provided and if a preference instance already exist with the old type and the
        conversion from the old type to the new one is not possible and an error would be returned. 
        
        - protectionScope: The level at which the preference is protected. Valid values are:                        
        
        
                                "User": All users can provide a value for the preference. 
                                "Role": Only system and group administrators can provide a value. 
                                "Group": Only system and group administrators can provide a value. 
                                "Site": Only system administrators can provide a value. 
                                "System": Only system administrators can provide a value. Furthermore, the protection
        scope cannot be changed from then on. If the preference does not exist, this information is mandatory. If the
        preference exists and the protection scope string is empty, the parameter will not be taken into account. If
        the  preference exists and the protection scope string is not empty, the code will consider this to be a
        modification. 
        - isEnvEnabled: Status if the preference value can be set through an environment variable, in which case it
        will come from that location first. This piece of information will always be taken into consideration.
        
        
        
        - isOOTBPreference: Not used for this operation.
        
        """
        return cls.execute_soa_method(
            method_name='setPreferencesDefinition',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'preferenceInput': preferenceInput},
            response_cls=ServiceData,
        )

    @classmethod
    def deletePreferenceDefinitions(cls, preferenceNames: List[str], deleteAllCustomDefinitions: bool) -> ServiceData:
        """
        Deletes the definition and all value instances of the specified preferences.
        Since preferences will not be differentiated as Custom or COTS going forward, the input parameter
        deleteAllCustomDefinitions will not be used when performing this operation.
        """
        return cls.execute_soa_method(
            method_name='deletePreferenceDefinitions',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'preferenceNames': preferenceNames, 'deleteAllCustomDefinitions': deleteAllCustomDefinitions},
            response_cls=ServiceData,
        )

    @classmethod
    def deletePreferencesAtLocations(cls, deletePreferencesAtLocationIn: List[PreferencesAtLocationIn]) -> ServiceData:
        """
        Deletes the given preference instances at the specified location only. 
        This operation takes a list of 'PreferencesAtLocationIn' structures representing the preferences to delete and
        the location. 
        The location is a 'PreferenceLocation' structure, which contains 2 mutually exclusive parameters:
        1. The location parameter, for which values can be for this specific operation:
        - "Site": The preference will be deleted from current site location.
        - "Group": The preference will be deleted for the group of the logged-in user.
        - "Role": The preference will be deleted for the role of the logged-in user.
        - "User": The preference will be deleted for the logged-in user.
        
        
        2. The object parameter, which represents the User, Role or Group where to delete the values. This is to be
        used when the target is for the non-logged-in user.
        
        Use cases:
        A preference instance is present at the user level, and it needs to be removed.
        """
        return cls.execute_soa_method(
            method_name='deletePreferencesAtLocations',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'deletePreferencesAtLocationIn': deletePreferencesAtLocationIn},
            response_cls=ServiceData,
        )

    @classmethod
    def getPreferences(cls, preferenceNames: List[str], includePreferenceDescriptions: bool) -> GetPreferencesResponse:
        """
        Retrieves the values for the preferences specified in the list of names, as seen by the current logged-in user,
        based on current application context. If there are no values in current application context, values are
        retrieved from default application context if exists.
        If the list is empty or its first value is equal to "*", all the preferences as seen by the logged-in user will
        be returned (not only the preference instances created by the logged-in user).
        
        Use cases:
        Retrieving the value for a series of preferences.
        """
        return cls.execute_soa_method(
            method_name='getPreferences',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'preferenceNames': preferenceNames, 'includePreferenceDescriptions': includePreferenceDescriptions},
            response_cls=GetPreferencesResponse,
        )

    @classmethod
    def getPreferencesAtLocations(cls, getPreferenceAtLocationIn: List[PreferencesAtLocationIn], includePreferenceDescriptions: bool) -> GetPreferencesAtLocationsResponse:
        """
        Retrieves the values for the specified preferences and locations.<br/>The input structure contains:<ul><li>A
        vector preference names. If the list is empty or its first element is "*", all the preferences for the
        specified locations (and only for preference instances at this location) are being returned.
        <li>A <font face="Courier" height="10">PreferenceLocation'  structure, which contains 2 mutually exclusive
        parameters:<ol><li>The location parameter, for which values can be for this specific operation:<ul
        type="circle"><li>"Site": The preference will be retrieved either as overwritten or as an out-of-the-box (OOTB)
        value (whichever gives a value first). 
        <li>"Group": The preference will be retrieved for the group of the logged-in user. 
        <li>"Role": The preference will be retrieved for the role of the logged-in user. 
        <li>"User": The preference will be retrieved for the logged-in user.
        </ul>
        <li> The object parameter, which represents the User, Role or Group where to retrieve the values. This is to be
        used when the target is for the non-logged-in user.
        </ol>
        </ul>
        
        Use cases:
        1. The logged-in user needs to know the preference value given at her/his Role or Group level.
        2. The logged-in user needs to know the preference value given by another user, or a Role/Group than hers/his.
        """
        return cls.execute_soa_method(
            method_name='getPreferencesAtLocations',
            library='Administration',
            service_date='2012_09',
            service_name='PreferenceManagement',
            params={'getPreferenceAtLocationIn': getPreferenceAtLocationIn, 'includePreferenceDescriptions': includePreferenceDescriptions},
            response_cls=GetPreferencesAtLocationsResponse,
        )
