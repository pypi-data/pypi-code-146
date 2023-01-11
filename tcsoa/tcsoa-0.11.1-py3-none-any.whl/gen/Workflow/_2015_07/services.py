from __future__ import annotations

from tcsoa.gen.Workflow._2015_07.Workflow import CreateSignoffs
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class WorkflowService(TcService):

    @classmethod
    def addSignoffs(cls, signoffs: List[CreateSignoffs]) -> ServiceData:
        """
        This operation adds signoffs to a workflow task. The signoffs can be added as adhoc-signoffs or it can be used
        to staff profiles. The signoff members can be group members or resource pools. When an address list is
        provided, the members of the address list are used to create and add signoffs to the task. The signoffs can be
        added as review signoffs, acknowledge signoffs and notify signoffs. This operation allows to designate added
        reviewers as required or optional.
        
        Use cases:
        Following are four different use cases to add the signoffs &ndash;
        Use case 1: Add adhoc signoff
        To add an adhoc signoff, signoffMember specified as part of 'CreateSignoffInfo' structure can either be a
        GroupMember, Resource Pool or an address list. For this use case, value for 'origin' in 'CreateSignoffInfo'
        should be NULLTAG.
        
        Use case 2: Add profile signoff
        In this use case, the signoffMember specified as part of the 'CreateSignoffInfo' structure has to satisfy the
        signoff profile. Value for the 'origin' should be the signoff profile object and 'originType' should be
        "SOA_EPM_SIGNOFF_ORIGIN_PROFILE".
        
        Use case 3: Add subset of the  members of the  address list as signoff
        User may want to add subset of the members of an address list as signoffs. In this use case, the 'origin'
        should be the address list object and 'originType' should be "SOA_EPM_SIGNOFF_ORIGIN_ADDRESSLIST".  Note that
        members of the address list are always added as adhoc signoffs.
        
        Use case 4: Add signoff as required or optional
        User may specify the signoff decision is required or optinal for the added reviewer . By default the signoff is
        "Optional" signoff.This can be done by adding string member 'signoffRequired' in 'CreateSignoffInfo'.To
        designate the added reviwer as required signoff the string value will be "RequiredUnmodifiable" which cannot be
        manually overridden to "Optional". One Possible value is "RequiredModifiable" It indicates sign off decision is
        required, which can be manually overridden to "Optional".
        
        Exceptions:
        >Teamcenter::Soa::Server::ServiceException:
        """
        return cls.execute_soa_method(
            method_name='addSignoffs',
            library='Workflow',
            service_date='2015_07',
            service_name='Workflow',
            params={'signoffs': signoffs},
            response_cls=ServiceData,
        )
