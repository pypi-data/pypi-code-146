"""Library defining the interface to a project."""
import json
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict, Iterator, List, NamedTuple, Optional, Tuple, cast

from rime_sdk.firewall import Firewall, get_reference_set_source
from rime_sdk.internal.config_parser import convert_config_to_swagger
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.internal.swagger_utils import (
    get_bin_size_swagger,
    get_data_params_swagger,
    get_data_type_enum_swagger,
    get_model_task_enum_swagger,
    get_swagger_data_type_enum,
    get_threshold_info_swagger,
    location_args_to_data_location_swagger,
    valid_model_task_for_data_type,
)
from rime_sdk.internal.utils import convert_dict_to_html, make_link
from rime_sdk.job import Job
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import (
    ApiClient,
    RimeCreateFirewallFromDataRequest,
    RimeDataLocation,
)
from rime_sdk.swagger.swagger_client.models import (
    ComponentsProjectIdBody,
    DigestConfigDigestFrequency,
    FirewallProjectIdBody,
    NotificationObjectType,
    RimeAnnotatedProject,
    RimeConfig,
    RimeCreateFirewallResponse,
    RimeCreateNotificationRequest,
    RimeDigestConfig,
    RimeFirewallComponents,
    RimeFirewallRules,
    RimeJobActionConfig,
    RimeLicenseLimit,
    RimeLimitStatusStatus,
    RimeListNotificationsResponse,
    RimeManagedImageReference,
    RimeMonitoringConfig,
    RimeNotificationType,
    RimeWebhookConfig,
    TestrunresultGetTestRunResponse,
)
from rime_sdk.swagger.swagger_client.rest import ApiException
from rime_sdk.test_run import TestRun

NOTIFICATION_TYPE_JOB_ACTION_STR: str = "Job_Action"
NOTIFICATION_TYPE_MONITORING_STR: str = "Monitoring"
NOTIFICATION_TYPE_DIGEST_STR: str = "Daily_Digest"
NOTIFICATION_TYPE_UNSPECIFIED_STR: str = "Unspecified"
NOTIFICATION_TYPES_STR_LIST: List[str] = [
    NOTIFICATION_TYPE_JOB_ACTION_STR,
    NOTIFICATION_TYPE_MONITORING_STR,
    NOTIFICATION_TYPE_DIGEST_STR,
]


class ProjectInfo(NamedTuple):
    """This object contains static information that describes a project."""

    project_id: str
    """How to refer to the project in the backend."""
    name: str
    """Name of the project."""
    description: str
    """Description of the project"""


class Project:
    """An interface to a RIME project.

    This object provides an interface for editing, updating, and deleting projects.

    Attributes:
        api_client: ApiClient
                The client used to query about the status of the job.
        project_id: str
            The identifier for the RIME project that this object monitors.
    """

    def __init__(self, api_client: ApiClient, project_id: str) -> None:
        """Contains information about a RIME Project.

        Args:
            api_client: ApiClient
                The client used to query about the status of the job.
            project_id: str
                The identifier for the RIME project that this object monitors.
        """
        self._api_client = api_client
        self._project_id = project_id

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"Project({self._project_id})"

    def _repr_html_(self) -> str:
        """Return HTML representation of the object."""
        info = {
            "Project ID": self._project_id,
            "Link": make_link("https://" + self.get_link(), link_text="Project Page"),
        }
        return convert_dict_to_html(info)

    @property
    def project_id(self) -> str:
        """Return the id of this project."""
        return self._project_id

    def _check_firewall_creation_limit(self) -> None:
        """Check if creating another firewall would be within license limits.

        Raises:
            ValueError if another firewall cannot be created as it would
            exceed license limits.
        """
        api = swagger_client.RIMEInfoApi(self._api_client)
        with RESTErrorHandler():
            rime_info_response = api.r_ime_info_get_rime_info()

        feature_flag_api = swagger_client.FeatureFlagApi(self._api_client)
        with RESTErrorHandler():
            feature_flag_response = feature_flag_api.feature_flag_get_limit_status(
                customer_name=rime_info_response.customer_name,
                limit=RimeLicenseLimit.FIREWALL,
            )

        limit_status = feature_flag_response.limit_status.limit_status
        limit_value = feature_flag_response.limit_status.limit_value
        if limit_status == RimeLimitStatusStatus.WARN:
            curr_value = int(feature_flag_response.limit_status.current_value)
            print(
                f"You are approaching the limit ({curr_value + 1}"
                f"/{limit_value}) of models monitored. Contact the"
                f" Robust Intelligence team to upgrade your license."
            )
        elif limit_status == RimeLimitStatusStatus.ERROR:
            # could be either within grace period or exceeded grace period
            # if the latter, let the create firewall call raise the
            # error
            print(
                "You have reached the limit of models monitored."
                " Contact the Robust Intelligence team to"
                " upgrade your license."
            )
        elif limit_status == RimeLimitStatusStatus.OK:
            pass
        else:
            raise ValueError("Unexpected status value.")

    def _get_data_type(self, test_run_id: str) -> str:
        """Get the Data Type associated with this test run."""
        with RESTErrorHandler():
            api = swagger_client.ResultsReaderApi(self._api_client)
            res: TestrunresultGetTestRunResponse = api.results_reader_get_test_run(
                test_run_id=test_run_id,
            )
        if res.test_run:
            return res.test_run.data_type
        else:
            raise ValueError("no test run found")

    def _get_project(self) -> RimeAnnotatedProject:
        """Get the project info from the backend.

        Returns:
            A ``GetProjectResponse`` object.
        """
        api = swagger_client.ProjectManagerApi(self._api_client)
        with RESTErrorHandler():
            response = api.project_manager_get_project(self._project_id)
            return response.project

    @property
    def info(self) -> ProjectInfo:
        """Return information about this project."""
        project = self._get_project()
        return ProjectInfo(
            self._project_id, project.project.name, project.project.description,
        )

    def get_link(self) -> str:
        """Get the web app URL to the project.

        This link directs to your organization's deployment of RIME.
        You can view more detailed information in the web app, including
        information on your test runs, comparisons of those results,
        and models that are monitored.

        Note: this is a string that should be copy-pasted into a browser.
        """
        project = self._get_project()
        return project.web_app_url.url

    @property
    def name(self) -> str:
        """Return the name of this project."""
        return self.info.name

    @property
    def description(self) -> str:
        """Return the description of this project."""
        return self.info.description

    def list_test_runs(self) -> Iterator[TestRun]:
        """List the stress test runs associated with the project."""
        api = swagger_client.ResultsReaderApi(self._api_client)
        # Iterate through the pages of projects and break at the last page.
        page_token = ""
        while True:
            if page_token == "":
                res = api.results_reader_list_test_runs(project_id=self._project_id)
            else:
                res = api.results_reader_list_test_runs(page_token=page_token)
            if res.test_runs is not None:
                for test_run in res.test_runs:
                    yield TestRun(self._api_client, test_run.test_run_id)
            # Advance to the next page of test cases.
            page_token = res.next_page_token
            # we've reached the last page of test cases.
            if not res.has_more:
                break

    def create_firewall(
        self,
        name: str,
        bin_size: str,
        test_run_id: str,
        run_ct_schedule: bool = False,
        rolling_window_duration: Optional[timedelta] = None,
        reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
        location_type: Optional[str] = None,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rime_managed_image: Optional[str] = None,
    ) -> Firewall:  # noqa: D400, D402
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Bin size. Can be `year`, `month`, `week`, `day`, `hour`.
            test_run_id: str
                ID of the stress test run that firewall will be based on.
            run_ct_schedule: bool
                Flag for ct scheduler.
            rolling_window_duration: Optional[int]
                Time duration of rolling window of reference set if provided.
                The rolling window is only supported for firewall running scheduled ct.
                Only one of rolling_window_seconds or reference_set_time_bin may be set.
            reference_set_time_bin: Optional[Tuple[datetime, datetime]]
                Time bin of reference set can be set for firewall running scheduled ct.
                Only one of rolling_window_seconds or reference_set_time_bin may be set.
            location_type: Optional[str]
                Type of the data location that ScheduledCT will pull data from.
            location_info: Optional[Dict]
                Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.


        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW based on foo stress test in project.
            firewall = project.create_firewall(
                "firewall name", "day", "foo")
        """
        self._check_firewall_creation_limit()
        bin_size_swagger = get_bin_size_swagger(bin_size_str=bin_size)
        reference_set_source = get_reference_set_source(
            rolling_window_duration=rolling_window_duration,
            reference_set_time_bin=reference_set_time_bin,
        )
        req = FirewallProjectIdBody(
            name=name,
            bin_size=bin_size_swagger,
            run_ct_schedule=run_ct_schedule,
            stress_test_run_id=test_run_id,
            reference_set_source=reference_set_source,
        )

        if rime_managed_image:
            req.managed_image = RimeManagedImageReference(name=rime_managed_image)

        # Prevent location info from being provided without location type
        if location_info is not None and location_type is None:
            raise ValueError("Must Specify both location type and location info.")
        if location_type is not None:
            swagger_data_type = self._get_data_type(test_run_id)
            location_args = location_args_to_data_location_swagger(
                location_type, location_info, data_params, swagger_data_type
            )
            req.data_location_info = location_args
        try:
            api = swagger_client.FirewallServiceApi(self._api_client)
            res = api.firewall_service_create_firewall_from_test_run_id(
                body=req, project_id=self._project_id
            )
            res = cast(RimeCreateFirewallResponse, res)
            return Firewall(self._api_client, res.firewall_id)
        except ApiException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                raise ValueError(
                    f"a test run with this id (`{test_run_id}`)  does not exist"
                )
            raise ValueError(e.reason) from None

    def create_firewall_from_components(
        self,
        name: str,
        bin_size: str,
        stress_test_config: Dict[str, Any],
        firewall_rules: List[Dict[str, Any]],
        threshold_infos: List[dict],
        run_ct_schedule: bool = False,
        location_type: Optional[str] = None,
        location_info: Optional[Dict] = None,
        data_params: Optional[Dict] = None,
        rime_managed_image: Optional[str] = None,
        data_type: str = "tabular",
    ) -> Firewall:  # noqa: D400, D402
        """Create a Firewall for a given project.

        Args:
            name: str
                FW name.
            bin_size: str
                Can be `year`, `month`, `week`, `day`, `hour`.
            stress_test_config: dict
                RIME Config that indicates the testing, model, and data configurations
            firewall_rules: List[Dict]
                Firewall Rules to update the firewall with.
            threshold_infos: List[Dict]
                Threshold info for each summary metric.
            run_ct_schedule: bool
                Flag for ct scheduler.
            location_type: Optional[str]
                Type of the data location that ScheduledCT will pull data from.
            location_info:  Optional[Dict]
                Information needed to access the data location provided.
            data_params: Optional[Dict]
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rime_managed_image: Optional[str]
                Name of a managed image to use when running the model test.
                The image must have all dependencies required by your model. To create
                new managed images with your desired dependencies, use the client's
                ``create_managed_image()`` method.
            data_type: str
                Type of data this firewall test is to be run on. Should be one of
                `tabular`, `nlp`, `images`. Defaults to `tabular`.


        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the provided values are invalid.
                If the request to the Firewall service failed.

        Example:

        .. code-block:: python

            # Create FW manually from components.
           stress_test_config = {
                "data_info": {
                    "pred_col": "preds",
                    "label_col": "label",
                    "ref_path": "s3://my-bucket/my-data.csv",
                },
                "model_info": {"path": "s3://model-test-bucket/model.py",},
                "model_task": "Binary Classification",
            }
            firewall_rules = [
                {
                    "test_name": "Unseen Categorical",
                    "description": "Value must be in a required set of values",
                    "is_transformation": False,
                    "firewall_configs": [
                        {
                            "rule_info": {
                                "feature_names": ["city"],
                                "flagged_action": "FLAG",
                            }
                        }
                    ],
                }
            ]
            metric_thresholds = [
                {
                    "direction": "below",
                    "low": 0.999,
                    "medium": 0.99,
                    "high": 0.9,
                    "metric_name": "accuracy",
                }
            ]
            firewall = project.create_firewall_from_components(
                "firewall name",
                "day",
                stress_test_config,
                firewall_rules,
                metric_thresholds,
            )
        """
        bin_size_swagger = get_bin_size_swagger(bin_size_str=bin_size)
        swagger_data_type = get_data_type_enum_swagger(data_type)
        typed_cli_config = convert_config_to_swagger(
            stress_test_config, swagger_data_type
        )
        firewall_rules_swagger = RimeFirewallRules(
            data=json.dumps(firewall_rules).encode("utf-8")
        )
        metric_thresholds = [
            get_threshold_info_swagger(threshold_dict)
            for threshold_dict in threshold_infos
        ]
        req = ComponentsProjectIdBody(
            name=name,
            bin_size=bin_size_swagger,
            run_ct_schedule=run_ct_schedule,
            components=RimeFirewallComponents(
                typed_cli_config=typed_cli_config,
                firewall_rules=firewall_rules_swagger,
                threshold_infos=metric_thresholds,
            ),
        )

        if rime_managed_image:
            req.managed_image = RimeManagedImageReference(name=rime_managed_image)

        # Prevent location info from being provided without location type
        if location_info is not None and location_type is None:
            raise ValueError("Must Specify both location type and location info.")
        if location_type is not None:
            location_args = location_args_to_data_location_swagger(
                location_type, location_info, data_params, swagger_data_type
            )
            req.data_location_info = location_args
        with RESTErrorHandler():
            api = swagger_client.FirewallServiceApi(self._api_client)
            res = api.firewall_service_create_firewall_from_components(
                body=req, project_id=self._project_id
            )
            res = cast(RimeCreateFirewallResponse, res)
            return Firewall(self._api_client, res.firewall_id)

    def create_firewall_from_data(
        self,
        name: str,
        data_type: str,
        model_task: str,
        bin_size: str,
        data_params: Dict,
        rolling_window_duration: Optional[timedelta] = None,
        reference_set_time_bin: Optional[Tuple[datetime, datetime]] = None,
        reference_set_file_path: Optional[str] = None,
        run_ct_schedule: bool = False,
        location_type: Optional[str] = None,
        location_info: Optional[dict] = None,
    ) -> Tuple[Job, str]:
        """Create a firewall directly from data without a stress test.

        Arguments:
            name: str
                FW name.
            data_type: str
                Data type. Can be `tabular` or `nlp`.
            model_task: str
                Model task. Can be `Binary Classification`, `Multi-class
                Classification`, `Regression`, `Ranking`, `Named Entity Recognition`,
                `Natural Language Inference`, or `Text Classification`.
            bin_size: str
                Bin size. Can be `year`, `month`, `week`, `day`, `hour`.
            data_params: Dict
                Information needed to process data from the data location provided.
                By default, these are obtained from your reference information.
                Eg. `pred_col`, `timestamp_col`, `label_col`, etc...
            rolling_window_duration: Optional[timedelta]
                Fixed Time duration of rolling window.
                Only one of rolling_window_seconds, reference_set_time_bin, or
                reference_set_file_path may be set. If this is specified, then data
                location and its related parameters must be set.
            reference_set_time_bin: Optional[Tuple[datetime, datetime]]
                Time bin of reference set can be set for firewall running scheduled ct.
                Only one of rolling_window_seconds, reference_set_time_bin, or
                reference_set_file_path may be set. If this is specified, then data
                location and its related parameters must be set.
            reference_set_file_path: str
                File path for reference set in S3 bucket.
                Only one of rolling_window_seconds, reference_set_time_bin, or
                reference_set_file_path may be set.
            run_ct_schedule: bool
                Flag for ct scheduler.
            location_type: Optional[str]
                Type of the data location that ScheduledCT will pull data from.
            location_info: Optional[Dict]
                Information needed to access the data location provided.

        Returns:
            A tuple containing the job for profiling the reference set and the
            firewall ID.

        Raises:
            ValueError
                If the provided values are invalid.
        """
        data_type_sw = get_swagger_data_type_enum(data_type)
        model_task_sw = get_model_task_enum_swagger(model_task)
        if not valid_model_task_for_data_type(model_task_sw, data_type_sw):
            raise ValueError(f"Model task {model_task} not valid for {data_type} data.")
        if reference_set_file_path is None and location_type is None:
            raise ValueError("Data location required if no file path specified.")

        data_location_sw: Optional[RimeDataLocation] = None
        if location_type is not None:
            data_location_sw = location_args_to_data_location_swagger(
                location_type=location_type,
                location_info=location_info,
                data_params=data_params,
                data_type=data_type_sw,
            )

        data_params_sw = get_data_params_swagger(data_params, data_type_sw)
        req = RimeCreateFirewallFromDataRequest(
            name=name,
            project_id=self._project_id,
            data_type=data_type_sw,
            model_task=model_task_sw,
            run_ct_schedule=run_ct_schedule,
            bin_size=get_bin_size_swagger(bin_size),
            reference_set_source=get_reference_set_source(
                reference_set_time_bin=reference_set_time_bin,
                rolling_window_duration=rolling_window_duration,
                file_path=reference_set_file_path,
            ),
            data_location_info=data_location_sw,
            data_params=data_params_sw,
        )
        with RESTErrorHandler():
            api = swagger_client.ModelTestingApi(self._api_client)
            response = api.model_testing_create_firewall_from_data(body=req)
            job = Job(self._api_client, response.stress_test_job.job_id)
            firewall_id = response.firewall.id
        return job, firewall_id

    def _get_firewall_id(self) -> Optional[str]:
        api = swagger_client.ProjectManagerApi(self._api_client)
        with RESTErrorHandler():
            response = api.project_manager_get_project(project_id=self._project_id)
            return response.project.project.firewall_id

    def get_firewall(self) -> Firewall:
        """Get the active Firewall for a project if it exists.

        Query the backend for an active `Firewall` in this project which
        can be used to perform Firewall operations. If there is no active
        Firewall for the project, this call will error.

        Returns:
            A ``Firewall`` object.

        Raises:
            ValueError
                If the Firewall does not exist.

        Example:

        .. code-block:: python

            # Get FW if it exists.
            firewall = project.get_firewall()
        """
        firewall_id = self._get_firewall_id()
        if firewall_id is None:
            raise ValueError("No firewall found for given project.")
        return Firewall(self._api_client, firewall_id)

    def has_firewall(self) -> bool:
        """Check whether a project has a firewall or not."""
        firewall_id = self._get_firewall_id()
        return firewall_id is not None

    def delete_firewall(self) -> None:
        """Delete firewall for this project if exists."""
        firewall = self.get_firewall()
        firewall.delete_firewall()

    def _list_notification_settings(self) -> RimeListNotificationsResponse:
        """Get list of notifications associated with the current project."""
        api = swagger_client.NotificationSettingApi(self._api_client)
        with RESTErrorHandler():
            response = api.notification_setting_list_notifications(
                list_notifications_query_notification_object_ids=[self._project_id]
            )
            return response

    def _set_create_notification_setting_config_from_type(
        self, req: RimeCreateNotificationRequest, notif_type: str
    ) -> None:
        if notif_type == RimeNotificationType.JOB_ACTION:
            req.config.job_action = RimeJobActionConfig()
        elif notif_type == RimeNotificationType.MONITORING:
            req.config.monitoring_config = RimeMonitoringConfig()
        elif notif_type == RimeNotificationType.DIGEST:
            req.config.digest_config = RimeDigestConfig(
                frequency=DigestConfigDigestFrequency.DAILY
            )

    def _get_notification_type_from_str(self, notif_type: str) -> str:
        if notif_type == NOTIFICATION_TYPE_JOB_ACTION_STR:
            return RimeNotificationType.JOB_ACTION
        elif notif_type == NOTIFICATION_TYPE_MONITORING_STR:
            return RimeNotificationType.MONITORING
        elif notif_type == NOTIFICATION_TYPE_DIGEST_STR:
            return RimeNotificationType.DIGEST
        else:
            raise ValueError(
                f"Notification type must be one of {NOTIFICATION_TYPES_STR_LIST}"
            )

    def _get_notification_type_str(self, notif_type: str) -> str:
        if notif_type == RimeNotificationType.JOB_ACTION:
            return NOTIFICATION_TYPE_JOB_ACTION_STR
        elif notif_type == RimeNotificationType.MONITORING:
            return NOTIFICATION_TYPE_MONITORING_STR
        elif notif_type == RimeNotificationType.DIGEST:
            return NOTIFICATION_TYPE_DIGEST_STR
        else:
            # This function is called only to show the user notification types
            # as string as defined in NOTIFICATION_TYPES_STR_LIST. We will have
            # to update this if we add more notification types in the future.
            # Making it unspecified will not break any SDK/BE mismatch and still
            # show users the new notification type with unspecified tag.
            # This situation should not happen ideally
            return NOTIFICATION_TYPE_UNSPECIFIED_STR

    def get_notification_settings(self) -> Dict:
        """Get the list of notifications for the project.

        Queries the backend to get a list of notifications
        added to the project. The notifications are grouped by the type
        of the notification and each type contains a list of emails and webhooks
        which are added to the notification setting

        Returns:
            A Dictionary of notification type and corresponding
            emails and webhooks added for that notification type.

        Example:

        .. code-block:: python

            notification_settings = project.list_notification_settings()
        """
        notif_list = self._list_notification_settings()
        out: Dict = {}
        for notif in notif_list.notifications:
            notif_type_str = self._get_notification_type_str(notif.notification_type)
            out[notif_type_str] = {}
            out[notif_type_str]["emails"] = notif.emails
            out[notif_type_str]["webhooks"] = []
            for webhook in notif.webhooks:
                out[notif_type_str]["webhooks"].append(webhook.webhook)
        return out

    def _add_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[RimeWebhookConfig],
    ) -> None:
        """Add the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be added in a single call. emails are checked first and we add a
        webhook only when email is set to None. The function first checks if
        a notification object exists for the give notification type and appends
        the email/webhook if found, else it creates a new notification object
        """
        api = swagger_client.NotificationSettingApi(self._api_client)
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_add_notif_entry expects exactly one of email or "
                "webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            print(
                                f"Email: {email} already exists in notification "
                                f"settings for notification type: {notif_type_str}"
                            )
                            return
                    notif_setting.emails.append(email)
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            print(
                                f"Webhook: {webhook_config.webhook} "
                                "already exists in notification settings "
                                f"for notification type: {notif_type_str}"
                            )
                            return
                    notif_setting.webhooks.append(webhook_config)
                with RESTErrorHandler():
                    api.notification_setting_update_notification(
                        body=notif_setting, notification_id=notif_setting.id
                    )
                    return
        # Notification setting does not exist for the notif_type.
        req = RimeCreateNotificationRequest(
            notification_object_type=NotificationObjectType.PROJECT,
            notification_object_id=self.project_id,
            config=RimeConfig(),
            emails=[],
            webhooks=[],
        )
        self._set_create_notification_setting_config_from_type(req, notif_type)
        notif_entry_str = ""
        if email is not None:
            req.emails.append(email)
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            req.webhooks.append(webhook_config)
            notif_entry_str = "Webhook " + webhook_config.webhook
        with RESTErrorHandler():
            api.notification_setting_create_notification(body=req)
            print(f"{notif_entry_str} added for notification type {notif_type_str}")
            return

    def _remove_notif_entry(
        self,
        notif_type_str: str,
        email: Optional[str],
        webhook_config: Optional[RimeWebhookConfig],
    ) -> None:
        """Remove the email or webhook in the notification settings of notif_type.

        This function should be called with either one of an email or a webhook
        to be removed in a single call. emails are checked first and we remove
        webhook only when email is set to None. In case a delete operation
        leads to the notification object having no email or webhook, that
        notification object is deleted as well.
        """
        if email is not None and webhook_config is not None:
            raise ValueError(
                "_remove_notif_entry expects exactly one of email "
                "or webhook config to be set"
            )
        notif_setting_list = self._list_notification_settings()
        notif_type = self._get_notification_type_from_str(notif_type_str)
        for notif_setting in notif_setting_list.notifications:
            if notif_setting.notification_type == notif_type:
                found = False
                if email is not None:
                    for existing_email in notif_setting.emails:
                        if existing_email == email:
                            notif_setting.emails.remove(existing_email)
                            found = True
                elif webhook_config is not None:
                    for existing_webhook in notif_setting.webhooks:
                        if existing_webhook.webhook == webhook_config.webhook:
                            notif_setting.webhooks.remove(existing_webhook)
                            found = True
                if found:
                    api = swagger_client.NotificationSettingApi(self._api_client)
                    with RESTErrorHandler():
                        if (
                            len(notif_setting.emails) == 0
                            and len(notif_setting.webhooks) == 0
                        ):
                            api.notification_setting_delete_notification(
                                id=notif_setting.id
                            )
                        else:
                            body = {"notification": notif_setting}
                            api.notification_setting_update_notification(
                                body=body, notification_id=notif_setting.id
                            )
                        return
        notif_entry_str = ""
        if email is not None:
            notif_entry_str = "Email " + email
        elif webhook_config is not None:
            notif_entry_str = "Webhook " + webhook_config.webhook
        print(f"{notif_entry_str} not found for notification type {notif_type_str}")

    def add_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add an email to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def remove_email(self, email: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Remove an email from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_email("<email>", "<notification type>")
        """
        if email == "":
            raise ValueError("Email must be a non empty string")
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=email, webhook_config=None
        )

    def add_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long
        """Add a webhook to the notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.add_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = RimeWebhookConfig(webhook=webhook)
        return self._add_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def remove_webhook(self, webhook: str, notif_type_str: str) -> None:
        # pylint: disable=line-too-long,
        """Remove a webhook from notification settings for the given notification type.

        Currently, we support 3 notification types:
        ["Job_Action", "Monitoring", "Daily_Digest"]

        Example:
            .. code-block:: python

                notification_settings = project.remove_webhook("<webhook>", "<notification type>")
        """
        if webhook == "":
            raise ValueError("Webhook must be a non empty string")
        webhook_config = RimeWebhookConfig(webhook=webhook)
        return self._remove_notif_entry(
            notif_type_str=notif_type_str, email=None, webhook_config=webhook_config
        )

    def delete(self) -> None:
        """Delete project in RIME's backend."""
        api = swagger_client.ProjectManagerApi(self._api_client)
        try:
            api.project_manager_delete_project(self._project_id)
        except ApiException as e:
            if e.status == HTTPStatus.NOT_FOUND:
                raise ValueError(
                    f"project with this id {self._project_id} does not exist"
                )
            raise ValueError(e.reason)
