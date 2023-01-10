from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from tcsoa.gen.Core._2015_10.FileManagement import DatasetDigestInfoResponse, FileDigestInfoResponse
from typing import List
from tcsoa.gen.Core._2006_03.Session import LoginResponse
from tcsoa.gen.Core._2015_10.DataManagement import ReassignParticipantResponse, ReassignParticipantInfo
from tcsoa.gen.Server import ServiceData, TypeSchema
from tcsoa.gen.Core._2007_12.Session import StateNameValue
from tcsoa.base import TcService
from tcsoa.gen.Core._2015_10.Session import TypeDescriptionOptions


class SessionService(TcService):

    @classmethod
    def getTypeDescriptions2(cls, typeNames: List[str], options: TypeDescriptionOptions) -> TypeSchema:
        """
        Gets the Meta data for the named Business Model object types based on the configurations specified by the
        client.  To improve performance, clients can specify to exclude certain Meta data such as LOV References and
        Naming Rule References for the given types.
        If options are not provided this operation returns all meta data associated with given types.
        """
        return cls.execute_soa_method(
            method_name='getTypeDescriptions2',
            library='Core',
            service_date='2015_10',
            service_name='Session',
            params={'typeNames': typeNames, 'options': options},
            response_cls=TypeSchema,
        )

    @classmethod
    def setUserSessionStateAndUpdateDefaults(cls, pairs: List[StateNameValue]) -> ServiceData:
        """
        This operation sets the desired user session state values. This operation also updates the default value of the
        Group, Role and Project when these session states are changed.
        
        To clear a field's value, client needs to pass an empty string "" as the value.
        
        Failure to set a particular state value will result in a Partial Error with the clientId set to the name of the
        state property. State values can be per client session or per server session. Client session state is kept
        separate for each client application sharing the same Teamcenter server session, while server session state is
        shared with all client application sharing the Teamcenter server session.
        
        Valid keys for the session state pairs are:
        
        - currentChangeNotice - The UID of the ChangeNotice business object for this session (client session).This is
        deprecated from release Teamcenter 11.5.
        - refreshPOM - If true the business objects in the POM are refreshed before returning property values.  This
        ensures property data is up-to-date, but is a performance hit (client session).
        - objectPropertyPolicy - The name of the current object property policy. This can also be controlled through
        the ObjectPropertyPolicyManager in the SOA client framework  (client session).
        - maxOperationBracketTime - Time (seconds) to bracket to limit a  POM refresh (client session).
        - maxOperationBracketInactiveTime - Time (seconds) to bracket to limit a  POM refresh (client session).
        - usePolicyOnly - If true, only properties defined in the current Object Property Policy will be returned.
        Objects that are added to the updated list of the ServiceData without named properties by default are returned
        with all properties currently loaded in the POM.
        - formatProperties - If true, the display value of the property will be formatted, if there is an active
        property formatter is attached to it. If false, the display value of the property will not be formatted, even
        if there is an active property formatter attached to it (client session).
        - currentProject - The UID of the Project object (server session).
        - workContex - The UID of the WorkContext object (server session).
        - volume - The UID of the Volume object (server session).
        - local_volume - The UID of the LocalVolume object (server session).
        - groupMember - The UID of the GroupMember object (server session).
        - currentDisplayRule - The UID of the DisplayRule object (server session).
        - currentOrganization - The UID of the Organization object (server session).
        - locationCodePref - The CAGE/Location Code preference. This value is set on the Item attribute
        'fnd0OriginalLocationCode' when Item objects are created (client session).
        - currentChangeItem - The UID of the Change Item Revision business object for this session. This functionality
        is supported from Teamcenter 11.5.
        
        """
        return cls.execute_soa_method(
            method_name='setUserSessionStateAndUpdateDefaults',
            library='Core',
            service_date='2015_10',
            service_name='Session',
            params={'pairs': pairs},
            response_cls=ServiceData,
        )

    @classmethod
    def sponsoredLogin(cls, sponsoringUser: str, password: str, sponsoredUser: str, sponsoredGroup: str, sponsoredRole: str, locale: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the sponsoring user`s credentials and initialize a Teamcenter session for the sponsored user. The
        operation will throw an InvalidCredentialsException as described below.
        
        When the client application is deployed to a 4Tier environment the login operation also contributes to the
        assignment of a Teamcenter server instance to the client session. The sponsoring user, sponsored users and
        sessionDiscriminator are considered in server assignment. 
        Note: The sessionDiscriminator could be blank ("") or have some value (e.g. "session1" or "session2")
        
        Example with blank ("") sessionDiscriminator: 
        - Sponsor1/User1 and Sponsor1/User2 will be assigned to different servers since their access controls are based
        on User1 and User2
        - Sponsor1/User1 and Sponsor2/User1 will be assigned to different servers.
        - Sponsor1/User1 and User1 will be assigned to different servers.
        
        Example with "session1" and "session2" sessionDiscriminator:
        - Sponsor1/User1(session1) and Sponsor1/User1(session1) will be assigned to same servers
        - Sponsor1/User1(session1) and Sponsor1/User1(session2) will be assigned to different servers
        
        Exceptions:
        >When the credentials supplied for the sponsoring user are invalid or the sponsored user's group is invalid or
        the requested locale is not allowed:
        515143: The logon was refused due to invalid username or password
        515144: The logon was refused due to invalid username or password
        515142: The logon was refused due to an invalid group for the sponsored user.
        128001: The logon was refused due to conflict with the encoding of the database instance.
        128002: The logon was refused due to missing localization.
        When the sponsoring user's credentials are valid but this user doesn't belong to "Sponsor" group.
        515145: The logon was refused since sponsoring user did not belong to "Sponsor" group.
        When the sponsoring user's credentials are valid but the userid requesting sponsorship is un-sponsorable.
        515146: The logon was refused since the userid requesting sponsorship is un-sponsorable.
        """
        return cls.execute_soa_method(
            method_name='sponsoredLogin',
            library='Core',
            service_date='2015_10',
            service_name='Session',
            params={'sponsoringUser': sponsoringUser, 'password': password, 'sponsoredUser': sponsoredUser, 'sponsoredGroup': sponsoredGroup, 'sponsoredRole': sponsoredRole, 'locale': locale, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )

    @classmethod
    def sponsoredLoginSSO(cls, sponsoringUser: str, ssoCredentials: str, sponsoredUser: str, sponsoredGroup: str, sponsoredRole: str, locale: str, sessionDiscriminator: str) -> LoginResponse:
        """
        Authenticates the sponsoring user using Single-Sign-On (SSO) credentials and initialize a Teamcenter session
        for the sponsored user client. The username and ssoCredentials arguments are for the sponsoring user and must
        be obtained from Teamcenter's Security Services. The SsoCredentials class offers a simple API to get these
        values. The operation will throw an InvalidCredentialsException as described below.
        
        When the client application is deployed to a 4Tier environment the login operation also contributes to the
        assignment of a Teamcenter server instance to the client session. The sponsoring user, sponsored users and
        sessionDiscriminator are considered in server assignment. 
        Note: The sessionDiscriminator could be blank ("") or have some value (e.g. "session1" or "session2")
        
        Example with blank ("") sessionDiscriminator: 
        - Sponsor1/User1 and Sponsor1/User2 will be assigned to different servers since their access controls are based
        on User1 and User2
        - Sponsor1/User1 and Sponsor2/User1 will be assigned to different servers.
        - Sponsor1/User1 and User1 will be assigned to different servers.
        
        Example with "session1" and "session2" sessionDiscriminator:
        - Sponsor1/User1(session1) and Sponsor1/User1(session1) will be assigned to same servers
        - Sponsor1/User1(session1) and Sponsor1/User1(session2) will be assigned to different servers
        
        Example with "session1" and "session2" sessionDiscriminator:
        - Sponsor1/User1(session1) and Sponsor1/User1(session1) will be assigned to same servers
        - Sponsor1/User1(session1) and Sponsor1/User1(session2) will be assigned to different servers
        
        Exceptions:
        >When the credentials supplied for the sponsoring user are invalid or the sponsored user's group is invalid or
        the requested locale is not allowed:
        515143: The logon was refused due to invalid username or password
        515144: The logon was refused due to invalid username or password
        515142: The logon was refused due to an invalid group for the sponsored user.
        128001: The logon was refused due to conflict with the encoding of the database instance.
        128002: The logon was refused due to missing localization.
        When the sponsoring user's credentials are valid but this user doesn't belong to "Sponsor" group.
        515145: The logon was refused since sponsoring user did not belong to "Sponsor" group.
        When the sponsoring user's credentials are valid but the userid requesting sponsorship is un-sponsorable.
        515146: The logon was refused since the userid requesting sponsorship is un-sponsorable.
        """
        return cls.execute_soa_method(
            method_name='sponsoredLoginSSO',
            library='Core',
            service_date='2015_10',
            service_name='Session',
            params={'sponsoringUser': sponsoringUser, 'ssoCredentials': ssoCredentials, 'sponsoredUser': sponsoredUser, 'sponsoredGroup': sponsoredGroup, 'sponsoredRole': sponsoredRole, 'locale': locale, 'sessionDiscriminator': sessionDiscriminator},
            response_cls=LoginResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def reassignParticipants(cls, reassignParticipantInfo: List[ReassignParticipantInfo]) -> ReassignParticipantResponse:
        """
        Reassigns the participant roles from one user to another for a given list of participant types on the input
        list of objects. The Particpant for the fromAssignee User is replaced with the Particpant for the toAssignee
        User. If the toAssignee User already exists as participant, then the fromAssignee User will not be replaced.
        
        Use cases:
        For Change Management use cases, user may need to reassign participant roles on the change objects like
        analyst, change specialist etc.  This operation can be used to reassign such participants.
        """
        return cls.execute_soa_method(
            method_name='reassignParticipants',
            library='Core',
            service_date='2015_10',
            service_name='DataManagement',
            params={'reassignParticipantInfo': reassignParticipantInfo},
            response_cls=ReassignParticipantResponse,
        )


class FileManagementService(TcService):

    @classmethod
    def getDigestInfoForDatasets(cls, datasets: List[Dataset]) -> DatasetDigestInfoResponse:
        """
        Gets the file digest information for the ImanFile objects contained in the Dataset objects. These digests can
        be used by clients to check for file integrity. Clients must use the same digest algorithm (as returned by this
        operation) to compute the digest on their end and compare with the digest returned by this operation.
        The Teamcenter File Management System (FMS) computes and stores the file digests on the volume if the content
        verification feature is turned on.
        This operation returns digests for binary files only.
        """
        return cls.execute_soa_method(
            method_name='getDigestInfoForDatasets',
            library='Core',
            service_date='2015_10',
            service_name='FileManagement',
            params={'datasets': datasets},
            response_cls=DatasetDigestInfoResponse,
        )

    @classmethod
    def getDigestInfoForFiles(cls, files: List[ImanFile]) -> FileDigestInfoResponse:
        """
        Gets the file digest information for all the ImanFile objects specified using files. These digests can be used
        by clients to check for file integrity. Clients must use the same digest algorithm (as returned by this
        operation) to compute the digest on their end and compare with the digest returned by this operation.
        The Teamcenter File Management System (FMS) computes and stores the file digests on the volume if the content
        verification feature is turned on. 
        This operation returns digests for binary files only.
        """
        return cls.execute_soa_method(
            method_name='getDigestInfoForFiles',
            library='Core',
            service_date='2015_10',
            service_name='FileManagement',
            params={'files': files},
            response_cls=FileDigestInfoResponse,
        )
