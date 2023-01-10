from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2020_05.RevisionRuleAdministration import CreateOrUpdateRevRuleResp, CreateUpdateRevRuleInput, RevRuleInfoResponse
from tcsoa.base import TcService


class RevisionRuleAdministrationService(TcService):

    @classmethod
    def getRevisionRuleInfo(cls, revRule: str) -> RevRuleInfoResponse:
        """
        Retreives description, rule entries and nested effectivity information for input RevisionRule.
        
        Use cases:
        User selects RevisionRule to view the details like rule entries so that user can make informed decision on
        configuring the content.
        """
        return cls.execute_soa_method(
            method_name='getRevisionRuleInfo',
            library='Internal-StructureManagement',
            service_date='2020_05',
            service_name='RevisionRuleAdministration',
            params={'revRule': revRule},
            response_cls=RevRuleInfoResponse,
        )

    @classmethod
    def createOrUpdateRevisionRule(cls, inputData: CreateUpdateRevRuleInput) -> CreateOrUpdateRevRuleResp:
        """
        Creates or updates a RevisionRule based on input information.
        
        Use cases:
        Use Case 1: Creation of Revision Rule:
        RevisionRule can be created from "Revision Rules" sub-location where all existing rules along with their
        clauses will be listed, given that user have privileges to create a RevisionRule.
        
        Use Case 2: Modification of existing Revision Rule:
        RevisionRules can be modified inside "Revision Rules" sub-location, given that user have privileges to modify a
        RevisionRule. Clauses of a RevisionRule can be re-ordered to change the precedence by moving the clause up/down
        using the corresponding controls. New clause from list of available clauses can be added or a clause can be
        removed from existing list of clauses.
        
        Use Case 3: Modification of existing Revision Rule inside ACE:
        Adhoc changes to the RevisionRule clauses can be performed to configure product structure. Addition of new
        clauses, removal of exisiting clauses or re-ordering of the clauses can be done to create a 'modified' version
        copy of the original RevisionRule which will be available to the current user only.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateRevisionRule',
            library='Internal-StructureManagement',
            service_date='2020_05',
            service_name='RevisionRuleAdministration',
            params={'inputData': inputData},
            response_cls=CreateOrUpdateRevRuleResp,
        )
