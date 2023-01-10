from __future__ import annotations

from tcsoa.gen.Internal.Administration._2008_06.IRM import ACLInfoResponse
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def getACLsByType(cls, aclsType: int) -> ACLInfoResponse:
        """
        This operation can be used to get the named Access Control Lists (ACLs) of given type. There are 3 types of
        ACLs in Teamcenter which are of type WORKFLOW, RULETREE and RULEPROJ ACLs. RULETREE ACLs are mainly used Access
        Manager Application, WORLFLOW ACLs are used in Workflow designer application and RULEPROJ ACLs are used in
        Project Administration Application. Following are the integer values corresponding to these types.
        
        0-RULETREE ACLs
        1-WORKFLOW ACLs
        2-RULEPROJ ACLs
        3-ACLs of all types will be fetched
        
        Sending an incorrect integer value as parameter to this operation will not cause any error but the operation
        will not return anything.
        
        
        Use cases:
        This operation can be used in general wherever the ACL names need to be displayed. At present following use
        cases in Teamcenter Rich Application Client (RAC) calls this operation.
        - Display the ACL names in Extra Protection information dialog.
        - Display the ACL names in effective ACL dialog.
        - Display the ACL names in Named ACL panel.
        
        """
        return cls.execute_soa_method(
            method_name='getACLsByType',
            library='Internal-Administration',
            service_date='2008_06',
            service_name='IRM',
            params={'aclsType': aclsType},
            response_cls=ACLInfoResponse,
        )
