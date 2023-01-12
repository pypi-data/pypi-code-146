from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReassignParticipantInfo(TcBaseObj):
    """
    A structure containing  a list of input objects  whose participant roles are reassigned, assignee to reassign from,
    assignee to reassign to, a list of participant types, a boolean to indicate all participant types and comments.
    
    :var itemRevs: List of ItemRevision objects to reassign participants roles.
    :var fromAssignee: The business object (User, GroupMember or a ResourcePool) to be replaced with the toAssignee
    business object.
    :var toAssignee: The business object (User, GroupMember or a ResourcePool) to replace the fromAssignee business
    object.
    :var participantTypes: List of participant types to be reassigned.  Valid types are:
    - ProposedResponsibleParty
    - ProposedReviewer
    - ChangeImplementationBoard
    - ChangeReviewBoard
    - ChangeSpecialist1
    - ChangeSpecialist2
    - ChangeSpecialist3
    - Analyst
    - Requestor
    
    
    Custom participant types are also allowed.
    :var allParticipantTypes: If true, all the participant roles for the fromAssignee will be considered for
    reassignment.  The values provided in the participantTypes list will be ignored.
    
    If false, only the participant roles provided in the particpantTypes list will be considered.
    :var comments: A comment provided during reassignment.
    :var clientId: A unique string supplied by the caller. This ID is used to identify the return data elements and
    partial errors associated with the input structure.
    """
    itemRevs: List[ItemRevision] = ()
    fromAssignee: BusinessObject = None
    toAssignee: BusinessObject = None
    participantTypes: List[str] = ()
    allParticipantTypes: bool = False
    comments: str = ''
    clientId: str = ''


@dataclass
class ReassignParticipantOutput(TcBaseObj):
    """
    Contains clientId and a list of objects on which the reassign operation failed.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify the return data elements and
    partial errors associated with the input structure.
    :var failedItemRevs: A list of ItemRevision objects on which the reassign operation failed.
    """
    clientId: str = ''
    failedItemRevs: List[ItemRevision] = ()


@dataclass
class ReassignParticipantResponse(TcBaseObj):
    """
    Contains a list of failed objects information and ServiceData.
    
    :var failedObjects: A list of failed objects information.
    :var serviceData: The modified participant objects are returned along with partial errors.
    """
    failedObjects: List[ReassignParticipantOutput] = ()
    serviceData: ServiceData = None
