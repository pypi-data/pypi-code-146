from __future__ import annotations

from tcsoa.gen.ChangeManagement._2020_01.ChangeManagement import DeriveInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ChangeManagementService(TcService):

    @classmethod
    def deriveChangeItems(cls, deriveInput: DeriveInput) -> ServiceData:
        """
        This operation derives multiple Change Item objects and carry forward its relations based on the
        propagateRelation flag. When applying deep copy rules, if user overridden deep copy information is provided in
        the input, then old relations are propagated to the new ItemRevision based on the input. If no deep copy
        information is provided in the input, the deep rules in the database will apply.
        
        Use cases:
        &bull;    The requestor (who may be the analyst of the ECR) either derives a new change notice to address the
        approved change request or associates the ECR with an existing ECN. The ECN addresses the implementation
        details of the change. It may address multiple change requests. 
        &bull;    Derive an engineering change request (ECR) from a problem report (PR) to determine a solution for the
        problem.
        &bull;    Derive an engineering change notice (ECN) from an ECR to implement the solution to the problem.
        &bull;    Derive a deviation request from a PR to allow a deviation.
        &bull;    Derive an ECN from multiples ECRs.
        """
        return cls.execute_soa_method(
            method_name='deriveChangeItems',
            library='ChangeManagement',
            service_date='2020_01',
            service_name='ChangeManagement',
            params={'deriveInput': deriveInput},
            response_cls=ServiceData,
        )
