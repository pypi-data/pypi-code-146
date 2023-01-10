from __future__ import annotations

from typing import List
from tcsoa.gen.Participant._2018_11.Participant import ParticipantInfoInput, ParticipantInfo, ReassignParticipantResponse, ReassignParticipantInfoInput, ParticipantResponse
from tcsoa.base import TcService


class ParticipantService(TcService):

    @classmethod
    def reassignParticipants(cls, input: List[ReassignParticipantInfoInput]) -> ReassignParticipantResponse:
        """
        Reassigns the participant roles from one user to another for a given list of participant types on the input
        list of objects. The Particpant for the fromAssignee user is replaced with the Participant for the toAssignee
        user. If the toAssignee user already exists as participant, then the fromAssignee user will not be replaced.
        
        Use cases:
        In Active Workspace Client, it will be required to reassign participants of a particular Participant Types from
        an old assignee value to new assignee on WorkspaceObject.
        """
        return cls.execute_soa_method(
            method_name='reassignParticipants',
            library='Participant',
            service_date='2018_11',
            service_name='Participant',
            params={'input': input},
            response_cls=ReassignParticipantResponse,
        )

    @classmethod
    def removeParticipants(cls, input: List[ParticipantInfo]) -> ParticipantResponse:
        """
        Removes participants from the WorkspaceObject. The participants can be removed from EPMJob or other
        WorkspaceObject objects that are provided as input
        
        Use cases:
        In the Active Workspace Client, participants added to workflow can be removed from the Participant page of the
        EPMTask in that workflow. The participants added to any WorkspaceObject can be removed from the participant
        page of the WorkspaceObject.
        """
        return cls.execute_soa_method(
            method_name='removeParticipants',
            library='Participant',
            service_date='2018_11',
            service_name='Participant',
            params={'input': input},
            response_cls=ParticipantResponse,
        )

    @classmethod
    def addParticipants(cls, input: List[ParticipantInfoInput]) -> ParticipantResponse:
        """
        Creates Participant objects and adds them to the input WorkspaceObject. These participants can be added to
        WorkspaceObject objects that are targets in a workflow or the workflow (EPMJob) itself. The participants can
        then be used by workflow handlers to assign tasks during workflow execution.
        
        Use cases:
        In Active Workspace Client, this operation can be used for following two cases:
        
        1.    Adding participants to WorkspaceObject from Participants tab.
        2.    Adding participants to a Workflow (EPMJob) from the Participants tab shown when a task is selected. 
        
        The Submit to workflow panel can be used to assign participants configured in the workflow.  The participants
        selected in the panel can be added based on the configuration to either the EPMJob or the first target in the
        workflow using this operation.
        """
        return cls.execute_soa_method(
            method_name='addParticipants',
            library='Participant',
            service_date='2018_11',
            service_name='Participant',
            params={'input': input},
            response_cls=ParticipantResponse,
        )
