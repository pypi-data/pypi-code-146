from __future__ import annotations

from tcsoa.gen.Administration._2018_11.IRM import GetSessionInfoTicketResponse, GetSessionInfoFromTicketResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Administration._2018_11.OrganizationManagement import UserConsentStatement


class IRMService(TcService):

    @classmethod
    def getSessionInfoFromTicket(cls, sessionInfoTicket: str) -> GetSessionInfoFromTicketResponse:
        """
        This operation gets all the session information in the form of key values map only if valid sessionInfoTicket
        is provided by client. Each key corresponds to particular session attribute like user, roles, groups, project
        teams, and licenses. For each entry in the keys array, the corresponding entry in the values array contains the
        values for that specific session attribute. Session information returned from this operation is used during
        read expression evaluation in external clients to determine the READ privilege to the current logged in user on
        the indexed Teamcenter data.
        
        Use cases:
        VDS (Visualization Data Server) has no user concept or connection authentication by design. TC SessionInfo
        passed to VDS clients after valid Teamcenter login but no validation is done by VDS today. Due to this
        shortcoming VDS is potential for spoofing, user session hacking and session reuse. To overcome this issue two
        new service operations are proposed and will be used. Calling client VDS uses getSessionInfoTicket operation to
        get encrypted (tamper proof) data packet and preserves the encrypted string. VDS calls SOA
        GetSessionInfoFromTicket with this ticket to get back the user session information. GetSessionInfoFromTicket
        returns back the session information only if the ticket is not expired.
        """
        return cls.execute_soa_method(
            method_name='getSessionInfoFromTicket',
            library='Administration',
            service_date='2018_11',
            service_name='IRM',
            params={'sessionInfoTicket': sessionInfoTicket},
            response_cls=GetSessionInfoFromTicketResponse,
        )

    @classmethod
    def getSessionInfoTicket(cls) -> GetSessionInfoTicketResponse:
        """
        This operation returns User, Group, Session Info, Site identifier and Ticket Expiry Time in the form of an
        encrypted string. Encrypted string ticket returned from this operation is used by getSessionInfoFromTicket
        operation to retrieve the session info.
        
        Use cases:
        VDS has no user concept or connection authentication by design. Teamcenter session information is passed to VDS
        clients after valid Teamcenter login but no validation is done by VDS today. Due to this shortcoming VDS is
        potential for spoofing, user session hacking and session reuse. To overcome this issue 2 new service operations
        are proposed and will be used. Calling client VDS uses getSessionInfoTicket to get encrypted (tamper proof)
        data packet and preserves the encrypted string. VDS client calls getSessionInfoFromTicket with this ticket to
        get back the user session information. getSessionInfoFromTicket returns back the session information only if
        the ticket is not expired and valid.
        
        Exceptions:
        >Partial errors
        """
        return cls.execute_soa_method(
            method_name='getSessionInfoTicket',
            library='Administration',
            service_date='2018_11',
            service_name='IRM',
            params={},
            response_cls=GetSessionInfoTicketResponse,
        )


class OrganizationManagementService(TcService):

    @classmethod
    def getUserConsentStatement(cls) -> UserConsentStatement:
        """
        This operation will return consent statement for the locale the user is logged in. If there is no consent
        statement found for the user&rsquo;s locale then master locale consent statement as per localization definition
        will be returned.
        """
        return cls.execute_soa_method(
            method_name='getUserConsentStatement',
            library='Administration',
            service_date='2018_11',
            service_name='OrganizationManagement',
            params={},
            response_cls=UserConsentStatement,
        )

    @classmethod
    def recordUserConsent(cls, userConsent: bool) -> ServiceData:
        """
        This operation records the user&rsquo;s consent to the General Data Protection Regulation (GDPR).
        """
        return cls.execute_soa_method(
            method_name='recordUserConsent',
            library='Administration',
            service_date='2018_11',
            service_name='OrganizationManagement',
            params={'userConsent': userConsent},
            response_cls=ServiceData,
        )
