from __future__ import annotations

from tcsoa.gen.Core._2020_01.ProjectLevelSecurity import ProjectTeamPagedResponse, UserProjectsAndPrivilegeResponse, ChildStructureResponse, GroupRoleNode, SetPrivilegeForUserInput, ProjectTeamPagedInput, ProjectPrivilegeResponse, AddOrRemoveProjectMemberInput
from tcsoa.gen.Core._2020_01.DataManagement import IDContextOutput, IdentifierTypesOut, IdentifierTypesIn, IDDispRuleCreateIn
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.BusinessObjects import WorkspaceObject, TC_Project
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def setUserPrivilege(cls, inputs: List[SetPrivilegeForUserInput]) -> ServiceData:
        """
        Set the privilege of the given User objects in ProjectTeam of the given TC_Project.
        
        Use cases:
        This service allows the project team administrator to achieve the following use cases.
        
        Use Case 1: The project team administrator sets a list of User objects to be non-privileged in the ProjectTeam
        of a TC_Project.
        Use Case 2: The project team administrator sets a list of User objects to be privileged in the ProjectTeam of a
        TC_Project.
        Use Case 3: The project team administrator sets a list of User objects to be project team administrator in the
        ProjectTeam of a TC_Project.
        """
        return cls.execute_soa_method(
            method_name='setUserPrivilege',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def addOrRemoveProjectMembers(cls, inputs: List[AddOrRemoveProjectMemberInput]) -> ServiceData:
        """
        Adds or removes GroupMember objects or Group objects to/from the ProjectTeam of the given TC_Project.
        
        Use cases:
        Use Case 1: The login user selects a TC_Project and adds some Group or GroupMember objects to the ProjectTeam.
        Use Case 2: The login user selects a TC_Project and removes some Group or GroupMember objects from the
        ProjectTeam.
        """
        return cls.execute_soa_method(
            method_name='addOrRemoveProjectMembers',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def getFirstLevelProjectTeamStructure(cls, input: ProjectTeamPagedInput) -> ProjectTeamPagedResponse:
        """
        This operations returns the paginated output of the first level nodes of the ProjectTeam for the given
        TC_Project object.
        
        Use cases:
        Select a TC_Project object to display all first level nodes in the ProjectTeam tree.
        """
        return cls.execute_soa_method(
            method_name='getFirstLevelProjectTeamStructure',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'input': input},
            response_cls=ProjectTeamPagedResponse,
        )

    @classmethod
    def getModifiableProjects(cls, startIndex: int, pageSize: int) -> UserProjectsAndPrivilegeResponse:
        """
        This operation returns the TC_Project objects that the login user can modify. The TC_Project objects in the
        response are based on the pagination input.
        
        Use cases:
        A User loads all modifiable project.
        """
        return cls.execute_soa_method(
            method_name='getModifiableProjects',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'startIndex': startIndex, 'pageSize': pageSize},
            response_cls=UserProjectsAndPrivilegeResponse,
        )

    @classmethod
    def getPrivilegeInProjects(cls, projects: List[TC_Project]) -> ProjectPrivilegeResponse:
        """
        This operation returns the privilege of the current user in each TC_Project object in the input.
        
        Use cases:
        When the login user checks the privilege in a list of TC_Project objects, the operation returns the privilege
        value of the login user of each project.
        """
        return cls.execute_soa_method(
            method_name='getPrivilegeInProjects',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'projects': projects},
            response_cls=ProjectPrivilegeResponse,
        )

    @classmethod
    def getProjectTeamChildNodes(cls, project: TC_Project, node: GroupRoleNode, depth: int) -> ChildStructureResponse:
        """
        The operation returns child nodes for the given Group node or a Role node in the ProjectTeam tree based on the
        given depth.
        
        Use cases:
        Expanding a Group or a Role node in a Project Team tree, the child nodes are returned.
        """
        return cls.execute_soa_method(
            method_name='getProjectTeamChildNodes',
            library='Core',
            service_date='2020_01',
            service_name='ProjectLevelSecurity',
            params={'project': project, 'node': node, 'depth': depth},
            response_cls=ChildStructureResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def createIdDisplayRules(cls, idDispRuleCreIns: List[IDDispRuleCreateIn]) -> ServiceData:
        """
        This operation creates the ID Display Rules (IdDispRule) with the input ID Context information.
        ID Display Rule contains the list of ID Contexts and their order. Based on the order of the ID Contexts
        defined, the system evaluates the display name of the Item and ItemRevision from their Alternate IDs.
        
        ID Context (IdContext), represents the context information under which the OEM defines the unique IDs of their
        Item and ItemRevision. This context information is used when Teamcenter users define the unique IDs of Item and
        ItemRevision objects.
        
        User can set one of the ID Display Rules as the current ID Display Rule. The current ID Display Rule is used to
        evaluate the display names of the Item and ItemRevision. In case the ID Context of the Alternate ID with the
        Item and ItemRevision object does not match with that of the current ID Display Rule then system uses the
        default ID Display Rule to evaluate the display names of Item and ItemRevision objects.
        """
        return cls.execute_soa_method(
            method_name='createIdDisplayRules',
            library='Core',
            service_date='2020_01',
            service_name='DataManagement',
            params={'idDispRuleCreIns': idDispRuleCreIns},
            response_cls=ServiceData,
        )

    @classmethod
    def getIdContexts(cls, inputObjs: List[WorkspaceObject]) -> IDContextOutput:
        """
        This operation fetches all instances of the ID Context objects (IdContext) from the Teamcenter database
        applicable for the input objects of type Item and ItemRevision based on defined ID Context Rules
        (IdContextRule) by the system administrators.
        
        This operation queries ID Context Rule objects and fetches the ID Context objects based on the input Item,
        ItemRevision or null. The input is the identifiable type defined on the ID Context Rules. For a null input, it
        returns the Id Context objects where the identifiable type is null.
        All ID Context objects from the Teamcenter data base are returned in case input object is other than Item,
        ItemRevision or null. An empty input list would also return all ID Context objects from the Teamcenter data
        base.
        
        IdContext objects represents the context information under which the OEM defines the unique IDs of their Item
        and ItemRevision objects. This context information is used when Teamcenter users define the unique IDs of Item
        and ItemRevision objects.
        
        Alternate and Alias IDs of Teamcenter are the example of the such unique IDs of Item and ItemRevision. Users
        define Alternate and Alias IDs with the help of the ID Context as one of the unique attribute of the ID.
        """
        return cls.execute_soa_method(
            method_name='getIdContexts',
            library='Core',
            service_date='2020_01',
            service_name='DataManagement',
            params={'inputObjs': inputObjs},
            response_cls=IDContextOutput,
        )

    @classmethod
    def getIdentifierTypes(cls, identifierTypesIn: List[IdentifierTypesIn]) -> IdentifierTypesOut:
        """
        This operation fetches the applicable Identifier types for the input objects of type Item and/or ItemRevision
        along with the input IdContext object. System queries the ID Context Rules defined in Teamcenter database and
        retrives the Identifier types.
        
        Alternate and Alias IDs are defined in Teamcenter as instances of business object of type Identifier. ID
        Context, of business object type IdContext, represents the context information under which the OEM defines the
        unique IDs of their Item and ItemRevision. This context information is used when Teamcenter users define the
        Alternate and Alias IDs of Item and ItemRevision objects.
        
        ID Context Rules are defined as instances of business object type IdContextRule in Teamcenter database. These
        rules map the combination of ID Context and the object type e.g.  Item or ItemRevision, called Identifiable
        types, to the type of the Identifier applicable in the context.
        
        This operation also returns the other applicable objects for which Alternate IDs along with the input objects
        can be defined. In case of input objects of type Item, this operation returns the list of revision objects of
        the Item, and in case of input objects of type ItemRevision, this operation returns the Item object as the
        applicable object for which Alternate IDs can be defined.
        """
        return cls.execute_soa_method(
            method_name='getIdentifierTypes',
            library='Core',
            service_date='2020_01',
            service_name='DataManagement',
            params={'identifierTypesIn': identifierTypesIn},
            response_cls=IdentifierTypesOut,
        )
