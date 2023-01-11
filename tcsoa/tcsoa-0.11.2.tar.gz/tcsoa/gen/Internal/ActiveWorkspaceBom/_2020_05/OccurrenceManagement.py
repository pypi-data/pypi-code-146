from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0ProductContextInfo, WorkspaceObject, POM_object
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UpdateContentBasedOnRevInput(TcBaseObj):
    """
    This structure contains WorkspaceObject and Awb0ProductContextInfo needed to reconfigure and update the content for
    impacted occurrences of the WorkspaceObject.
    
    :var workspaceObject: WorkspaceObject whose occurrences in content needs to be reconfigured. Supported type :
    ItemRevision
    :var productContext: The Awb0ProductContextInfo object containing configuration information.
    :var requestPref: A map (string, list of string) of preference names and values. Preference names and values are
    case sensitive.
    """
    workspaceObject: WorkspaceObject = None
    productContext: Awb0ProductContextInfo = None
    requestPref: RequestPreference11 = None


@dataclass
class UpdateWorkingContextInput(TcBaseObj):
    """
    UpdateWorkingContextInput contains working context container on which configuration and recipe to be saved.
    
    :var productInfo: Awb0ProductContextInfo containing the product and configuration.
    :var workingContext: Object to which configuration and recipe to be saved. Valid business object types are:
    Fnd0AppSession.
    :var saveResult: If true, persist results on Fnd0StructureContextData; otherwise, results will not persisted on
    Fnd0StructureContextData.
    :var operation: The operation to be performed. Valid values  are: "Create", "SaveAs"
    Create : Indicates user have performed create operation
    SaveAs : Indicates user have performed SaveAs operation
    """
    productInfo: Awb0ProductContextInfo = None
    workingContext: POM_object = None
    saveResult: bool = False
    operation: str = ''


"""
The map which can have a key and value pair, used for occurrences expansion filters or criteria or options. The key and value are case sensitive.
"""
RequestPreference11 = Dict[str, List[str]]
