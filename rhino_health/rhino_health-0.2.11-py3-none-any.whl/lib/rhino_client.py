import sys

from rhino_health.lib.constants import ApiEnvironment
from rhino_health.lib.endpoints.aimodel.aimodel_endpoints import AIModelEndpoints
from rhino_health.lib.endpoints.cohort.cohort_endpoints import (
    CohortEndpoints,
    CohortFutureEndpoints,
)
from rhino_health.lib.endpoints.data_schema.data_schema_endpoints import (
    DataschemaEndpoints,
    DataschemaFutureEndpoints,
)
from rhino_health.lib.endpoints.model_result.model_result_endpoints import (
    ModelResultEndpoints,
    ModelResultFutureEndpoints,
)
from rhino_health.lib.endpoints.project.project_endpoints import (
    ProjectEndpoints,
    ProjectFutureEndpoints,
)
from rhino_health.lib.endpoints.workgroup.workgroup_endpoints import (
    WorkgroupEndpoints,
    WorkgroupFutureEndpoints,
)
from rhino_health.lib.utils import alias, rhino_error_wrapper, setup_traceback, url_for

__api__ = ["RhinoClient"]


class EndpointTypes:
    """
    Constants for different endpoint types. This is how we group and separate different endpoints
    """

    PROJECT = "project"
    COHORT = "cohort"
    DATA_SCHEMA = "data_schema"
    AIMODEL = "aimodel"
    MODEL_RESULT = "model_action"
    WORKGROUP = "workgroup"


class SDKVersion:
    """
    Used internally for future backwards compatibility
    """

    STABLE = "0.1"
    PREVIEW = "1.0"


VERSION_TO_CLOUD_API = {SDKVersion.STABLE: "v1", SDKVersion.PREVIEW: "v1"}


VERSION_TO_ENDPOINTS = {
    SDKVersion.STABLE: {
        EndpointTypes.PROJECT: ProjectEndpoints,
        EndpointTypes.COHORT: CohortEndpoints,
        EndpointTypes.DATA_SCHEMA: DataschemaEndpoints,
        EndpointTypes.AIMODEL: AIModelEndpoints,
        EndpointTypes.MODEL_RESULT: ModelResultEndpoints,
        EndpointTypes.WORKGROUP: WorkgroupEndpoints,
    },
    SDKVersion.PREVIEW: {
        EndpointTypes.PROJECT: ProjectFutureEndpoints,
        EndpointTypes.COHORT: CohortFutureEndpoints,
        EndpointTypes.DATA_SCHEMA: DataschemaFutureEndpoints,
        EndpointTypes.AIMODEL: AIModelEndpoints,
        EndpointTypes.MODEL_RESULT: ModelResultFutureEndpoints,
        EndpointTypes.WORKGROUP: WorkgroupFutureEndpoints,
    },
}


class RhinoClient:
    """
    Allows access to various endpoints directly from the RhinoSession

    Attributes
    ----------
    aimodel: Access endpoints at the aimodel level
    cohort: Access endpoints at the cohort level
    data_schema: Access endpoints at the data_schema level
    model_result: Access endpoints at the model_result level
    project: Access endpoints at the project level
    data_schema: Access endpoints at the schema level

    Examples
    --------
    >>> session.project.get_projects()
    array[Project...]
    >>> session.cohort.get_cohort(my_cohort_id)
    Cohort

    See Also
    --------
    rhino_health.lib.endpoints.aimodel.aimodel_endpoints: Available aimodel endpoints
    rhino_health.lib.endpoints.cohort.cohort_endpoints: Available cohort endpoints
    rhino_health.lib.endpoints.data_schema.data_schema_endpoints: Available data_schema endpoints
    rhino_health.lib.endpoints.model_result.model_result_endpoints: Available model_result endpoints
    rhino_health.lib.endpoints.project.project_endpoints: Available project endpoints
    rhino_health.lib.endpoints.workgroup.workgroup_endpoints: Available workgroup endpoints
    """

    @rhino_error_wrapper
    def __init__(
        self,
        rhino_api_url: str = ApiEnvironment.PROD_API_URL,
        sdk_version: str = SDKVersion.PREVIEW,
        show_traceback: bool = False,
    ):
        setup_traceback(sys.excepthook, show_traceback)
        self.rhino_api_url = rhino_api_url
        self.sdk_version = sdk_version
        if sdk_version not in VERSION_TO_ENDPOINTS.keys():
            raise ValueError(
                "The api version you specified is not supported in this version of the SDK"
            )
        self.aimodel: AIModelEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.AIMODEL](
            self
        )
        self.cohort: CohortEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.COHORT](self)
        self.data_schema: DataschemaEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.DATA_SCHEMA
        ](self)
        # TODO: Should there be dicomweb here
        self.model_result: ModelResultEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.MODEL_RESULT
        ](self)
        self.project: ProjectEndpoints = VERSION_TO_ENDPOINTS[sdk_version][EndpointTypes.PROJECT](
            self
        )
        self.workgroup: WorkgroupEndpoints = VERSION_TO_ENDPOINTS[sdk_version][
            EndpointTypes.WORKGROUP
        ](self)
        self.api_url = url_for(self.rhino_api_url, VERSION_TO_CLOUD_API[sdk_version])

    @property
    def dataschema(self):
        """
        @autoapi False
        """
        return alias(
            self.data_schema,
            "dataschema",
            is_property=True,
            new_function_name="data_schema",
            base_object="session",
        )()
