import base64
import json
from typing import Any, Optional

from pydantic import Field
from typing_extensions import Annotated, Literal

from rhino_health.lib.constants import ECRService
from rhino_health.lib.dataclass import RhinoBaseModel
from rhino_health.lib.endpoints.endpoint import RESULT_DATACLASS_EXTRA
from rhino_health.lib.utils import RhinoSDKException, alias


class BaseCohort(RhinoBaseModel):
    """
    @autoapi False
    Used for both creating a cohort as well as returning a cohort
    """

    name: str
    """
    @autoapi True The name of the Cohort
    """
    description: str
    """
    @autoapi True The description of the Cohort
    """
    base_version_uid: Optional[str]
    """
    @autoapi True The original Cohort this Cohort is a new version of, if applicable
    """
    project_uid: Annotated[str, Field(alias="project")]
    """
    @autoapi True The unique ID of the Project this Cohort belongs to.
    """
    _project: Any = None
    workgroup_uid: Annotated[str, Field(alias="workgroup")]
    """
    @autoapi True
    The unique ID of the Workgroup this Cohort belongs to
    .. warning workgroup_uid may change to primary_workgroup_uid in the future
    """
    data_schema_uid: Annotated[Any, Field(alias="data_schema")]
    """
    @autoapi True The unique ID of the DataSchema this Cohort follows
    """

    @property
    def primary_workgroup_uid(self):
        # TODO: Standardize workgroup_uid -> primary_workgroup_uid to be consistent with the other objects
        return self.workgroup_uid

    @property
    def project(self):
        """
        @autoapi True

        Get the project of this Cohort

        .. warning:: Be careful when calling this for newly created objects.
            The project associated with the PROJECT_UID must already exist on the platform.

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the project

        Returns
        -------
        project: Project
            A DataClass representing the Project of the user's primary workgroup

        See Also
        --------
        rhino_health.lib.endpoints.project.project_dataclass : Project Dataclass
        """
        if self._project:
            return self._project
        if self.project_uid:
            self._project = self.session.project.get_projects([self.project_uid])[0]
            return self._project
        else:
            return None

    def create_args(self):
        return self.dict(
            by_alias=True,
            include={
                "name",
                "description",
                "base_version_uid",
                "project_uid",
                "workgroup_uid",
                "data_schema_uid",
            },
        )


class CohortCreateInput(BaseCohort):
    """
    Input arguments for adding a new cohort
    """

    csv_filesystem_location: str
    """@autoapi True The location the cohort data is located on-prem. The file should be a CSV."""
    method: Literal["DICOM", "filesystem"]
    """@autoapi True What source are we importing imaging data from. Either a DICOM server, or the local file system"""
    is_data_deidentified: Optional[bool] = False
    """@autoapi True Is the data already deidentified?"""

    image_dicom_server: Optional[str]
    """@autoapi True The DICOM Server URL to import DICOM images from"""
    image_filesystem_location: Optional[str]
    """@autoapi True The on-prem Location to import DICOM images from"""

    file_base_path: Optional[str]
    """@autoapi True The location of non DICOM files listed in the cohort data CSV on-prem"""
    sync: Optional[bool] = True
    """@autoapi True Should we perform this import request synchronously."""

    def import_args(self):
        return self.dict(
            by_alias=True,
            include={
                "csv_filesystem_location",
                "method",
                "is_data_deidentified",
                "image_dicom_server",
                "image_filesystem_location",
                "file_base_path",
                "sync",
            },
        )


class Cohort(BaseCohort, extra=RESULT_DATACLASS_EXTRA):
    """
    @autoapi False
    """

    uid: str
    """
    @autoapi True The unique ID of the Cohort
    """
    version: Optional[int] = 0
    """
    @autoapi True Which revision this Cohort is
    """
    created_at: str
    """
    @autoapi True When this Cohort was added
    """
    num_cases: int
    """
    @autoapi True The number of cases in the cohort
    """
    cohort_info: Optional[dict]
    """
    @autoapi True Sanitized metadata information about the cohort.
    """
    import_status: str
    """
    @autoapi True The import status of the cohort
    """
    data_schema_info: dict
    """
    @autoapi True Metadata about the DataSchema for this cohort.
    """

    def run_code(self, run_code, **kwargs):
        """
        @autoapi True

        Create and run an aimodel, Using defaults that can be overridden

        .. warning:: This function relies on a cohort's metadata so make sure to create the input cohort first
        .. warning:: This feature is under development and the interface may change

        run_code: str
            The code that will run in the container
        name: Optional[str] = "{cohort.name} (v.{cohort.version}) containerless code"
            Model name - Uses the cohort name and version as part of the default
            (eg: when using a the first version of cohort named cohort_one the name will be cohort_one (v.1) containerless code)
        description: Optional[str] = "Python code run"
            Model description
        container_image_uri: Optional[str] = {ENV_URL}/rhino-gc-workgroup-rhino-health:generic-python-runner"
            Uri to container that should be run - ENV_URL is the environment ecr repo url
        input_data_schema_uid: Optional[str] = cohort.data_schema_uid
            The data_schema used for the input cohort - By default uses the data_schema used to import the cohort
        output_data_schema_uid: Optional[str] = None (Auto generate data schema)
            The data_schema used for the output cohort - By default generates a schema from the cohort_csv
        output_cohort_names_suffix: Optional[str] = "containerless code"
            String that will be added to output cohort name
        timeout_seconds: Optional[int] = 600
            Amount of time before timeout in seconds

        Examples
        --------
        cohort.run_code(run_code = <df['BMI'] = df.Weight / (df.Height ** 2)>)

        Returns
        -------
        Tuple: (output_cohorts, run_response)
            output_cohorts: List of  Cohort Dataclasses
            run_response: An AIModelRunSyncResponse object containing the run outcome
        """
        from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import (
            AIModelCreateInput,
            AIModelRunInput,
            ModelTypes,
        )

        param_dict = {
            "name": f"{self.name} (v.{self.version}) containerless code",
            "description": f"Python code run",
            "container_image_uri": f"{ECRService.PROD_URL}/rhino-gc-workgroup-rhino-health:generic-python-runner",
            "input_data_schema_uid": str(self.data_schema_uid),
            "output_data_schema_uid": None,
            "output_cohort_names_suffix": " containerless code",
            "timeout_seconds": 600,
        }
        param_dict.update(kwargs)
        model_creation_params = {
            "session": self.session,
            "name": param_dict["name"],
            "description": param_dict["description"],
            "model_type": ModelTypes.GENERALIZED_COMPUTE,
            "config": {"container_image_uri": param_dict["container_image_uri"]},
            "project_uid": self.project_uid,
            "input_data_schema_uids": [param_dict["input_data_schema_uid"]],
            "output_data_schema_uids": [param_dict["output_data_schema_uid"]],
        }
        create_model_params = AIModelCreateInput(**model_creation_params)
        try:
            aimodel_response = self.session.aimodel.create_aimodel(create_model_params)
        except RhinoSDKException as e:
            if "already exists" in str(e):
                # A model with this name already exists - create a new version of the model object instead
                all_models = self.session.project.get_models(self.project_uid)
                matching_models = [
                    x for x in all_models if x.name == param_dict["name"] and x.version == 0
                ]
                if not matching_models:
                    raise
                base_model = matching_models[0]
                model_creation_params["base_version_uid"] = base_model.uid
                create_model_params = AIModelCreateInput(**model_creation_params)
                aimodel_response = self.session.aimodel.create_aimodel(create_model_params)
            else:
                raise

        run_model_params = AIModelRunInput(
            aimodel_uid=aimodel_response.uid,
            input_cohort_uids=[self.uid],
            output_cohort_names_suffix=param_dict["output_cohort_names_suffix"],
            run_params=json.dumps(
                {"code64": base64.b64encode(run_code.encode("utf-8")).decode("utf-8")}
            ),
            timeout_seconds=param_dict["timeout_seconds"],
            sync=True,
        )
        run_response = self.session.aimodel.run_aimodel(run_model_params)
        output_cohorts = [
            self.session.cohort.get_cohort(output_cohort)
            for output_cohort in run_response.output_cohort_uids
        ]
        return output_cohorts, run_response


class FutureCohort(Cohort):
    """
    @autoapi True
    @objname Cohort
    """

    _primary_workgroup: Any = None
    _data_schema: Optional[Any] = None

    def create(self):
        if self._persisted:
            raise RuntimeError("Cohort has already been created")
        created_cohort = self.session.cohort.create_cohort(self)
        return created_cohort

    def get_metric(self, metric_configuration):
        """
        Queries on-prem and returns the result based on the METRIC_CONFIGURATION for this cohort.

        See Also
        --------
        rhino_health.lib.endpoints.cohort.cohort_endpoints.CohortEndpoints.get_cohort_metric : Full documentation
        """
        """
        Then Cloud API use gRPC -> on-prem where the cohort raw data exists
        On on-prem we will run the sklearn metric function with the provided arguments on the raw cohort data
        on-prem will perform k-anonymization, and return data to Cloud API
        # TODO: How we support multiple instance
        # TODO: Way to exclude internal docs from autoapi
        """
        return self.session.cohort.get_cohort_metric(self.uid, metric_configuration)

    @property
    def primary_workgroup(self):
        """
        Return the primary workgroup associated with this Cohort

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the project

        Returns
        -------
        primary_workgroup: Workgroup
            DataClasses representing the Primary Workgroup of the Cohort
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
    def data_schema(self):
        """
        Return the data_schema associated with this Cohort

        .. warning:: The result of this function is cached.
            Be careful calling this function after making changes to the cohort

        Returns
        -------
        data_schema: Dataschema
            DataClasses representing the Dataschema of the Cohort
        """
        if self._data_schema:
            return self._data_schema
        if self.data_schema_uid:
            self._data_schema = self.session.data_schema.get_data_schemas([self.data_schema_uid])[0]
            return self._data_schema
        else:
            return None

    @property
    def dataschema(self):
        """@autoapi False"""
        return alias(
            self.data_schema,
            old_function_name="dataschema",
            is_property=True,
            new_function_name="data_schema",
            base_object="session.cohort",
        )()
