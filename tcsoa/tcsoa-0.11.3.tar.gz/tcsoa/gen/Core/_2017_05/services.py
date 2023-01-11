from __future__ import annotations

from tcsoa.gen.Core._2006_03.FileManagement import CommitDatasetFileInfo
from tcsoa.gen.Core._2017_05.ProjectLevelSecurity import ModifyProjectsInfo2, CopyProjectsInfo2, ProjectAssignOrRemoveInput, ProjectInformation2, ProjectsInput, PropagationDataInput, ProjectsOutputResponse
from typing import List
from tcsoa.gen.Core._2012_09.ProjectLevelSecurity import ProjectOpsResponse
from tcsoa.gen.Core._2017_05.FileManagement import ReplaceFileInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def getProjectsForAssignOrRemove(cls, projectsInput: List[ProjectsInput]) -> ProjectsOutputResponse:
        """
        This operation retrieves the assigned projects to the input data and all available projects where the input
        user is a priveleged member. When multiple business objects are selected this operation retrieves the assigned
        projects which are in common for the complete input data. It also retrieves level or structure information in
        case of ActiveWorkspace Content context. In ActiveWorkspace Content context, if the selected object does not
        have further child objects then level or structure information will not be returned.
        """
        return cls.execute_soa_method(
            method_name='getProjectsForAssignOrRemove',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'projectsInput': projectsInput},
            response_cls=ProjectsOutputResponse,
        )

    @classmethod
    def modifyProjects2(cls, modifyProjectsInfos: List[ModifyProjectsInfo2]) -> ProjectOpsResponse:
        """
        This operation modifies the given list of TC_Project objects using the input specified. The input contains new
        values for all the project properties. Values for properties other than the project team are ignored unless the
        user is the Project Administrator. 
        The entire Project Team, with the exception of the Project Administrator, is replaced with the specified team.
        Therefore, a Project Team Administrator must be specified. If the new Project Team is different than the
        current team, the user performing this operation must be either the Project Administrator or Project Team
        Administrator for the project being modified.
        """
        return cls.execute_soa_method(
            method_name='modifyProjects2',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'modifyProjectsInfos': modifyProjectsInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def copyProjects2(cls, copyProjectInfos: List[CopyProjectsInfo2]) -> ProjectOpsResponse:
        """
        This operation copies the given list of TC_Project objects. The operation also copies any information which is
        in contained in the project. Data such as project team members and any objects assigned to the source project
        will also be copied to the new project. If a project with given project ID exists in the system then this
        operation will return error 101010. The operation will continue with copying the other projects.
        """
        return cls.execute_soa_method(
            method_name='copyProjects2',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'copyProjectInfos': copyProjectInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def setPropagationEnabledProperties(cls, propagationDataInput: List[PropagationDataInput]) -> None:
        """
        The operation sets propagation enabled properties on a given set of objects and performs propagation. This will
        be done either in the same session or a different session depending on the dispatcher configuration. If
        dispatcher is configured and the SOA URL is set correctly in organization application then the request will be
        processed asynchronously. On the otherhand if dispatcher is not configured or the SOA URL is not correctly set
        in the organization application then the request will be processed in the same process.If the operation is
        executed in a different session and it involves a structures then an attempt will be made to recreate the BOM
        window in the new session; to achieve this operation takes a list of BOMWindow objects and re-creates the
        BOMwindow and the contents of the windows (i.e. configuration) by applying the supplied Revision Rule and
        variant configuration information. If the RevisionRuleEntryProps::unitNo is set to -1 then it considers default
        unitNo or use the input RevisionRule object with no changes. If no value specified for
        RevisionRuleEntryProps::unitNo, then the input RevisionRule object used as modified/transient rule with unitNo
        as 0. If the value of preference PSM_enable_product_configurator is true, then Product Configurator variant
        rule will be honored.
        
        Use cases:
        Set propagation enabled property in context of some configured window in structure manager or active workspace
        context editor.
        """
        return cls.execute_soa_method(
            method_name='setPropagationEnabledProperties',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'propagationDataInput': propagationDataInput},
            response_cls=None,
        )

    @classmethod
    def createProjects2(cls, projectInfos: List[ProjectInformation2]) -> ProjectOpsResponse:
        """
        This operation creates TC_Project objects using the given input information. This operation also supports
        creation of TC_Project object in hierarchical configuration. If the project with given project ID exists in the
        system then this operation will return unique id violation error 101010. However, creation of rest of the
        projects will continue.
        
        Use cases:
        This operation provides the following use cases for Teamcenter objects:
        
        Use Case 1: Create parent program in project application.
        * Administartor user will open Project application. User will fill all details like ProjectID, Project Name,
        Team members. Here we are creating parent program so user will select "Use Program Security" flag.
        * Once the user input is received, client makes subsequent invocation to this operation to execute
        createProjects2.
        * The method is invoked. New program is created using values passed in. Newly created program will display on
        left side in Project application.
        
        Use Case 2: Create a project with associated program.
        * Administartor user will open Project application. User will fill all details like ProjectID, Project Name,
        Team members. Here we are creating project which will associated with
        program so user will not select "Use Program Security" flag. User will also select parent program from the list
        of values.
        * Once the user input is received, client makes subsequent invocation to this operation to execute
        createProjects2.
        * The method is invoked. New project is created using values passed in. Newly created project will display on
        left side in Project application under select parent program.
        """
        return cls.execute_soa_method(
            method_name='createProjects2',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'projectInfos': projectInfos},
            response_cls=ProjectOpsResponse,
        )

    @classmethod
    def assignOrRemoveObjectsFromProjects(cls, assignOrRemoveInput: List[ProjectAssignOrRemoveInput]) -> ServiceData:
        """
        This operation assigns the given set of workspace objects to the given projects. Similarly, it removes an
        additional set of given workspace objects from the same set of given projects. If the input contains revision
        rule and or variant rule these will be applied to the given set of objects for traversing the structure i.e.
        the project will be propagated to the objects which are obtained by applying these configurations. If the
        additional input parameters type options and depth are specified; the assign or remove operation will filter
        out additional objects based on the inputs. If user is not privileged to assign objects to any of the given
        projects then this operation will return the error 101014 : You have insufficient privilege to assign object to
        a project. Similarly, if user is not privileged to remove objects from any of the given projects then this
        operation will return error 101015: You have insufficient privilege to remove object from a project. These
        errors will not terminate processing of rest of the objects.
        
        Use cases:
        - Assign projects to objects specified in an input by applying the given revision rules and variant rules for
        4GD structures. 
        - Assign project to objects specified in the input by applying the current BOM window in classic BOM 
        - Assign projects to objects specified without applying any configuration information
        
        """
        return cls.execute_soa_method(
            method_name='assignOrRemoveObjectsFromProjects',
            library='Core',
            service_date='2017_05',
            service_name='ProjectLevelSecurity',
            params={'assignOrRemoveInput': assignOrRemoveInput},
            response_cls=ServiceData,
        )


class FileManagementService(TcService):

    @classmethod
    def commitDatasetFilesInBulk(cls, commitInput: List[CommitDatasetFileInfo]) -> ServiceData:
        """
        This operation uploads files to a Teamcenter volume and associates them to a Dataset. The mechanism for a
        client application adding files to a Teamcenter volume contains several steps. This mechanism is implemented in
        the com.teamcenter.soa.client.FileManagementUtility class, which provides this functionality to clients in a
        consistent, reusable package. 
        
        This operation is supported only for internal Siemens PLM purposes. Customers should not invoke this operation.
        
        Use cases:
        This operation uploads files to a Teamcenter volume and associates them as named references of a Dataset. All
        data is bulk saved to improve performance.
        """
        return cls.execute_soa_method(
            method_name='commitDatasetFilesInBulk',
            library='Core',
            service_date='2017_05',
            service_name='FileManagement',
            params={'commitInput': commitInput},
            response_cls=ServiceData,
        )

    @classmethod
    def replaceFiles(cls, inputs: List[ReplaceFileInput]) -> ServiceData:
        """
        This operation replaces an existing volume file with a new file that has already been uploaded to a transient
        volume.  It uploads the file from the transient volume to the regular Teamcenter volume.  The original volume
        file is replaced with the new file, and the ImanFile references the new file.  Note that there is no new
        ImanFile object created.  This operation includes the ability to change the original file name or retain its
        existing value.  The file type on the ImanFile object is updated to match the value from the input write
        tickets.  The tickets for the upload to the transient volume can be obtained by calling
        'getTransientFileTicketsForUpload'.
        
        This operation is used for replacing an existing file in a volume when the original file content is to be
        replaced with a newly encrypted file.
        
        Use cases:
        There are very specific cases where this operation should be used. One use case is where encryption software
        needs to replace the contents of the original file with the encrypted contents.
        """
        return cls.execute_soa_method(
            method_name='replaceFiles',
            library='Core',
            service_date='2017_05',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
