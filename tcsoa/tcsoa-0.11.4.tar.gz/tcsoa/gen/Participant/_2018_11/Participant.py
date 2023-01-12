from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, Participant
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ParticipantInfo(TcBaseObj):
    """
    ParticipantInfo structure contains information about WorkspaceObject and list of Participant objects.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var wso: WorkspaceObject whose participants are modified.
    :var participants: A list of Participant objects.
    :var additionalData: A map (string/list of strings) to send additional information. This is provided for future use
    and will be implemented in future. For example, user can provide comments that can be sent as "COMMENTS" as key and
    user entered comments as values.
    """
    clientId: str = ''
    wso: WorkspaceObject = None
    participants: List[Participant] = ()
    additionalData: KeyValueMap = None


@dataclass
class ParticipantInfoInput(TcBaseObj):
    """
    ParticipantInfoInput structure contains information about WorkspaceObject and list of ParticipantInput structures.
    
    :var wso: The WorkspaceObject on which the particpant is to be added.
    :var additionalData: A map (string/list of strings) to send additional information. This is provided for future use
    and will be implemented in future. For example, user can provide comments that can be sent as "COMMENTS" as key and
    user entered comments as values.
    :var participantInputData: A list of ParticipantInput structures. Each element will contain the assignee and
    corresponding participant type.
    """
    wso: WorkspaceObject = None
    additionalData: KeyValueMap = None
    participantInputData: List[ParticipantInput] = ()


@dataclass
class ParticipantInfoOutput(TcBaseObj):
    """
    ParticipantInfoOutput structure contains information about list of WorkspaceObject objects on which the participant
    failed to get reassigned.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var wsoList: A list of WorkspaceObject objects on which the participants failed to get reassigned.
    :var additionalData: A map (string/list of strings) to send additional information. This is provided for future use
    and will be implemented in future. For example, user can provide comments that can be sent as "COMMENTS" as key and
    user entered comments as values.
    """
    clientId: str = ''
    wsoList: List[WorkspaceObject] = ()
    additionalData: KeyValueMap = None


@dataclass
class ParticipantInput(TcBaseObj):
    """
    ParticipantInput structure contains information about assignee and participant type.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var assignee: The participant which can be a User, GroupMember or a ResourcePool.
    :var participantType: Corresponding participant type to which the assignee will be added. For example
    PROPOSED_RESPONSIBLE_PARTY, PROPOSED_REVIEWERS, CHANGE_SPECIALIST1, CHANGE_SPECIALIST2, CHANGE_SPECIALIST3,
    CHANGE_REVIEW_BOARD, CHANGE_IMPLEMENTATION_BOARD, ANALYST, REQUESTOR.
    """
    clientId: str = ''
    assignee: BusinessObject = None
    participantType: str = ''


@dataclass
class ParticipantResponse(TcBaseObj):
    """
    ParticipantResponse structure contains information about list of ParticipantInfo structures and service data.
    
    :var output: A list of ParticipantInfo structure.
    :var serviceData: The service data.
    """
    output: List[ParticipantInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ReassignParticipantInfoInput(TcBaseObj):
    """
    ReassignParticipantInfoInput structure contains information about WorkspaceObject, old value of assignee, new value
    of assignee, participant types and comments.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var wsoList: A list of WorkspaceObject to reassign participant roles.
    :var fromAssignee: The business object that can be User, GroupMember or ResourcePool to be replaced with the
    toAssignee business object.
    :var toAssignee: The business object that can be User, GroupMember or ResourcePool to replace the fromAssignee
    business object.
    :var participantTypes: A list of Participant types to be reassigned.
    :var allParticipantTypes: If true, all the participant roles for the fromAssignee will be considered for
    reassignment. The values provided in the participantTypes list will be ignored. If false, only the participant
    roles provided in the participantTypes list will be considered.
    :var comment: A comment provided during reassignment.
    :var additionalData: A map (string/list of strings) to send additional information. This is provided for future use
    and will be implemented in future. For example, user can provide comments that can be sent as "COMMENTS" as key and
    user entered comments as values.
    """
    clientId: str = ''
    wsoList: List[WorkspaceObject] = ()
    fromAssignee: BusinessObject = None
    toAssignee: BusinessObject = None
    participantTypes: List[str] = ()
    allParticipantTypes: bool = False
    comment: str = ''
    additionalData: KeyValueMap = None


@dataclass
class ReassignParticipantResponse(TcBaseObj):
    """
    ReassignParticipantResponse structure contains information about list of ParticipantInfoOutput structures and
    service data.
    
    :var output: A list of ParticipantInfoOutput structure.
    :var serviceData: The service data.
    """
    output: List[ParticipantInfoOutput] = ()
    serviceData: ServiceData = None


"""
Structure for passing data in form of key and values.
"""
KeyValueMap = Dict[str, List[str]]
