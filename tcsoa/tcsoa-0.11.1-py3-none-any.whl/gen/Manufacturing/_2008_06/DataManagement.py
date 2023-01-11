from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.BusinessObjects import MENXObject, PSBOMView, WorkspaceObject, MEActivity
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MEActivityFolderInfo(TcBaseObj):
    """
    TODO
    
    :var activity: The MEActivity object tag in
    cases of update
    :var name: Name of the activity folder that
    needs to created/updated.
    :var description: Description of the acivity folder
    that needs to created or updated.
    :var type: Type of the activity folder that
    needs to be created.
    :var toolInfo: toolInfo
    :var contents: Objects that need to be inserted
    into the activity folder as
    contents.
    :var parentActivities: Parent activity folder into which
    this folder needs to inserted as
    a content.
    :var predecessors: MEActivity folder that need to
    added as predecessors.
    :var attributes: A vector of NameValueStruct  that
    has the name value pairs.
    Through this act_location, time
    and start_time can be set for the
    folder.
    :var complete: Whether the given information
    completely represents the folder
    to be updated.
    This is flag is applicable only
    for completely replacing tools,
    predecessors and contents.
    """
    activity: MEActivity = None
    name: str = ''
    description: str = ''
    type: str = ''
    toolInfo: ActivityToolInfo = None
    contents: List[WorkspaceObject] = ()
    parentActivities: List[MEActivity] = ()
    predecessors: List[MEActivity] = ()
    attributes: List[NameValueStruct] = ()
    complete: bool = False


@dataclass
class MENXObjectInfo(TcBaseObj):
    """
    TODO
    
    :var menxObject: The MENXObject object tag in cases of update
    :var name: Name of the MENXObject that needs to created or updated.
    :var description: Description of the MENXObject that needs to created or updated.
    :var type: Type of the MENXObject that needs to created.
    :var subType: Sub-Type of the MENXObject that needs to created.
    :var attributes: A vector of NameValueStruct  that has the name value pairs.
    Through this the attributes of the MENXObject like double_attrs,
    double_keys, int_attrs, int_keys, string_attrs, string_keys can be set.
    """
    menxObject: MENXObject = None
    name: str = ''
    description: str = ''
    type: str = ''
    subType: str = ''
    attributes: List[NameValueStruct] = ()


@dataclass
class NameValueStruct(TcBaseObj):
    """
    TODO
    
    :var name: Title of the attribute that
    needs to be set
    :var values: Values of the attribute to be set
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class ActivityToolInfo(TcBaseObj):
    """
    TODO
    
    :var processBV: The context bom view
    :var toolOccThreadChains: The context bom view
    """
    processBV: PSBOMView = None
    toolOccThreadChains: OccThreadChainsSet = None


@dataclass
class CreateOrUpdateMEActivityFolderResponse(TcBaseObj):
    """
    TODO
    
    :var successfullyProcessedMEAct: successfullyProcessedMEAct
    :var serviceData: serviceData
    """
    successfullyProcessedMEAct: SuccessFullyProcessedMapMEAct = None
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateMENXObjectResponse(TcBaseObj):
    """
    TODO
    
    :var successfullyProcessedMENXObj: successfullyProcessedMENXObj
    :var serviceData: serviceData
    """
    successfullyProcessedMENXObj: SuccessFullyProcessedMapMENXObj = None
    serviceData: ServiceData = None


"""
OccThreadChainsSet
"""
OccThreadChainsSet = Dict[int, List[str]]


"""
SuccessFullyProcessedMapMEAct
"""
SuccessFullyProcessedMapMEAct = Dict[int, MEActivity]


"""
SuccessFullyProcessedMapMENXObj
"""
SuccessFullyProcessedMapMENXObj = Dict[int, MENXObject]
