from __future__ import annotations

from tcsoa.gen.UiConfig._2014_11.UiConfig import ColumnConfig, ScopeInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ResetUIConfigInput(TcBaseObj):
    """
    Contains input information required to reset UI configurations from the Teamcenter database.
    
    :var scope: The scope of the desired UI configuration information. This includes the name of the scope (i.e. a
    user, group or role) and scope query parameter information.
    :var columnConfigIds: List of column configuration IDs
    """
    scope: ScopeInput = None
    columnConfigIds: List[str] = ()


@dataclass
class ResetUIConfigResponse(TcBaseObj):
    """
    This structure returns information to the client about column configuration and command applicability. The
    ServiceData contains information about errors encountered during processing.
    
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    :var columnConfigurations: List of effective column configurations.
    """
    serviceData: ServiceData = None
    columnConfigurations: List[ColumnConfig] = ()
