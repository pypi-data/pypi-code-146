from __future__ import annotations

from tcsoa.gen.UiConfig._2014_11.UiConfig import ColumnConfigData
from tcsoa.gen.BusinessObjects import Fnd0Client, Fnd0AbstractCommand, Fnd0UIConfigCollectionRel, Fnd0CommandCollection, Fnd0ClientScope
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetUIConfigResponse(TcBaseObj):
    """
    DEPRECATED: This structure returns information to the client about column configuration and command applicability.
    The ServiceData contains information about errors encountered during processing.
    
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    :var uiConfigInfo: List of configuration information including command and column information
    """
    serviceData: ServiceData = None
    uiConfigInfo: List[ClientConfigurations] = ()


@dataclass
class ClientConfigurations(TcBaseObj):
    """
    DEPRECATED: This structure contains command and column configuration data for the indicated client.
    
    :var client: The client for which the configurations are applicable.
    :var columnConfigurations: List of column configurations.
    :var commandConfigurations: List of command configurations.
    """
    client: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    commandConfigurations: List[CommandConfigData] = ()


@dataclass
class CommandCollectionInfo(TcBaseObj):
    """
    DEPRECATED: Contains a command collection and indexes to its children commands or command collections.
    
    :var childIsCollection: Flag indicating if the child is a command or a command collection.
    :var childIsVisible: Flag indicating if the command or collection is visible.
    :var childConfigIndex: Index of the child in either the CommandConfigData:commands list or the
    CommandConfigData:cmdsCollections list.
    :var commandCollection: The Teamcenter command collection object.
    """
    childIsCollection: List[bool] = ()
    childIsVisible: List[bool] = ()
    childConfigIndex: List[int] = ()
    commandCollection: Fnd0CommandCollection = None


@dataclass
class CommandConfigData(TcBaseObj):
    """
    DEPRECATED: This structure returns information about the command configuration definitions for a client scope URI.
    
    :var scopeName: The scope for which the command data is applicable.
    :var hostingClient: The hosting client for which the command data is applicable.
    :var clientScope: The client scope URI containing the list of command configurations.
    :var cmdCollections: List of all top level and child command collections in the client scope.
    :var cmdCollectionIndex: Index into cmdCollections list for top level command collections in the client scope.
    :var commands: List of all command children accessible in the client scope.
    :var commandCollectionRels: List of all commandCollectionRel objects that associate top level command collections
    with client scope.
    """
    scopeName: str = ''
    hostingClient: Fnd0Client = None
    clientScope: Fnd0ClientScope = None
    cmdCollections: List[CommandCollectionInfo] = ()
    cmdCollectionIndex: List[int] = ()
    commands: List[Fnd0AbstractCommand] = ()
    commandCollectionRels: List[Fnd0UIConfigCollectionRel] = ()
