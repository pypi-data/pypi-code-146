from __future__ import annotations

from tcsoa.gen.UiConfig._2014_11.UiConfig import GetUIConfigInput, GetUIConfigResponse, SaveUiConfigurations
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getUIConfigs(cls, getUiConfigsIn: List[GetUIConfigInput]) -> GetUIConfigResponse:
        """
        This operation returns information used by the client to render the User Interface. The information returned
        includes command and column configuration information.
        
        Use cases:
        Use Case 1: Request UI Configuration(s) based on the current login user
        Client requests the column and/or command information for one or more client scopes using this operation and
        scope as login user.
        
        Use Case 2: Request UI Configuration(s) based on a specific Teamcenter scope
        Client requests the column and/or command information for one or more client scopes using this operation and
        scope as Role, Site or Group.
        """
        return cls.execute_soa_method(
            method_name='getUIConfigs',
            library='UiConfig',
            service_date='2014_11',
            service_name='UiConfig',
            params={'getUiConfigsIn': getUiConfigsIn},
            response_cls=GetUIConfigResponse,
        )

    @classmethod
    def saveUiConfigs(cls, saveUiConfigsIn: SaveUiConfigurations) -> ServiceData:
        """
        This service operation saves column and command configuration information to the Teamcenter database.  A
        Teamcenter client may use this information to render the user interface as the user navigates the Teamcenter
        client.  Default configurations are created using the Business Modeler IDE and installed with Teamcenter.
        
        Use cases:
        Use Case 1: User level column configuration
        
        A User wants to change the default column configuration for a Client Scope when he is logged into the client. 
        The saved configuration will override the default configuration for the user's applicable role, group or site.  
        
        Use Case 2: Administrator level column and command configuration
        An Administrator wants to change the UI configurations for Client Scope URI for a specific Group, Role, or
        User.  Columns may be reordered, removed, or if removed, added back to a specific configuration.  Commands and
        command collections may be reordered, hidden or unhidden.  The Business Modeler IDE must be used to create new
        commands, commands and command collections.
        """
        return cls.execute_soa_method(
            method_name='saveUiConfigs',
            library='UiConfig',
            service_date='2014_11',
            service_name='UiConfig',
            params={'saveUiConfigsIn': saveUiConfigsIn},
            response_cls=ServiceData,
        )
