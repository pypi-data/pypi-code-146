from __future__ import annotations

from tcsoa.gen.DocumentManagement._2010_04.DigitalSignature import DigitalSignSaveInput, DigtalSigningSaveResponse
from tcsoa.gen.DocumentManagement._2010_04.LaunchDefinition import SessionInfo, UserAgentDataInfo, LDSelectedInputInfo, ServerInfo, LaunchDefinitionResponse
from typing import List
from tcsoa.base import TcService


class DigitalSignatureService(TcService):

    @classmethod
    def digitalSigningSave(cls, saveInput: DigitalSignSaveInput) -> DigtalSigningSaveResponse:
        """
        The digitalSigningSave function will update an existing dataset that has the name referenced uploaded signed
        file.
        """
        return cls.execute_soa_method(
            method_name='digitalSigningSave',
            library='DocumentManagement',
            service_date='2010_04',
            service_name='DigitalSignature',
            params={'saveInput': saveInput},
            response_cls=DigtalSigningSaveResponse,
        )


class LaunchDefinitionService(TcService):

    @classmethod
    def getLaunchDefinition(cls, operation: str, selectedInputs: List[LDSelectedInputInfo], serverInfo: ServerInfo, sessionInfo: SessionInfo, userAgentData: UserAgentDataInfo) -> LaunchDefinitionResponse:
        """
        The Application Launcher (AppLauncher) uses a launch definition XML as input to launch appropriate external
        applications. This operation gathers the data and builds the launch definition XML string. It contains
        information for list of supported tools, business data and tool preferences. The definition XML is based on the
        list of 'LDSelectedInputInfo' structure ( contains WorkspaceObject, related Item, related ItemRevision, related
        control WorkspaceObject business object, request mode and additional information in the form of key value pair
        strings), structure of server information 'ServerInfo' where the operation is initiated, structure of the
        session information 'SessionInfo' of the client from where the operation is initiated, and structure of client
        information 'UserAgentDataInfo' from where the operation is initiated.
        The required input data from the 'LDSelectedInputInfo' structure is the WorkspaceObject business object
        (normally this input is the subtype of WorkspaceObject business object such as Item business object or
        ItemRevision business object or Dataset business object).    The input structures for server, session, and
        client information can be empty.
        
        Use cases:
        Use case1:  View/Markup action from client
        When a user selects an Item or an ItemRevision or a Dataset and performs View/Markup action in the client, the
        system will invoke the getLaunchDefinition operation.
        Use case2:  Office client open
        When a user performs open action on an MSWord Dataset and the client is configured to use AppLauncher for open,
        the system will invoke the getLaunchDefinition operation.
        Use case3: Active Workspace Office client open
        When a user performs open and edit in office client action on an MSWord Dataset and the client is configured to
        use AppLauncher for open, the system will invoke the getLaunchDefinition operation.
        
        """
        return cls.execute_soa_method(
            method_name='getLaunchDefinition',
            library='DocumentManagement',
            service_date='2010_04',
            service_name='LaunchDefinition',
            params={'operation': operation, 'selectedInputs': selectedInputs, 'serverInfo': serverInfo, 'sessionInfo': sessionInfo, 'userAgentData': userAgentData},
            response_cls=LaunchDefinitionResponse,
        )
