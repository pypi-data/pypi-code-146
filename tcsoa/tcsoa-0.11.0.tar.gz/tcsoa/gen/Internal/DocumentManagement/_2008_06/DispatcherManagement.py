from __future__ import annotations

from tcsoa.gen.BusinessObjects import DispatcherServiceConfig
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConfigInput(TcBaseObj):
    """
    The 'ConfigInput' structure is used to filter source dataset type, derived dataset type, and service available for
    DispatcherServiceConfig business objects query.
    
    :var sourceDatasetTypeName: The input source dataset type name.  Set to empty string (use double quotes to specify
    empty string) to query all source dataset type name.
    :var derivedDatasetTypeName: The input derived dataset type name. Set to empty string (use double quotes to specify
    empty string) to query all derived dataset type name.
    :var serviceAvailable: The input service available state.  Set to 0 means for false state, set to 1 means for true
    state, and set to negative/minus 1 means to ignore service available state.
    """
    sourceDatasetTypeName: str = ''
    derivedDatasetTypeName: str = ''
    serviceAvailable: int = 0


@dataclass
class ConfigOutput(TcBaseObj):
    """
    This structure contains the output list DispatcherServiceConfig business objects and the 'Service Data'.
    
    :var configOutputData: List of DispatcherServiceConfig business objects, one for each 'ConfigInput' in the list.
    :var svcData: The' Service Data'. Partial errors and failures are updated and returned through this object.
    """
    configOutputData: List[ConfigOutputData] = ()
    svcData: ServiceData = None


@dataclass
class ConfigOutputData(TcBaseObj):
    """
    This structure contains the output list of DispatcherServiceConfig business objects, one for each 'ConfigInput' in
    the list.
    
    :var svcConfig: List of DispatcherServiceConfig business objects.  Can be empty if no object found.
    """
    svcConfig: List[DispatcherServiceConfig] = ()
