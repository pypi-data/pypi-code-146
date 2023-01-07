from typing import Any, Dict, List, cast

from pydantic import Field
from typing_extensions import Annotated, Literal

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA, VersionMode
from rhino_health.lib.endpoints.user.user_dataclass import FutureUser, User
from rhino_health.lib.utils import alias


class ProjectCreateInput(RhinoBaseModel):
    """
    Input arguments for adding a new project.
    """

    name: str
    """@autoapi True The name of the Project"""
    description: str
    """@autoapi True The description of the Project"""
    type: Literal["Validation", "Refinement"]
    """@autoapi True The type of the Project"""
    primary_workgroup_uid: Annotated[str, Field(alias="primary_workgroup")]
    """@autoapi True The unique ID of the Project's Primary Workgroup"""


class Project(ProjectCreateInput, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False

    A Project that exists on the Rhino Health Platform
    """

    uid: str
    """@autoapi True The unique ID of the Project"""
    slack_channel: str
    """@autoapi True Slack Channel URL for communications for the Project"""
    collaborating_workgroups_uids: List[str]
    """@autoapi True A list of unique IDs of the Project's collaborating Workgroups"""
    users: List[User]
    """@autoapi True A list of users in the project"""
    status: Dict
    """@autoapi True The status of the Workgroup"""


class FutureProject(Project):
    """
    @objname Project
    DataClass representing a Project on the Rhino platform.
    """

    users: List[FutureUser]
    _collaborating_workgroups: Any = None
    _primary_workgroup: Any = None
    created_at: str
    """@autoapi True When this AIModel was added"""

    @property
    def primary_workgroup(self):
        """
        Return the primary workgroup associated with this Project

        Returns
        -------
        primary_workgroup: Workgroup
            DataClasses representing the Primary Workgroup of the Project
        """
        if self._primary_workgroup:
            return self._primary_workgroup
        if self.primary_workgroup_uid:
            self._primary_workgroup = self.session.workgroup.get_workgroups(
                [self.primary_workgroup_uid]
            )[0]
            return self._primary_workgroup
        else:
            return None

    @property
    def collaborating_workgroups(self):
        """
        Get the Collaborating Workgroup DataClass of this Project

        .. warning:: Be careful when calling this for newly created objects.
            The workgroups associated with the COLLABORATING_WORKGROUP_UIDS must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the collaborating workgroups

        Returns
        -------
        collaborating_workgroups: List[Workgroup]
            A List of DataClasses representing the Collaborating Workgroups of the Project

        See Also
        --------
        rhino_health.lib.endpoints.workgroup.workgroup_dataclass : Workgroup Dataclass
        """
        if self._collaborating_workgroups:
            return self._collaborating_workgroups
        if self.collaborating_workgroups_uids:
            self._collaborating_workgroups = self.session.project.get_collaborating_workgroups(
                self.uid
            )
            return self._collaborating_workgroups
        else:
            return []

    def add_collaborator(self, collaborator_or_uid):
        """
        Adds COLLABORATOR_OR_UID as a collaborator to this project

        .. warning:: This feature is under development and the interface may change
        """
        from ..workgroup.workgroup_dataclass import Workgroup

        if isinstance(collaborator_or_uid, Workgroup):
            collaborator_or_uid = collaborator_or_uid.uid
        self.session.project.add_collaborator(
            project_uid=self.uid, collaborating_workgroup_uid=collaborator_or_uid
        )
        self._collaborating_workgroups = None
        self.collaborating_workgroups_uids.append(collaborator_or_uid)
        return self

    def remove_collaborator(self, collaborator_or_uid):
        """
        Removes COLLABORATOR_OR_UID as a collaborator from this project

        .. warning:: This feature is under development and the interface may change
        """
        from ..workgroup.workgroup_dataclass import Workgroup

        if isinstance(collaborator_or_uid, Workgroup):
            collaborator_or_uid = collaborator_or_uid.uid
        self.session.project.remove_collaborator(
            project_uid=self.uid, collaborating_workgroup_uid=collaborator_or_uid
        )
        self._collaborating_workgroups = None
        self.collaborating_workgroups_uids.remove(collaborator_or_uid)
        return self

    @property
    def cohorts(self):
        """
        Get Cohorts associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_cohorts : Full documentation
        """
        return self.session.project.get_cohorts(self.uid)

    def get_cohort_by_name(self, name, version=VersionMode.LATEST, **_kwargs):
        """
        Get Cohort associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_cohort_by_name : Full documentation
        """
        return self.session.project.get_cohort_by_name(name, project_uid=self.uid, version=version)

    def search_for_cohorts_by_name(
        self, name, version=VersionMode.LATEST, name_filter_mode=None, **_kwargs
    ):
        """
        Get Cohorts associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.search_for_cohorts_by_name : Full documentation
        """
        return self.session.project.search_for_cohorts_by_name(
            name, project_uid=self.uid, version=version, name_filter_mode=name_filter_mode
        )

    @property
    def data_schemas(self):
        """
        Get Data Schemas associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_data_schemas : Full documentation
        """
        return self.session.project.get_data_schemas(self.uid)

    @property
    def dataschemas(self):
        """
        @autoapi False
        """
        return alias(
            self.data_schemas,
            "dataschemas",
            is_property=True,
            new_function_name="data_schemas",
            base_object="project",
        )()

    def get_data_schema_by_name(self, name, version=VersionMode.LATEST, **_kwargs):
        """
        Get Dataschema associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_data_schema_by_name : Full documentation
        """
        return self.session.project.get_data_schema_by_name(
            name, project_uid=self.uid, version=version
        )

    @property
    def get_dataschema_by_name(self):
        """
        @autoapi False
        """
        return alias(
            self.get_data_schema_by_name,
            "get_dataschema_by_name",
            is_property=True,
            new_function_name="get_data_schema_by_name",
            base_object="project",
        )()

    def search_for_data_schemas_by_name(
        self, name, version=VersionMode.LATEST, name_filter_mode=None, **_kwargs
    ):
        """
        Get Data Schemas associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.search_for_data_schemas_by_name : Full documentation
        """
        return self.session.project.search_for_data_schemas_by_name(
            name, project_uid=self.uid, version=version, name_filter_mode=name_filter_mode
        )

    @property
    def search_for_dataschemas_by_name(self):
        """
        @autoapi False
        """
        return alias(
            self.search_for_data_schemas_by_name,
            "search_for_dataschemas_by_name",
            is_property=True,
            new_function_name="search_for_data_schemas_by_name",
            base_object="project",
        )()

    @property
    def aimodels(self):
        """
        Get AIModels associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_aimodels : Full documentation
        """
        return self.session.project.get_aimodels(self.uid)

    def get_aimodel_by_name(self, name, version=VersionMode.LATEST, **_kwargs):
        """
        Get AIModel associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.get_aimodel_by_name : Full documentation
        """
        return self.session.project.get_aimodel_by_name(name, project_uid=self.uid, version=version)

    def search_for_aimodels_by_name(
        self, name, version=VersionMode.LATEST, name_filter_mode=None, **_kwargs
    ):
        """
        Get AIModels associated with this project

        See Also
        --------
        rhino_health.lib.endpoints.project.project_endpoints.ProjectEndpoints.search_for_aimodels_by_name : Full documentation
        """
        return self.session.project.search_for_aimodels_by_name(
            name, project_uid=self.uid, version=version, name_filter_mode=name_filter_mode
        )

    def aggregate_cohort_metric(self, *args, **kwargs):
        return self.session.project.aggregate_cohort_metric(*args, **kwargs)

    # Add Schema
    # Local Schema from CSV
