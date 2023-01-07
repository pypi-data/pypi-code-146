import csv
from typing import Any, List, Optional
from warnings import warn

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA


class SchemaVariable(BaseModel, extra=RESULT_DATACLASS_EXTRA):
    """
    A schema variable
    """

    # TODO: Better type checks
    name: str
    identifier: Optional[str]
    description: Optional[str]
    role: Optional[str]
    type: Optional[str]
    type_params: Any
    units: Optional[str]
    may_contain_phi: Optional[bool]
    permissions: Optional[str]


class SchemaVariables(list):
    """
    Extension of a list that provides some convenience functions
    """

    def __init__(self, schema_variables: List[dict]):
        self.field_names = schema_variables[0].keys()
        schema_variables = self._parse_data(schema_variables)
        super(SchemaVariables, self).__init__(schema_variables)

    def _parse_data(self, schema_variables: List[dict]):
        return [SchemaVariable(**schema_variable) for schema_variable in schema_variables]

    def dict(self, *args, **kwargs):
        return [schema_variable.dict(*args, **kwargs) for schema_variable in self]

    def to_csv(self, output_file):
        """
        @autoai False
        """
        # TODO: RH-1871 Ability to write to CSV again
        raise NotImplementedError


class BaseDataschema(RhinoBaseModel, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    Base Dataschema used by both return result and creation
    """

    name: str
    """@autoapi True The name of the Dataschema"""
    description: str
    """@autoapi True The description of the Dataschema"""
    base_version_uid: Optional[str]
    """@autoapi True If this Dataschema is a new version of another Dataschema, the original Unique ID of the base Dataschema."""
    primary_workgroup_uid: Annotated[str, Field(alias="primary_workgroup")]
    """@autoapi True The UID of the primary workgroup for this data schema"""
    version: Optional[int] = 0
    """@autoapi True The revision of this Dataschema"""
    project_uids: Annotated[List[str], Field(alias="projects")]
    """@autoapi True A list of UIDs of the projects this data schema is associated with"""


class DataschemaCreateInput(BaseDataschema):
    """
    @autoapi True
    Input for creating a new dataschema

    Examples
    --------
    >>> DataschemaCreateInput(
    >>>     name="My Dataschema",
    >>>     description="A Sample Dataschema",
    >>>     primary_workgroup_uid=project.primary_workgroup_uid,
    >>>     projects=[project.uid],
    >>>     file_path="/absolute/path/to/my_schema_file.csv"
    >>> )
    """

    schema_variables: List[str] = []
    """ A list of rows representing the schema variables from a csv file.

    Users are recommended to use file_path instead of directly setting this value
    
    The first row should be the field names in the schema. Each list string should have a newline at the end.
    Each row should have columns separated by commas.
    """
    file_path: Optional[str] = None
    """ Path to a `CSV <https://en.wikipedia.org/wiki/Comma-separated_values>`_ File 
    that can be opened with python's built in `open() <https://docs.python.org/3/library/functions.html#open>`_ command.
    """

    def __init__(self, **data):
        self._load_csv_file(data)
        super(BaseDataschema, self).__init__(**data)

    def _load_csv_file(self, data):
        file_path = data.get("file_path", None)
        if file_path:
            data["schema_variables"] = open(
                file_path, "r", encoding="utf-8", newline=None
            ).readlines()
            # TODO: Verify the schema file is correct
            del data["file_path"]


class Dataschema(BaseDataschema):
    """
    @autoapi False
    """

    uid: Optional[str]
    """@autoapi True The Unique ID of the Dataschema"""
    created_at: str
    """@autoapi True When this Dataschema was created"""
    num_cohorts: int
    """@autoapi True The number of cohorts using this Dataschema"""
    creator: "User"
    """@autoapi True The creator of this Dataschema"""


class FutureDataschema(Dataschema):
    """
    @autoapi True
    @objname Dataschema
    A dataschema in the system used by cohorts
    """

    schema_variables: SchemaVariables
    """@autoapi True A list of schema variables in this data schema"""
    _projects: Any = None
    _primary_workgroup: Any = None

    def __init__(self, **data):
        self._handle_schema_variables(data)
        super().__init__(**data)

    def _handle_schema_variables(self, data):
        raw_schema_variable = data["schema_variables"]
        data["schema_variables"] = SchemaVariables(raw_schema_variable)

    @property
    def projects_uids(self):
        """
        @autoapi False

        .. warning:: This function is deprecated and will be removed in the future, please call project_uids
        """
        warn(
            "DataSchema.projects_uids is deprecated and will be removed in the future, please use project_uids()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.project_uids

    @property
    def projects(self):
        """
        @autoapi True

        Get the projects of using this Dataschema

        .. warning:: Be careful when calling this for newly created objects.
            The projects associated with the PROJECT_UIDS must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the dataschema

        Returns
        -------
        projects: List[Project]
            A DataClass representing the Project of the user's primary workgroup

        See Also
        --------
        rhino_health.lib.endpoints.project.project_dataclass : Project Dataclass
        """
        if self._projects:
            return self._projects
        if self.project_uids:
            self._projects = self.session.project.get_projects(self.project_uids)
            return self._projects
        else:
            return None

    def delete(self):
        if not self._persisted or not self.uid:
            raise RuntimeError("Dataschema has already been deleted")

        self.session.data_schema.remove_dataschema(self.uid)
        self._persisted = False
        self.uid = None
        return self

    @property
    def primary_workgroup(self):
        """
        Return the primary workgroup associated with this Dataschema

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the project

        Returns
        -------
        primary_workgroup: Workgroup
            DataClasses representing the Primary Workgroup of the Dataschema
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


from rhino_health.lib.endpoints.user.user_dataclass import User

Dataschema.update_forward_refs()
FutureDataschema.update_forward_refs()
